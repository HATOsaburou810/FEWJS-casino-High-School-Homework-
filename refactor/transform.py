# -*- coding: utf-8 -*-
"""casino_slot.py を casino/ パッケージへ機械的に分割するリファクタリングツール。

設計:
  - AST の正確な位置情報 (lineno/col_offset/end_col_offset) でソーステキストを
    直接編集するため、コメント・空行・整形は完全に保存される。
  - スコープ解析を自前で行い、グローバル状態変数への参照を `st.<name>` に、
    他モジュールのトップレベル関数参照を `<mod>.<name>` に書き換える。
  - `global` 文は削除する (属性代入になるため不要)。
  - verify サブコマンドで、生成コードを正規化 (st.x -> x, mod.F -> F) した AST が
    元の関数の AST (global文除去後) と完全一致することを機械検証する。

使い方:
  python3 refactor/transform.py split  --map refactor/module_map.json --out casino
  python3 refactor/transform.py verify --map refactor/module_map.json --out casino
"""
import ast
import json
import os
import sys

SRC = os.path.join(os.path.dirname(__file__), "..", "casino_slot.py")

# state.py に強制配置する関数 (globals()[name] による動的アクセスのため、
# 状態変数と同じモジュール名前空間に置く必要がある)
FORCE_STATE_FUNCS = {"py_getflag", "py_setflag"}

def make_aliases(mods, svars, func_names, locals_all):
    """モジュール修飾子のエイリアスを決定。状態変数・ローカル変数・関数名と
    衝突する場合 (例: 状態変数 missions vs モジュール missions) は _mod を付ける。"""
    taken = set(svars) | set(func_names) | set(locals_all)
    aliases = {}
    for mod in sorted(mods):
        cand = mod
        while cand in taken:
            cand += "_mod"
        aliases[mod] = cand
        taken.add(cand)
    st = "st"
    while st in taken:
        st += "_"
    return aliases, st


def all_local_names(items, ):
    """全関数の全スコープで束縛される名前の合算 (エイリアス衝突回避用)。"""
    names = set()

    def rec(node, scope):
        for c in ast.iter_child_nodes(node):
            if _scope_children(c):
                cs = Scope(c, scope)
                collect_bindings(c, cs)
                names.update(cs.bound)
                rec(c, cs)
            else:
                rec(c, scope)

    for kind, node, _, _ in items:
        if kind != "func":
            continue
        s = Scope(node, None)
        collect_bindings(node, s)
        names.update(s.bound)
        rec(node, s)
    return names


# ---------------------------------------------------------------- scope 解析
class Scope:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        self.bound = set()      # この scope でローカル束縛される名前
        self.globals_ = set()   # global 宣言された名前

    def is_function_like(self):
        return isinstance(
            self.node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
             ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp),
        )


def _scope_children(node):
    """直下の子ノードのうち、新しい scope を作るものと作らないものを返す。"""
    return isinstance(
        node,
        (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
         ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp),
    )


def collect_bindings(scope_node, scope):
    """scope 直属の束縛名・global宣言を収集 (ネストした scope の中身は見ない)。"""
    if isinstance(scope_node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = scope_node.args
        for arg in (a.posonlyargs + a.args + a.kwonlyargs):
            scope.bound.add(arg.arg)
        if a.vararg:
            scope.bound.add(a.vararg.arg)
        if a.kwarg:
            scope.bound.add(a.kwarg.arg)
    if isinstance(scope_node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        for gen in scope_node.generators:
            for n in ast.walk(gen.target):
                if isinstance(n, ast.Name):
                    scope.bound.add(n.id)

    def walk(node):
        for child in ast.iter_child_nodes(node):
            if _scope_children(child):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    scope.bound.add(child.name)
                continue  # ネスト scope の中は別処理
            if isinstance(child, ast.Global):
                scope.globals_.update(child.names)
            elif isinstance(child, ast.Nonlocal):
                raise SystemExit(f"nonlocal は未対応: line {child.lineno}")
            elif isinstance(child, ast.Name) and isinstance(child.ctx, (ast.Store, ast.Del)):
                scope.bound.add(child.id)
            elif isinstance(child, ast.NamedExpr):
                if isinstance(child.target, ast.Name):
                    scope.bound.add(child.target.id)
                walk(child)
                continue
            elif isinstance(child, ast.ExceptHandler) and child.name:
                scope.bound.add(child.name)
            elif isinstance(child, (ast.Import, ast.ImportFrom)):
                for alias in child.names:
                    scope.bound.add((alias.asname or alias.name).split(".")[0])
            elif isinstance(child, ast.ClassDef):
                scope.bound.add(child.name)
                continue
            elif isinstance(child, ast.For):
                for n in ast.walk(child.target):
                    if isinstance(n, ast.Name):
                        scope.bound.add(n.id)
                walk(child)
                continue
            elif isinstance(child, ast.withitem) and child.optional_vars:
                for n in ast.walk(child.optional_vars):
                    if isinstance(n, ast.Name):
                        scope.bound.add(n.id)
            walk(child)

    walk(scope_node)
    # global 宣言された名前はローカル束縛ではない
    scope.bound -= scope.globals_


def resolves_to_global(name, scope):
    """scope チェーンを内→外に辿り、name がモジュールグローバルに解決されるか判定。"""
    s = scope
    while s is not None:
        if name in s.globals_:
            return True
        if s.is_function_like() and name in s.bound:
            return False
        s = s.parent
    return True


# ---------------------------------------------------------------- 書き換え収集
class Edit:
    __slots__ = ("lineno", "col", "end_col", "text", "orig")

    def __init__(self, lineno, col, end_col, text, orig):
        self.lineno, self.col, self.end_col, self.text, self.orig = (
            lineno, col, end_col, text, orig)


def collect_edits(func_node, state_vars, func_mod, current_mod, lines,
                  aliases, state_alias):
    """関数1つ分の書き換え (Edit) と削除すべき global 文の行範囲を返す。"""
    edits = []
    removals = []  # (start_lineno, end_lineno)

    def visit(node, scope):
        if _scope_children(node) and node is not scope.node:
            child_scope = Scope(node, scope)
            collect_bindings(node, child_scope)
            for c in ast.iter_child_nodes(node):
                visit(c, child_scope)
            return
        if isinstance(node, ast.Global):
            for nm in node.names:
                if nm not in state_vars:
                    raise SystemExit(
                        f"global 宣言に状態変数以外: {nm} line {node.lineno}")
            assert node.lineno == node.end_lineno, f"複数行 global: {node.lineno}"
            stripped = lines[node.lineno - 1].strip()
            assert stripped.startswith("global "), f"global 行に他要素: {node.lineno}"
            removals.append((node.lineno, node.end_lineno))
            return
        if isinstance(node, ast.Name):
            nm = node.id
            qual = None
            if nm in state_vars and resolves_to_global(nm, scope):
                qual = state_alias
            elif nm in func_mod and resolves_to_global(nm, scope):
                target = func_mod[nm]
                if target != current_mod:
                    # state モジュール所属関数 (py_getflag 等) も st 経由で参照
                    qual = state_alias if target == "state" else aliases[target]
            if qual:
                # 位置整合性チェック (col_offset は UTF-8 バイトオフセット)
                raw = lines[node.lineno - 1].encode("utf-8")
                seg = raw[node.col_offset:node.end_col_offset].decode("utf-8")
                assert seg == nm, (
                    f"位置不一致 line {node.lineno}: expected {nm!r} got {seg!r}")
                assert node.lineno == node.end_lineno
                edits.append(Edit(node.lineno, node.col_offset,
                                  node.end_col_offset, f"{qual}.{nm}", nm))
        for c in ast.iter_child_nodes(node):
            visit(c, scope)

    top_scope = Scope(func_node, None)
    collect_bindings(func_node, top_scope)
    for c in ast.iter_child_nodes(func_node):
        visit(c, top_scope)
    return edits, removals


def apply_edits(lines, edits, removals):
    """lines (1-origin list のコピー) に編集を適用し、行リストを返す。"""
    out = list(lines)
    by_line = {}
    for e in edits:
        by_line.setdefault(e.lineno, []).append(e)
    for ln, es in by_line.items():
        raw = out[ln - 1].encode("utf-8")  # col は UTF-8 バイトオフセット
        for e in sorted(es, key=lambda e: -e.col):
            raw = raw[: e.col] + e.text.encode("utf-8") + raw[e.end_col:]
        out[ln - 1] = raw.decode("utf-8")
    dead = set()
    for a, b in removals:
        dead.update(range(a, b + 1))
    return [s for i, s in enumerate(out, 1) if i not in dead], dead


# ---------------------------------------------------------------- 解析
def parse_source():
    with open(SRC, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    return src, tree, lines


def top_level_layout(tree, nlines):
    """トップレベル文を分類し、(種別, node, seg_start, seg_end) を返す。
    seg_start は前の文の終端+1 (直前のコメント・空行を含む)。"""
    items = []
    prev_end = 0
    for node in tree.body:
        kind = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "func"
        elif isinstance(node, ast.If) and isinstance(node.test, ast.Compare) \
                and isinstance(node.test.left, ast.Name) \
                and node.test.left.id == "__name__":
            kind = "main"
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            kind = "import"
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            kind = "docstring"
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr)):
            kind = "data"
        else:
            raise SystemExit(f"未対応のトップレベル文: {ast.dump(node)[:80]} line {node.lineno}")
        items.append((kind, node, prev_end + 1, node.end_lineno))
        prev_end = node.end_lineno
    assert prev_end == nlines or all(
        not l.strip() or l.strip().startswith("#")
        for l in open(SRC, encoding="utf-8").readlines()[prev_end:])
    return items


def state_var_names(items):
    names = set()
    for kind, node, _, _ in items:
        if kind != "data":
            continue
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def load_map(path, items):
    with open(path, encoding="utf-8") as f:
        m = json.load(f)["modules"]
    func_mod = {}
    for mod, funcs in m.items():
        for fn in funcs:
            assert fn not in func_mod, f"重複: {fn}"
            func_mod[fn] = mod
    for fn in FORCE_STATE_FUNCS:
        func_mod[fn] = "state"
    defined = {n.name for k, n, _, _ in items if k == "func"}
    missing = defined - set(func_mod)
    extra = set(func_mod) - defined
    assert not missing, f"map に無い関数: {sorted(missing)}"
    assert not extra, f"存在しない関数: {sorted(extra)}"
    return func_mod


# ---------------------------------------------------------------- 生成
HEADER = '''# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — {desc} (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
'''

SHIM = '''# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot エントリポイント (本体は casino/ パッケージ)"""
from cs_runtime import Console
from casino.state import rand
from casino.app import Main

'''

MOD_DESC = {
    "state": "ゲーム状態 (旧グローバル変数)",
    "app": "メインフロー",
    "ui": "共通UI・演出",
    "slot_normal": "通常スロット",
    "vip": "VIPルーム",
    "underground": "地下カジノ",
    "persistence": "セーブ/ロード",
    "shop": "ショップ",
    "items": "装備アイテム",
    "missions": "ミッション",
    "stats": "ランキング・コレクション",
    "dream": "夢カジノ",
    "abandoned": "廃娯楽施設",
    "events": "ランダム・ストーリーイベント",
    "contracts": "悪魔契約",
    "addiction": "中毒システム",
    "endings": "エンディング",
    "devmode": "開発者モード",
}


def split(map_path, out_dir):
    src, tree, lines = parse_source()
    items = top_level_layout(tree, len(lines))
    svars = state_var_names(items)
    func_mod = load_map(map_path, items)
    mods = sorted(set(func_mod.values()) | {"state"})

    clash2 = svars & set(func_mod)
    assert not clash2, f"状態変数名と関数名が衝突: {clash2}"

    locals_all = all_local_names(items)
    aliases, state_alias = make_aliases(mods, svars, set(func_mod), locals_all)
    print(f"state alias: {state_alias}; aliased modules: "
          f"{ {m: a for m, a in aliases.items() if a != m} }")

    pieces = {m: [] for m in mods}
    main_block = None

    for kind, node, seg_a, seg_b in items:
        seg = lines[seg_a - 1: seg_b]
        if kind in ("import", "docstring"):
            continue  # 各モジュールのヘッダで再生成
        if kind == "main":
            main_block = "".join(seg)
            continue
        if kind == "data":
            # state.py へ原文移動 (コメント込み)。式中の関数参照は無いはず
            for n in ast.walk(node):
                if isinstance(n, ast.Name) and n.id in func_mod:
                    raise SystemExit(
                        f"トップレベル data が関数参照: {n.id} line {n.lineno}")
            pieces["state"].append("".join(seg))
            continue
        # func
        mod = func_mod[node.name]
        edits, removals = collect_edits(
            node, svars, func_mod, mod, lines, aliases, state_alias)
        new_seg, _ = apply_edits(seg, _shift(edits, seg_a), _shift_rm(removals, seg_a))
        pieces[mod].append("".join(new_seg))

    os.makedirs(out_dir, exist_ok=True)
    pkg = os.path.basename(out_dir)
    written = []
    for mod in mods:
        body = pieces[mod]
        if not body:
            continue
        text = "".join(body)
        head = HEADER.format(desc=MOD_DESC.get(mod, mod))
        imp = ""
        if mod != "state" and _uses(text, state_alias):
            imp += f"from . import state as {state_alias}\n"
        dep_lines = []
        for d in mods:
            if d == mod or d == "state":
                continue
            if _uses(text, aliases[d]):
                if aliases[d] == d:
                    dep_lines.append(d)
                else:
                    imp += f"from . import {d} as {aliases[d]}\n"
        if dep_lines:
            imp += f"from . import {', '.join(dep_lines)}\n"
        out = head + imp + "\n" + text
        path = os.path.join(out_dir, f"{mod}.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        written.append(path)

    with open(os.path.join(out_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write('"""FEWJSCasinoSlot パッケージ"""\n')

    # エントリシム
    assert main_block, "__main__ ブロックが見つからない"
    with open(os.path.join(os.path.dirname(out_dir), "casino_slot.py"),
              "w", encoding="utf-8") as f:
        f.write(SHIM + main_block)
    print(f"生成: {len(written)} modules -> {out_dir}/, shim -> casino_slot.py")
    for p in written:
        with open(p, encoding="utf-8") as fh:
            n = sum(1 for _ in fh)
        print(f"  {os.path.basename(p):20s} {n:6d} lines")


def _shift(edits, seg_start):
    for e in edits:
        e.lineno -= seg_start - 1
    return edits


def _shift_rm(removals, seg_start):
    return [(a - seg_start + 1, b - seg_start + 1) for a, b in removals]


def _uses(text, mod):
    import re
    return re.search(rf"(?<![\w.]){re.escape(mod)}\.", text) is not None


# ---------------------------------------------------------------- 検証
class Fold(ast.NodeTransformer):
    """st.x -> x / mod.F -> F に畳み込み、global 文を除去して正規化。"""

    def __init__(self, svars, func_mod, alias2mod, state_alias):
        self.svars, self.func_mod = svars, func_mod
        self.alias2mod, self.state_alias = alias2mod, state_alias

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            base, attr = node.value.id, node.attr
            if base == self.state_alias and (
                    attr in self.svars or self.func_mod.get(attr) == "state"):
                return ast.copy_location(ast.Name(id=attr, ctx=node.ctx), node)
            mod = self.alias2mod.get(base)
            if mod and self.func_mod.get(attr) == mod:
                return ast.copy_location(ast.Name(id=attr, ctx=node.ctx), node)
        return node


class StripGlobal(ast.NodeTransformer):
    def visit_Global(self, node):
        return None


def _dump(node):
    return ast.dump(node, include_attributes=False)


def verify(map_path, out_dir):
    src, tree, lines = parse_source()
    items = top_level_layout(tree, len(lines))
    svars = state_var_names(items)
    func_mod = load_map(map_path, items)
    mods = sorted(set(func_mod.values()) | {"state"})
    locals_all = all_local_names(items)
    aliases, state_alias = make_aliases(mods, svars, set(func_mod), locals_all)
    alias2mod = {a: m for m, a in aliases.items()}

    orig_funcs = {n.name: n for k, n, _, _ in items if k == "func"}
    orig_data = [_dump(n) for k, n, _, _ in items if k == "data"]

    new_funcs = {}
    new_data = []
    for mod in sorted(mods):
        path = os.path.join(out_dir, f"{mod}.py")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            mtree = ast.parse(f.read())
        for node in mtree.body:
            if isinstance(node, ast.FunctionDef):
                assert func_mod.get(node.name) == mod, \
                    f"{node.name} が {mod} にあるが map では {func_mod.get(node.name)}"
                new_funcs[node.name] = node
            elif mod == "state" and isinstance(
                    node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr)):
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                    continue  # docstring
                new_data.append(_dump(node))

    missing = set(orig_funcs) - set(new_funcs)
    assert not missing, f"生成漏れ: {sorted(missing)}"

    fold = Fold(svars, func_mod, alias2mod, state_alias)
    bad = []
    for name, onode in orig_funcs.items():
        o = StripGlobal().visit(ast.parse(ast.unparse(onode)))
        n = fold.visit(ast.parse(ast.unparse(new_funcs[name])))
        if _dump(o) != _dump(n):
            bad.append(name)
    # state.py の data 文 (extend 呼び出し含む) 原文一致
    data_ok = orig_data == new_data
    print(f"関数AST等価: {len(orig_funcs) - len(bad)}/{len(orig_funcs)}")
    if bad:
        print("不一致:", bad[:20])
    print(f"state data 一致: {data_ok} ({len(orig_data)} vs {len(new_data)})")
    if bad or not data_ok:
        sys.exit(1)
    print("VERIFY OK")


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = dict(zip(sys.argv[2::2], sys.argv[3::2]))
    map_path = args.get("--map", "refactor/module_map.json")
    out_dir = args.get("--out", "casino")
    if cmd == "split":
        split(map_path, out_dir)
    elif cmd == "verify":
        verify(map_path, out_dir)
    else:
        raise SystemExit("usage: transform.py split|verify --map X --out Y")
