# -*- coding: utf-8 -*-
"""Characterization-test driver for casino_slot.py.

Run as a subprocess:

    python3 tests/driver.py <workdir> <state_out_json>

- <workdir>:    cwd the game runs under (isolates relative "saves/" and
                "rankings.txt"). Must already exist.
- <state_out>:  path the final-state JSON snapshot is written to.

Keys are fed via stdin (a pipe). time.sleep is patched to a no-op,
DateTime.Now is frozen, and the RNG is seeded so transcripts are
deterministic and byte-identical across runs.

Refactor-proofing: the driver only depends on
  * casino_slot.Main         (entry point)
  * casino_slot.rand          (RNG wrapper, seeded via rand._r)
  * module globals            (state snapshot)
and, if present, a casino.state module (preferred snapshot source).
No other internal function names are referenced.
"""
import sys
import os
import json
import time
import types
import datetime as _real_datetime


_FREEZE_ISO_ENV = os.environ.get("FREEZE_ISO", "2026-01-01T12:00:00")
FROZEN = _real_datetime.datetime.fromisoformat(_FREEZE_ISO_ENV)
SEED = 12345


def _freeze_datetime(cs_runtime):
    """Replace cs_runtime._dt with a shim whose datetime.now() is fixed.

    cs_runtime's DateTime / _DT look up the module global _dt at call
    time, so swapping cs_runtime._dt freezes every Now / default-now path
    (DateTime(), _DT.Now, AddDays, etc.) while preserving timedelta and the
    rest of the datetime API.
    """

    class _FrozenDateTime(_real_datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return FROZEN

    class _DtShim(types.ModuleType):
        pass

    shim = _DtShim("datetime")
    shim.datetime = _FrozenDateTime
    shim.timedelta = _real_datetime.timedelta
    shim.date = _real_datetime.date
    shim.time = _real_datetime.time
    shim.tzinfo = _real_datetime.tzinfo
    shim.timezone = _real_datetime.timezone
    shim.MINYEAR = _real_datetime.MINYEAR
    shim.MAXYEAR = _real_datetime.MAXYEAR
    cs_runtime._dt = shim
    return shim


def _verify_frozen(cs_runtime):
    got = cs_runtime.DateTimeNS.Now._dt
    if not (got == FROZEN):
        raise AssertionError("DateTime freeze failed: " + repr(got)
                             + " vs " + repr(FROZEN))
    if not (cs_runtime.DateTime()._dt == FROZEN):
        raise AssertionError("DateTime() default-now not frozen")


def _collect_state(casino_slot):
    """Return the serializable state snapshot.

    Prefer a casino.state module if importable (post-refactor layout);
    otherwise fall back to casino_slot module globals. Collects only
    int/bool/str/list/dict attributes, dropping callables, classes,
    modules and the symbols reel-art constant.
    """
    source = casino_slot
    try:
        import importlib
        state_mod = importlib.import_module("casino.state")
        source = state_mod
    except Exception:
        source = casino_slot

    snapshot = {}
    for name in dir(source):
        if name.startswith("__"):
            continue
        if name == "symbols":
            continue
        try:
            val = getattr(source, name)
        except Exception:
            continue
        if isinstance(val, (int, bool, str, list, dict)):
            snapshot[name] = val
    return snapshot


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("usage: driver.py <workdir> <state_out>\n")
        return 2
    workdir = os.path.abspath(sys.argv[1])
    state_out = os.path.abspath(sys.argv[2])

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    os.makedirs(workdir, exist_ok=True)
    os.chdir(workdir)

    time.sleep = lambda *a, **k: None

    # EOF 後に cs_runtime が Enter を返し続けて無限ループするのを防ぐ:
    # キーが尽きたら read(1) が EOFError を投げる stdin ラッパに差し替える
    class _EofStdin:
        def __init__(self, real):
            self._real = real

        def read(self, n=-1):
            data = self._real.read(n)
            if data == "":
                raise EOFError("scenario keys exhausted")
            return data

        def readline(self, *a):
            data = self._real.readline(*a)
            if data == "":
                raise EOFError("scenario keys exhausted")
            return data

        def fileno(self):
            return self._real.fileno()

        def __getattr__(self, name):
            return getattr(self._real, name)

    sys.stdin = _EofStdin(sys.stdin)

    import cs_runtime
    _freeze_datetime(cs_runtime)
    _verify_frozen(cs_runtime)

    # sentinel バイトを F5/F9 ConsoleKeyInfo にマップ
    # gen_keys.py は \x0f=F5, \x1c=F9 を .keys ファイルに埋め込む
    _SENTINEL_F5 = "\x0f"
    _SENTINEL_F9 = "\x1c"
    _orig_read_key_raw = cs_runtime._read_key_raw
    def _sentinel_read_key_raw():
        ki = _orig_read_key_raw()
        if ki.KeyChar == _SENTINEL_F5:
            return cs_runtime.ConsoleKeyInfo("\x00", cs_runtime.ConsoleKey.F5)
        if ki.KeyChar == _SENTINEL_F9:
            return cs_runtime.ConsoleKeyInfo("\x00", cs_runtime.ConsoleKey.F9)
        return ki
    cs_runtime._read_key_raw = _sentinel_read_key_raw

    import casino_slot
    casino_slot.rand._r.seed(SEED)

    # COV=1 のとき、実行されたゲーム関数名を <state_out>.cov に記録する
    # (カバレッジ把握用。転写・状態の比較対象には含めない)
    covered = set()
    if os.environ.get("COV"):
        pkg_dir = os.path.join(repo_root, "casino") + os.sep

        def _prof(frame, event, arg):
            if event == "call":
                fn = frame.f_code.co_filename
                if fn.startswith(pkg_dir) or os.path.basename(fn) == "casino_slot.py":
                    covered.add(frame.f_code.co_name)

        sys.setprofile(_prof)

    try:
        casino_slot.Main()
    except (KeyboardInterrupt, EOFError, SystemExit):
        pass
    except Exception as exc:
        sys.stderr.write("[driver] Main() raised "
                         + type(exc).__name__ + ": " + str(exc) + "\n")
    finally:
        sys.setprofile(None)
    if os.environ.get("COV"):
        with open(state_out + ".cov", "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(covered)) + "\n")

    snapshot = _collect_state(casino_slot)

    def _stable(o):
        # repr(obj) はメモリアドレスを含み実行毎に変わるため、
        # __dict__ を持つオブジェクトは中身で安定的に表現する
        if callable(o):
            return "<fn:" + getattr(o, "__name__", "?") + ">"
        d = getattr(o, "__dict__", None)
        if d:
            out = {"__class__": type(o).__name__}
            out.update(d)
            return out
        return str(o)

    with open(state_out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2,
                  sort_keys=True, default=_stable)
    return 0


if __name__ == "__main__":
    sys.exit(main())
