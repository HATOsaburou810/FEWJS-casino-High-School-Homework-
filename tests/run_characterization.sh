#!/bin/bash
# 特性化テスト: リファクタリング前後で挙動がバイト単位で一致することを検証する。
#   tests/run_characterization.sh record   # ベースライン記録
#   tests/run_characterization.sh check    # 現行コードをベースラインと比較
#
# FREEZE_ISO: 時刻凍結 (デフォルト "2026-01-01T12:00:00")
#   シナリオ毎にオーバーライド可能 (case 文参照)
#   s8 (夢カジノ) は深夜条件 (hour>=22) のため 23:00 に固定
set -u
cd "$(dirname "$0")/.."
MODE="${1:-check}"
SCENARIOS="s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15"

case "$MODE" in
  record) DEST=tests/baseline ;;
  check)  DEST=tests/current ;;
  *) echo "usage: $0 record|check"; exit 2 ;;
esac

rm -rf "$DEST"
mkdir -p "$DEST"
FAIL=0

for s in $SCENARIOS; do
  work="$DEST/$s.work"
  mkdir -p "$work"
  # シナリオ毎の FREEZE_ISO を設定 (デフォルトは昼12時)
  unset FREEZE_ISO
  case "$s" in
    s8)  export FREEZE_ISO="2026-01-01T23:00:00" ;;  # 夢カジノ: 深夜条件 (hour>=22)
    s12) export FREEZE_ISO="2026-01-01T23:00:00" ;;  # 夢カジノ Layer2+: 深夜条件
  esac
  timeout 60 python3 tests/driver.py "$work" "$DEST/$s.state.json" \
    < "tests/scenarios/$s.keys" > "$DEST/$s.out" 2> "$DEST/$s.err"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "[$s] driver exit=$rc"; FAIL=1
  fi
done

# アニメーション直接スナップショット (777演出など、プレイ経由で到達困難な描画)
timeout 60 python3 tests/test_animations.py "$DEST/animations.out" > /dev/null 2>&1 \
  || { echo "[animations] snapshot failed"; FAIL=1; }

if [ "$MODE" = check ]; then
  if ! cmp -s tests/baseline/animations.out tests/current/animations.out; then
    echo "MISMATCH: animations.out"
    FAIL=1
  fi
  for s in $SCENARIOS; do
    for f in "$s.out" "$s.state.json"; do
      if ! cmp -s "tests/baseline/$f" "tests/current/$f"; then
        echo "MISMATCH: $f"
        diff <(tail -c 2000 "tests/baseline/$f") <(tail -c 2000 "tests/current/$f") | head -20
        FAIL=1
      fi
    done
    if ! diff -r "tests/baseline/$s.work" "tests/current/$s.work" > /dev/null 2>&1; then
      echo "MISMATCH: $s.work (saves/rankings)"
      diff -r "tests/baseline/$s.work" "tests/current/$s.work" | head -10
      FAIL=1
    fi
  done
  [ $FAIL -eq 0 ] && echo "CHECK OK: all scenarios byte-identical"
fi
[ "$MODE" = record ] && [ $FAIL -eq 0 ] && echo "RECORDED: $SCENARIOS"
exit $FAIL
