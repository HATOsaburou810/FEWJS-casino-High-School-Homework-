# FEWJS Casino Slot (Python移植版)

C# コンソールゲームからの自動移植。`python3 casino_slot.py` で起動。

## 構成

```
casino_slot.py        エントリポイント (シム)
cs_runtime.py         C# Console API 互換ランタイム (Windows/macOS/Linux)
casino/
  state.py            全ゲーム状態 (旧グローバル変数 ~110個) + py_getflag/py_setflag
  app.py              Main / タイトル / GameLoop
  ui.py               汎用演出 (タイプライタ・グリッチ・リール描画)
  slot_normal.py      通常スロット (スピン・当選演出・GODモード)
  vip.py              VIPルーム
  underground.py      地下カジノ
  persistence.py      セーブ/ロード/ランキング永続化
  shop.py             ショップ (ベル)
  items.py            装備アイテム
  missions.py         ミッション
  stats.py            ランキング・コレクション表示
  dream.py            夢カジノ (キノコ男)
  abandoned.py        廃娯楽施設 (3フロア+地下)
  events.py           ランダム・ストーリーイベント
  contracts.py        悪魔契約
  addiction.py        中毒システム演出
  endings.py          各種エンディング
  devmode.py          開発者モード (タイトルで ` キー)
```

状態は `casino/state.py` のモジュール属性に集約され、各モジュールから
`from . import state as st` 経由で `st.money` のように参照する。

## テスト (特性化テスト)

決定論的シナリオ (乱数シード固定・時刻凍結・sleep無効) を再生し、
標準出力・最終状態・セーブファイルがベースラインとバイト一致することを検証する。

```bash
bash tests/run_characterization.sh check    # 変更後の検証 (これが通れば挙動同一)
bash tests/run_characterization.sh record   # ベースライン再記録 (意図的な挙動変更時のみ)
python3 tests/gen_keys.py s1                # シナリオキー列の再生成
COV=1 bash tests/run_characterization.sh check && python3 tests/coverage_report.py tests/current  # 関数カバレッジ
```

- s1: 通常スピン6回 → 終了
- s2: スピン22回 (オートセーブ発火) → ショップ → 終了
- s3: ミッション/コレクション/ランキング/装備画面 → スピン2回 → 終了
- s4: DevModeでVIP解放 → VIPルームでスピン4回 → 終了
- s5: DevModeで地下解放 → 地下カジノでスピン3回 (全財産含む) → 終了
- s6/s7: DevMode全機能・イベントギャラリー (TrueEnding含む)
- s8: 夢カジノ (FREEZE_ISO=23:00で深夜条件を満たす) → 第1層 → 覚醒
- s9: 廃娯楽施設 1F→2F→3F 全室+Final → 出口イベント → 退出
- s10: 悪魔契約1締結 + 呪いアイテム装備切替
- s11: セーブ/ロード/削除 (永続化往復)
- s12: 夢カジノ 第2層〜最終層 + キノコ男 (FREEZE_ISO=23:00)
- s13: ギャラリー経由 廃娯楽施設3F・地下室 (BasementEvent→黒服最終対決)・エンディングA/B
- s14: 中毒度90でのスピン (幻覚演出) + アイテム
- s15: DevModeメニュー網羅 + 隠しイベントギャラリー

加えて `tests/test_animations.py` が当選演出・グリッチ・中毒演出・夢カジノ深層・
エンディング群など55ターゲットを直接呼び出してスナップショット比較する
(プレイ経由では777等の出目や特定フラグが必要なため)。未接続の UnknownCoinFlip も
ここでカバーする。
関数カバレッジはシナリオ+スナップショット合算で 162/184 (未カバーは events/items/
underground の一部ランダムイベント等。`python3 tests/coverage_report.py tests/current -v` で一覧)。

時刻凍結はデフォルト 2026-01-01 12:00。`FREEZE_ISO` 環境変数でシナリオ毎に
変更できる (run_characterization.sh の case 文参照)。

## リファクタリング履歴

元は単一ファイル casino_slot.py (10,619行・グローバル変数~110個)。
`refactor/transform.py` が AST 位置情報ベースの機械変換で分割した
(コメント・整形は完全保存、関数ASTの等価性 184/184 を機械検証済み)。
分割の関数→モジュール対応は `refactor/module_map.json`。

2026-06-12 に静的解析 + シナリオ拡張で潜在バグ19件を修正済み
(LoadGame全壊・所持金マイナス化・float汚染・`ex.Message` 等。git log 参照)。
当選演出のFlash骨格は `ui.FlashBlock` に統合済み。

未カバー領域: DreamLayer2以降 (totalLoses>=3が必要)、廃カジノ3F、
エンディング群の大半、addiction演出。変更時は該当シナリオの追加を推奨。
