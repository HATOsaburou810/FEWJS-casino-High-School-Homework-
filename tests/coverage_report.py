# カバレッジ集計: COV=1 で記録した .cov ファイル群を module_map.json と突き合わせ、
# モジュール別の実行済み/未実行関数を表示する。
# usage: COV=1 bash tests/run_characterization.sh check && python3 tests/coverage_report.py
import json
import glob
import os
import sys

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mm = json.load(open(os.path.join(repo, "refactor/module_map.json"), encoding="utf-8"))

covered = set()
src = sys.argv[1] if len(sys.argv) > 1 else "tests/current"
for p in glob.glob(os.path.join(repo, src, "*.cov")):
    covered.update(l.strip() for l in open(p, encoding="utf-8") if l.strip())

total_all = done_all = 0
for mod, funcs in sorted(mm["modules"].items()):
    done = [f for f in funcs if f in covered]
    miss = [f for f in funcs if f not in covered]
    total_all += len(funcs)
    done_all += len(done)
    bar = "#" * (len(done) * 20 // max(1, len(funcs)))
    print(f"{mod:14s} {len(done):3d}/{len(funcs):3d} [{bar:<20s}]")
    if miss and "-v" in sys.argv:
        print("   miss:", ", ".join(miss))
print(f"{'TOTAL':14s} {done_all:3d}/{total_all:3d}")
