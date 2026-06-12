# -*- coding: utf-8 -*-
"""アニメーション描画関数のスナップショットテスト。

ゲームプレイ経由では特定の出目 (777等) が必要で到達しにくい描画関数を
直接呼び出し、stdout をバイト単位でベースラインと比較できる形で出力する。
重複コード統合リファクタの回帰検証が主目的。

usage: python3 tests/test_animations.py <out_file>
"""
import sys
import os
import io
import time
import types
import shutil
import contextlib
import datetime as rdt

FROZEN = rdt.datetime(2026, 1, 1, 12, 0, 0)
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo)
time.sleep = lambda *a, **k: None

import cs_runtime
from cs_runtime import ConsoleColor

# 出力先は chdir 前の cwd 基準で解決する
OUT_PATH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None

# ファイル書き込み (SaveRanking 等) を隔離するため scratch ディレクトリで実行
# 追記型の rankings.txt が残ると実行毎に状態が変わるため毎回作り直す
_scratch = os.path.join(repo, "tests", "_scratch_anim")
shutil.rmtree(_scratch, ignore_errors=True)
os.makedirs(_scratch, exist_ok=True)
os.chdir(_scratch)


class _FD(rdt.datetime):
    @classmethod
    def now(cls, tz=None):
        return FROZEN


_sh = types.ModuleType("datetime")
for _a in ("timedelta", "date", "time", "tzinfo", "timezone", "MINYEAR", "MAXYEAR"):
    setattr(_sh, _a, getattr(rdt, _a))
_sh.datetime = _FD
cs_runtime._dt = _sh
# 万一 ReadKey を呼ぶ関数があっても決定論的に進むように
cs_runtime._read_key_raw = lambda: cs_runtime._make_keyinfo(".")
# ReadLine を呼ぶ対象 (夢カジノ層の選択肢など) には常に "1" を返す
cs_runtime.Console.ReadLine = lambda: "1"

import casino.state as st
from casino import slot_normal, vip, underground, ui, addiction, dream, endings, abandoned

TARGETS = [
    ("DrawTitle", lambda: ui.DrawTitle()),
    ("DrawReels(7,7,7)", lambda: ui.DrawReels([7, 7, 7])),
    ("DrawReels(0,1,2)", lambda: ui.DrawReels([0, 1, 2])),
    ("MegaWinAnimation", lambda: slot_normal.MegaWinAnimation("+7770G")),
    ("BigWinAnimation", lambda: slot_normal.BigWinAnimation("+600G")),
    ("SmallWinAnimation", lambda: slot_normal.SmallWinAnimation("+150G")),
    ("LoseAnimation", lambda: slot_normal.LoseAnimation()),
    ("ReachEffect", lambda: slot_normal.ReachEffect([6, 6, 1])),
    ("GodModeActivation", lambda: slot_normal.GodModeActivation()),
    ("LuckyTimeActivation", lambda: slot_normal.LuckyTimeActivation()),
    ("FreezeEffect", lambda: slot_normal.FreezeEffect()),
    ("GreedRingMegaWinAnimation", lambda: slot_normal.GreedRingMegaWinAnimation("+9990G")),
    ("GreedRingBigWinAnimation", lambda: slot_normal.GreedRingBigWinAnimation("+800G")),
    ("GreedRingSmallWinAnimation", lambda: slot_normal.GreedRingSmallWinAnimation("+200G")),
    ("GreedRingLoseAnimation", lambda: slot_normal.GreedRingLoseAnimation()),
    ("DrawVIPTitle", lambda: vip.DrawVIPTitle()),
    ("VIPMegaWinAnimation", lambda: vip.VIPMegaWinAnimation("+30000G")),
    ("VIPBigWinAnimation", lambda: vip.VIPBigWinAnimation("+5000G")),
    ("VIPSmallWinAnimation", lambda: vip.VIPSmallWinAnimation("+1500G")),
    ("VIPLoseAnimation", lambda: vip.VIPLoseAnimation()),
    ("VIPReachEffect", lambda: vip.VIPReachEffect([2, 2, 3])),
    ("DrawUndergroundTitle", lambda: underground.DrawUndergroundTitle()),
    ("UndergroundMegaWinAnimation", lambda: underground.UndergroundMegaWinAnimation("+50000G", 10)),
    ("UndergroundBigWinAnimation", lambda: underground.UndergroundBigWinAnimation("+5000G", 5)),
    ("UndergroundSmallWinAnimation", lambda: underground.UndergroundSmallWinAnimation("+750G")),
    ("UndergroundLoseAnimation(False)", lambda: underground.UndergroundLoseAnimation(False)),
    ("UndergroundLoseAnimation(True)", lambda: underground.UndergroundLoseAnimation(True)),
    # ---- グリッチ・汎用演出 ----
    ("GlitchText", lambda: ui.GlitchText("CASINO", ConsoleColor.Red)),
    ("ScreenGlitch", lambda: ui.ScreenGlitch(1)),
    ("JackpotGlitch", lambda: ui.JackpotGlitch()),
    ("SpinGlitch", lambda: ui.SpinGlitch()),
    ("MenuGlitch", lambda: ui.MenuGlitch()),
    ("TypeText", lambda: ui.TypeText("テスト")),
    # ---- 中毒演出 (addictionLevel=85 で発火条件を満たす) ----
    ("ShowAddictionMessage", lambda: (_set_addiction(85), addiction.ShowAddictionMessage())),
    ("AddictionHallucinationEffect", lambda: (_set_addiction(85), addiction.AddictionHallucinationEffect())),
    ("AddictionWaveEffect_Soft", lambda: addiction.AddictionWaveEffect_Soft()),
    ("AddictionWaveEffect_Break", lambda: addiction.AddictionWaveEffect_Break()),
    ("AddictionWaveEffect_Chaos", lambda: addiction.AddictionWaveEffect_Chaos()),
    # ---- 夢カジノ深層 (直接呼び出し; 選択肢 ReadLine は常に "1") ----
    ("DreamLayer2", lambda: dream.DreamLayer2()),
    ("DreamLayer3", lambda: dream.DreamLayer3()),
    ("DreamLayer4", lambda: dream.DreamLayer4()),
    ("DreamLayerFinal", lambda: dream.DreamLayerFinal()),
    ("MushroomManWaiting", lambda: dream.MushroomManWaiting()),
    # ---- エンディング群 (引数なし・描画+状態変更のみ) ----
    ("LaborEnding", lambda: endings.LaborEnding()),
    ("ExecutionEnding", lambda: endings.ExecutionEnding()),
    ("GreedRingBadEnding", lambda: endings.GreedRingBadEnding()),
    ("AddictionBadEnding", lambda: endings.AddictionBadEnding()),
    ("DevilContract1BadEnding", lambda: endings.DevilContract1BadEnding()),
    ("DevilContract2TimeUpEnding", lambda: endings.DevilContract2TimeUpEnding()),
    ("DevilContract1Success", lambda: endings.DevilContract1Success()),
    ("DevilContract2Success", lambda: endings.DevilContract2Success()),
    ("BloodAmuletBadEnding", lambda: endings.BloodAmuletBadEnding()),
    ("OverflowHiddenEnding", lambda: endings.OverflowHiddenEnding()),
    ("ShowCredits", lambda: endings.ShowCredits()),
    # ---- 未接続関数 (ゲーム本体から呼び出し箇所なし) ----
    # 3回振って表/裏の両分岐を踏む (seed 777 固定で決定論的)
    ("UnknownCoinFlip x3", lambda: [abandoned.UnknownCoinFlip(100, 2) for _ in range(3)]),
]


def _set_addiction(level):
    st.addictionLevel = level


def main():
    out_path = OUT_PATH
    chunks = []
    covered = set()
    pkg_dir = os.path.join(repo, "casino") + os.sep

    def _prof(frame, event, arg):
        if event == "call" and frame.f_code.co_filename.startswith(pkg_dir):
            covered.add(frame.f_code.co_name)

    for label, fn in TARGETS:
        st.rand._r.seed(777)  # 乱数を使う演出 (グリッチ等) も決定論化
        buf = io.StringIO()
        try:
            sys.setprofile(_prof)
            with contextlib.redirect_stdout(buf):
                fn()
            body = buf.getvalue()
        except Exception as e:
            body = f"<EXCEPTION {type(e).__name__}: {e}>\n"
        finally:
            sys.setprofile(None)
        chunks.append(f"##### {label}\n{body}\n")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(chunks))
    # カバレッジ集計 (COV=1 のとき driver.py と同様に .cov を出力し、
    # coverage_report.py が *.cov を合算する)
    if os.environ.get("COV") == "1":
        with open(out_path + ".cov", "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(covered)) + "\n")
    print(f"animations snapshot: {len(TARGETS)} targets -> {out_path}")


if __name__ == "__main__":
    main()
