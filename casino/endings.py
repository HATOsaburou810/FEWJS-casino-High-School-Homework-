# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — エンディング (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod
from . import persistence

# ========== オーバーフロー隠しエンディング（超豪華版） ==========

def OverflowHiddenEnding():
    # RTA判定
    elapsed = DateTimeNS.Now - st.gameStartTime
    isRTA = elapsed.TotalSeconds <= 300
    st.overflowCleared = True
    if isRTA:
        st.rtaCleared = True
    # ============================================
    # フェーズ0: 予兆演出（新規追加）
    # ============================================
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n\n\n")
    Console.WriteLine(f"    所持金: {st.money:,}G")
    Thread.Sleep(1000)
    # 画面が少しずつおかしくなる
    for i in range(0, 3):
        Console.WriteLine("\n    .")
        Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    ...何かが...おかしい...")
    Thread.Sleep(2000)
    # ============================================
    # フェーズ1: 所持金表示の崩壊
    # ============================================
    Console.clear()
    for i in range(0, 20):
        Console.clear()
        # 色がおかしくなる
        Console.ForegroundColor = CONSOLE_COLOR_BY_INDEX(st.rand.Next(1, 16))
        Console.BackgroundColor =(ConsoleColor.Black if i % 4 == 0 else CONSOLE_COLOR_BY_INDEX(st.rand.Next(0, 16)))
        Console.WriteLine("\n\n\n")
        # 複数の所持金が同時表示
        glitchValues = [ st.money, st.money + st.rand.Next(-99999999, 99999999), -st.money, 2147483647, (-2147483648), st.rand.Next(0, 999999999) ]
        for val in sorted(glitchValues, key=lambda x: st.rand.Next()):
            Console.WriteLine(f"    所持金: {val:,}G")
        # ランダムなエラーメッセージ
        if i > 5:
            warnings = [ "WARNING: Value exceeds safe range", "CAUTION: Memory corruption detected", "ALERT: Integer overflow imminent", "ERROR: Boundary check failed", "CRITICAL: Stack integrity compromised" ]
            Console.WriteLine(f"\n    [{warnings[st.rand.Next(len(warnings))]}]")
        Thread.Sleep(100 + i * 10)
    # ============================================
    # フェーズ2: システムパニック
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Red
    panicMessages = [ "SYSTEM PANIC", "KERNEL PANIC", "FATAL ERROR", "UNRECOVERABLE ERROR", "CATASTROPHIC FAILURE" ]
    for i in range(0, 10):
        Console.clear()
        Console.WriteLine("\n\n\n")
        for msg in panicMessages:
            Console.ForegroundColor = CONSOLE_COLOR_BY_INDEX(st.rand.Next(9, 16))
            Console.WriteLine(f"    *** {msg} ***")
        Console.WriteLine(f"\n\n    OVERFLOW VALUE: {st.money}")
        Console.WriteLine(f"    MAX_INT: {2147483647}")
        Console.WriteLine(f"    DIFF: {st.money - 2147483647}")
        Thread.Sleep(150)
    # ============================================
    # フェーズ3: ブルースクリーン風演出
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Blue
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n")
    Console.WriteLine("    :(")
    Console.WriteLine()
    Console.WriteLine("    Your casino has run into a problem and needs to restart.")
    Console.WriteLine("    We're just collecting some error info, and then we'll restart")
    Console.WriteLine("    for you.")
    Thread.Sleep(3000)
    Console.WriteLine("\n    0% complete")
    Thread.Sleep(500)
    i = 0
    while i <= 100:
        if i > 100:
            i = 100
        Console.SetCursorPosition(4, Console.CursorTop)
        Console.Write(f"    {i}% complete")
        Thread.Sleep(100)
        i += st.rand.Next(1, 15)
    Thread.Sleep(1000)
    Console.WriteLine("\n\n\n    Technical details:")
    Console.WriteLine(f"    Stop code: MONEY_OVERFLOW_EXCEPTION")
    Console.WriteLine(f"    Failed component: SlotMachine.Money")
    Console.WriteLine(f"    Error value: 0x{st.money:X}")
    Thread.Sleep(3000)
    # ============================================
    # フェーズ4: マトリックス風データストリーム
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    for frame in range(0, 30):
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        for row in range(0, 15):
            Console.Write("    ")
            for col in range(0, 50):
                if st.rand.Next(100) < 30:
                    chars = list("01アイウエオカキクサシスセタチツテナニヌネハヒフヘマミムメヤユヨラリルレワヲン")
                    Console.Write(chars[st.rand.Next(len(chars))])
                else:
                    Console.Write(" ")
            Console.WriteLine()
        Thread.Sleep(100)
    # ============================================
    # フェーズ5: 謎の選択肢（UI完全崩壊版）
    # ============================================
    # 崩壊していくアニメーション
    normalUI = [ "    ┌────────────────────────────┐", "    │                            │", "    │         ？？？             │", "    │                            │", "    └────────────────────────────┘" ]
    glitchedUI = [ [ "    ┌─??─────??──────??─────────┐", "    │  ??        ??          ??  │", "    │      ？？？？？？？？      │", "    │  ??        ??          ??  │", "    └──??──────??───────??───────┘" ], [ "    ╔═??═════??══════??═════════╗", "    ║??╔═══╗??╔═══╗??╔═══╗??║", "    ║  ║？？║  ║？？║  ║？？║  ║", "    ║??╚═══╝??╚═══╝??╚═══╝??║", "    ╚══??══════??═══════??═════╝" ], [ "    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓", "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓", "    ▓░░░░？？？？？？？？░░░░░░▓", "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓", "    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓" ] ]
    for iteration in range(0, 15):
        Console.clear()
        Console.BackgroundColor =(ConsoleColor.DarkRed if iteration % 3 == 0 else ConsoleColor.Black)
        Console.ForegroundColor = CONSOLE_COLOR_BY_INDEX(st.rand.Next(1, 16))
        Console.WriteLine("\n\n\n")
        if iteration < 5:
            for line in normalUI:
                Console.WriteLine(line)
        else:
            ui = glitchedUI[st.rand.Next(len(glitchedUI))]
            for line in ui:
                Console.WriteLine(line)
        Console.WriteLine("\n\n")
        Console.ForegroundColor = ConsoleColor.Yellow
        prompts = [ "         [Enter] ？？？", "         [????] ???", "         [E̷n̷t̷e̷r̷] ？？？", "         [█████] ███", "         [UNKNOWN] UNKNOWN" ]
        Console.WriteLine(prompts[st.rand.Next(len(prompts))])
        Thread.Sleep(200)
    Console.ResetColor()
    Console.ReadKey(True)
    # ============================================
    # フェーズ6: 世界崩壊シーケンス
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    destructionMessages = [ "データベース接続...切断", "メモリ整合性...破損", "スタックフレーム...崩壊", "ヒープ領域...解放失敗", "レジスタ値...不正", "キャッシュライン...汚染", "パイプライン...ストール", "分岐予測...失敗", "TLB...フラッシュ", "ページテーブル...破損" ]
    for msg in destructionMessages:
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.Write(f"\n    {msg}")
        Thread.Sleep(300)
        for i in range(0, 3):
            Console.Write(".")
            Thread.Sleep(200)
        Console.ForegroundColor = ConsoleColor.Red
        Console.Write(" [FAILED]")
        Thread.Sleep(500)
    Thread.Sleep(2000)
    # ============================================
    # フェーズ7: カウントダウン
    # ============================================
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n\n")
    Console.WriteLine("    システム再起動まで...")
    Thread.Sleep(1500)
    for countdown in range(10, (0) - 1, -1):
        Console.clear()
        # カウントダウンのサイズと色を変化
        colors = [ ConsoleColor.Red, ConsoleColor.DarkRed, ConsoleColor.Yellow, ConsoleColor.DarkYellow, ConsoleColor.Magenta ]
        Console.ForegroundColor = colors[countdown % len(colors)]
        Console.WriteLine("\n\n\n\n")
        # 大きな数字をASCIIアートで表示
        digits = ui_mod.GetBigNumber(countdown)
        for line in digits:
            Console.WriteLine("         " + line)
        Thread.Sleep((500 if countdown <= 3 else 800))
    # ============================================
    # フェーズ8: ホワイトアウト
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.White
    Console.ForegroundColor = ConsoleColor.White
    for i in range(0, 30):
        Console.WriteLine()
    Thread.Sleep(2000)
    # ============================================
    # フェーズ9: 再起動（ゆっくり復帰）
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n\n\n\n\n\n")
    Thread.Sleep(2000)
    Console.Write("    .")
    Thread.Sleep(1000)
    Console.Write(".")
    Thread.Sleep(1000)
    Console.Write(".")
    Thread.Sleep(1500)
    Console.clear()
    Console.WriteLine("\n\n\n\n\n")
    Console.WriteLine("    起動中...")
    Thread.Sleep(2000)
    # ============================================
    # フェーズ10: システムメッセージ
    # ============================================
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    bootMessages = [ "BIOS Version 2.0.26.42", "Memory Test: OK", "CPU: Quantum Processor x64", "Loading Kernel...", "Initializing Casino System...", "Checking Integrity...", "Loading Player Data...", f"Player: {st.playerName}", "Anomaly Detected.", "Running Diagnostic..." ]
    Console.WriteLine("\n\n")
    for msg in bootMessages:
        Console.WriteLine(f"    {msg}")
        Thread.Sleep(400)
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n    DIAGNOSTIC RESULT:")
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine(f"    >>> OVERFLOW DETECTED: {st.money:,}G <<<")
    Thread.Sleep(2000)
    # ============================================
    # フェーズ11: メタメッセージ
    # ============================================
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n\n\n")
    ui_mod.TypewriterEffect("    想定外の富は、世界を壊した。", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    ――責任は取らない。", 50)
    Thread.Sleep(3000)
    Console.clear()
    Console.WriteLine("\n\n\n\n")
    ui_mod.TypewriterEffect("    だが、君は成し遂げた。", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    誰も到達しないと思われた領域に。", 50)
    Thread.Sleep(2500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    整数の限界を超えて。", 50)
    Thread.Sleep(2500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    システムの壁を突き破って。", 50)
    Thread.Sleep(3000)
    # ============================================
    # フェーズ12: クエスト達成（超豪華演出）
    # ============================================
    Console.clear()
    # パーティクル風演出
    for frame in range(0, 20):
        Console.clear()
        Console.BackgroundColor = ConsoleColor.Black
        # ランダムに星を散りばめる
        for i in range(0, 50):
            x = st.rand.Next(0, 50)
            y = st.rand.Next(0, 20)
            Console.SetCursorPosition(x, y)
            Console.ForegroundColor = CONSOLE_COLOR_BY_INDEX(st.rand.Next(9, 16))
            particles = [ "*", "✦", "✧", "◆", "◇", "○", "●" ]
            Console.Write(particles[st.rand.Next(len(particles))])
        Thread.Sleep(100)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    # メインタイトル表示
    for i in range(0, 5):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Yellow if i % 2 == 0 else ConsoleColor.White)
        Console.WriteLine("\n\n")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("    ━━                                      ━━")
        Console.WriteLine("    ━━      隠しクエスト達成！！！        ━━")
        Console.WriteLine("    ━━                                      ━━")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Thread.Sleep(300)
    Thread.Sleep(1000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ╔═══════════════════════════════════════════════════╗")
    Console.WriteLine("    ║                                                   ║")
    Console.WriteLine("    ║   🏆 「あぁーあ、開発者が見たら泣くぞ。       ║")
    Console.WriteLine("    ║              by開発者」                           ║")
    Console.WriteLine("    ║                                                   ║")
    Console.WriteLine("    ╚═══════════════════════════════════════════════════╝")
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("    達成情報:")
    Console.WriteLine(f"    ├─ 到達所持金: {st.money:,}G")
    Console.WriteLine(f"    ├─ 到達時間: {ui_mod.FormatTimeSpan(elapsed)}")
    Console.WriteLine(f"    ├─ 総回転数: {st.totalSpins}回")
    Console.WriteLine(f"    └─ 設定: {st.setting}")
    Thread.Sleep(3000)
    # ============================================
    # フェーズ13: RTA判定（超特別演出）
    # ============================================
    if isRTA:
        Thread.Sleep(1000)
        # 画面フラッシュ
        for i in range(0, 10):
            Console.BackgroundColor =(ConsoleColor.Magenta if i % 2 == 0 else ConsoleColor.Black)
            Console.clear()
            Thread.Sleep(100)
        Console.clear()
        Console.BackgroundColor = ConsoleColor.Black
        # 特別なアニメーション
        rtaArt = [ "    ██████╗ ████████╗ █████╗ ", "    ██╔══██╗╚══██╔══╝██╔══██╗", "    ██████╔╝   ██║   ███████║", "    ██╔══██╗   ██║   ██╔══██║", "    ██║  ██║   ██║   ██║  ██║", "    ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝" ]
        for frame in range(0, 8):
            Console.clear()
            Console.ForegroundColor = CONSOLE_COLOR_BY_INDEX(9 + (frame % 7))
            Console.WriteLine("\n\n")
            for line in rtaArt:
                Console.WriteLine(line)
            Thread.Sleep(200)
        Thread.Sleep(1000)
        # 虹色グラデーション演出
        Console.clear()
        rainbow = [ ConsoleColor.Red, ConsoleColor.DarkYellow, ConsoleColor.Yellow, ConsoleColor.Green, ConsoleColor.Cyan, ConsoleColor.Blue, ConsoleColor.Magenta ]
        for i in range(0, 3):
            for c in range(0, len(rainbow)):
                Console.clear()
                Console.ForegroundColor = rainbow[c]
                Console.WriteLine("\n\n")
                Console.WriteLine("    ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
                Console.WriteLine("    ★                                              ★")
                Console.WriteLine("    ★            RTA 達成！！！！！               ★")
                Console.WriteLine("    ★         5分以内到達成功！！！               ★")
                Console.WriteLine("    ★                                              ★")
                Console.WriteLine("    ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
                Thread.Sleep(150)
        Console.clear()
        Console.BackgroundColor = ConsoleColor.DarkMagenta
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ╔═════════════════════════════════════════════════╗")
        Console.WriteLine("    ║                                                 ║")
        Console.WriteLine("    ║        🏆🏆🏆 特別クエスト達成 🏆🏆🏆        ║")
        Console.WriteLine("    ║                                                 ║")
        Console.WriteLine("    ║              「  R  T  A  」                   ║")
        Console.WriteLine("    ║                                                 ║")
        Console.WriteLine("    ╚═════════════════════════════════════════════════╝")
        Console.BackgroundColor = ConsoleColor.Black
        Thread.Sleep(2000)
        Console.WriteLine("\n\n")
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("    ═══════════════════════════════════════")
        Console.WriteLine(f"         記録: {elapsed.Minutes:02d}:{elapsed.Seconds:02d}.{elapsed.Milliseconds:03d}")
        Console.WriteLine("    ═══════════════════════════════════════")
        Thread.Sleep(2000)
        Console.WriteLine("\n")
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("    ステータス: 🌟 LEGENDARY 🌟")
        Console.WriteLine("    称号: 「時間の支配者」")
        Console.WriteLine("    ランク: SSS+")
        Thread.Sleep(3000)
        # スペシャルメッセージ
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n\n\n\n")
        ui_mod.TypewriterEffect("    君は伝説となった。", 50)
        Thread.Sleep(2000)
        Console.WriteLine("\n")
        ui_mod.TypewriterEffect("    開発者の友人と同じ偉業を成し遂げた者として。", 50)
        Thread.Sleep(2500)
        Console.WriteLine("\n")
        ui_mod.TypewriterEffect("    5分でゲームを破壊した者として。", 50)
        Thread.Sleep(2500)
        Console.WriteLine("\n")
        ui_mod.TypewriterEffect("    その名は永遠に刻まれる。", 50)
        Thread.Sleep(3000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("              開発者からのメッセージ")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        Thread.Sleep(2000)
        Console.WriteLine("\n\n")
        Console.ForegroundColor = ConsoleColor.Yellow
        ui_mod.TypewriterEffect("    「まさか本当に5分で到達する人が", 40)
        Console.WriteLine()
        ui_mod.TypewriterEffect("     現れるとは思わなかった...」", 40)
        Thread.Sleep(2500)
        Console.WriteLine("\n")
        ui_mod.TypewriterEffect("    「友達がやった時は笑ってたけど、", 40)
        Console.WriteLine()
        ui_mod.TypewriterEffect("     君も同じことやるとは...」", 40)
        Thread.Sleep(2500)
        Console.WriteLine("\n")
        Console.ForegroundColor = ConsoleColor.Magenta
        ui_mod.TypewriterEffect("    「おめでとう。君は本物だ。」", 40)
        Thread.Sleep(3000)
    # ============================================
    # フェーズ14: 最終エンディング表示
    # ============================================
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    # 星空演出
    for frame in range(0, 30):
        if frame % 3 == 0:
            for i in range(0, 20):
                Console.SetCursorPosition(st.rand.Next(0, 60), st.rand.Next(0, 20))
                Console.ForegroundColor = ConsoleColor.White
                Console.Write("·")
        Thread.Sleep(100)
    Console.clear()
    # エンディングタイトル
    endingTitle = [ "    ═══════════════════════════════════════════", "                                               ", "              H I D D E N   E N D              ", "                                               ", "           - OVERFLOW ACHIEVED -               ", "                                               ", "    ═══════════════════════════════════════════" ]
    for line in endingTitle:
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine(line)
        Thread.Sleep(200)
    Thread.Sleep(2000)
    Console.WriteLine("\n\n")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("    ═══════════════════════════════════════════")
    Console.WriteLine("                 達成記録                    ")
    Console.WriteLine("    ═══════════════════════════════════════════")
    Console.WriteLine()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine(f"    プレイヤー名: {st.playerName}")
    Console.WriteLine(f"    最終所持金: {st.money:,}G")
    Console.WriteLine(f"    到達時間: {ui_mod.FormatTimeSpan(elapsed)}")
    Console.WriteLine(f"    総回転数: {st.totalSpins}回")
    Console.WriteLine(f"    777回数: {st.total777Count}回")
    Console.WriteLine(f"    最大連勝: {st.maxConsecutiveWins}回")
    if isRTA:
        Console.WriteLine()
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine(f"    ★ RTA記録: {elapsed.Minutes:02d}:{elapsed.Seconds:02d}.{elapsed.Milliseconds:03d} ★")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(5000)
    # ============================================
    # フェーズ15: 哲学的メッセージ
    # ============================================
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Gray
    Console.WriteLine("\n\n\n\n")
    ui_mod.TypewriterEffect("    システムには限界がある。", 40)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    だが、人の欲望には限界がない。", 40)
    Thread.Sleep(2500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    君はそれを証明した。", 40)
    Thread.Sleep(2500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    たとえ世界が壊れようとも。", 40)
    Thread.Sleep(3000)
    Thread.Sleep(2000)
    # イベント登録
    if not ("OVERFLOW END" in st.unlockedEvents):
        st.unlockedEvents.append("OVERFLOW END")
    if isRTA and not ("RTA達成" in st.unlockedEvents):
        st.unlockedEvents.append("RTA達成")
    st.metaEventCount = Math.Max(st.metaEventCount, 10)
    Thread.Sleep(3000)

def LaborEnding():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkBlue
    Console.WriteLine("\n\n黒服たちに連行される...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n\n")
    Console.WriteLine("     あなたは見知らぬ施設に連れてこられた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     過酷な労働が待っている...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     二度と自由な生活には戻れないだろう...")
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("              BAD END - 強制労働")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("BAD END" in st.unlockedEvents):
        st.unlockedEvents.append("BAD END")

def ExecutionEnding():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n黒服が静かに銃を取り出す...")
    Thread.Sleep(2000)
    Console.clear()
    Console.WriteLine("\n\n\n")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("     ================================")
    Console.WriteLine("          冷たい銃口が向けられた")
    Console.WriteLine("     ================================")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n     黒服「悪く思うなよ...」")
    Console.WriteLine("\n     銃口があなたのこめかみに押し当てられる...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n          カチッ...")
    Thread.Sleep(1500)
    Console.clear()
    Console.WriteLine("\n\n\n")
    Console.WriteLine("           パァンッ！！！")
    Thread.Sleep(1000)
    Console.clear()
    Console.WriteLine("\n\n\n")
    Console.WriteLine("     ================================")
    Console.WriteLine("              一発の銃声")
    Console.WriteLine("     ================================")
    Thread.Sleep(1500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n     あなたは崩れ落ちた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     意識が遠のいていく...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     ...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Black
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("              GAME OVER")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("GAME OVER" in st.unlockedEvents):
        st.unlockedEvents.append("GAME OVER")

def GreedRingBadEnding():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         強欲の代償")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n指輪が激しく輝き始めた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n黒い霧があなたを包み込む...")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n「...我が糧となれ...」")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("     あなたの魂は指輪に吸い込まれた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     強欲に溺れた者の末路...")
    Thread.Sleep(2000)
    Console.WriteLine("\n     二度と戻ることはない...")
    Thread.Sleep(3000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("          BAD END - 破滅への道")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("破滅への道" in st.unlockedEvents):
        st.unlockedEvents.append("破滅への道")
# ========== エンディング ==========

def AddictionBadEnding():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         中毒の末路")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    あなたは...もう止まれない...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    カジノから出ることができない...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    レバーを引き続ける...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    何日も...何週間も...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    体が...動かなくなった...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    意識が...薄れていく...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    ...")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("          BAD END - 中毒の虜")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("中毒の虜" in st.unlockedEvents):
        st.unlockedEvents.append("中毒の虜")
# ========== 悪魔契約1 BADエンディング ==========

def DevilContract1BadEnding():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         魂の回収")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n10回の勝利を果たした...")
    Thread.Sleep(2000)
    Console.WriteLine("\n...しかし...")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    悪魔「契約通り...魂を頂こう...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    体が...動かない...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    魂が...引き抜かれていく...")
    Thread.Sleep(2000)
    Console.clear()
    Console.WriteLine("\n\n\n    ...")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("          BAD END - 悪魔の契約")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("悪魔に魂を奪われる" in st.unlockedEvents):
        st.unlockedEvents.append("悪魔に魂を奪われる")
    ShowEnding()
# ========== 悪魔契約2 時間切れエンディング ==========

def DevilContract2TimeUpEnding():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         時間切れ")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n時計の音が止まった...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    悪魔「時間だ...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔「完済できなかったな...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔「契約通り...魂を頂く...」")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("          BAD END - 時間との取引失敗")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("時間切れ" in st.unlockedEvents):
        st.unlockedEvents.append("時間切れ")
    ShowEnding()
# ========== 悪魔契約1 成功 ==========

def DevilContract1Success():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkRed
    ui_mod.TypewriterEffect("    10回目の勝利の瞬間...", 60)
    Thread.Sleep(2000)
    Console.clear()
    for f in range(0, 5):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Red if f % 2 == 0 else ConsoleColor.DarkRed)
        Console.BackgroundColor =(ConsoleColor.Black if f % 2 == 0 else ConsoleColor.DarkRed)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("  ╔══════════════════════════════════════╗")
        Console.WriteLine("  ║                                      ║")
        Console.WriteLine("  ║    💀  魂の担保  達成  💀           ║")
        Console.WriteLine("  ║    10連勝 — 契約履行               ║")
        Console.WriteLine("  ║                                      ║")
        Console.WriteLine("  ╚══════════════════════════════════════╝")
        Console.ResetColor()
        Thread.Sleep(280)
    Thread.Sleep(800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    静寂...", 80)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    悪魔「...見事だ」", 60)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    悪魔「10連勝...約束は守られた」", 60)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    ui_mod.TypewriterEffect("    悪魔「だが...魂を返すとは言っていない」", 60)
    Thread.Sleep(3000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...笑い声が遠ざかる...", 60)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ★ 契約1「魂の担保」— 達成 ★")
    Console.WriteLine("    報酬 +5000G")
    Console.ResetColor()
    st.money += 5000
    Thread.Sleep(3000)
# ========== 悪魔契約2 成功 ==========

def DevilContract2Success():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★")
    Console.WriteLine("    ★                                ★")
    Console.WriteLine("    ★      借金完済成功！！！      ★")
    Console.WriteLine("    ★                                ★")
    Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    悪魔「...約束は守られた...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔「貴様は自由だ...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔の姿が消えていく...")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    ★ 悪魔との契約を成功させた！ ★")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("悪魔契約成功" in st.unlockedEvents):
        st.unlockedEvents.append("悪魔契約成功")
# ========== TRUEエンディング ==========

def TrueEnding():
    Console.clear()
    Thread.Sleep(1000)
    # フェーズ1: 異変
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    いつものように、カジノへ向かった", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    でも", 50)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    何かが違った", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ2: カジノの様子
    ui_mod.TypewriterEffect("    扉を開けると", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    カジノは静かだった", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    スロットの音も", 50)
    Thread.Sleep(800)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    客の声も", 50)
    Thread.Sleep(800)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    何もなかった", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ3: ベルとの再会
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("    カウンターに、ベルがいた", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    いつもと違った", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    笑っていなかった", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("    ベル「...来てくれたのね」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「このカジノ...来月で閉まるの」", 50)
    Thread.Sleep(2500)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ4: 真実
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    知らなかった", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    ずっと通っていたのに", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    気づかなかった", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("    ベル「オーナーが...去年死んだの」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「キノコみたいな帽子が好きな...変な人だったけど」", 50)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...優しい人だったわ」", 50)
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ4.5: キノコ男の正体
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    そういえば", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    夢の中にいた", 50)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    キノコの帽子の男", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("    ベル「...あの人ね」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「死ぬ前に...夢の中でだけ会いに来てくれてたの」", 50)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...あなたにも、会わせたかったのかもしれない」", 50)
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ5: 夢の種明かし
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    夢カジノのことを思い出した", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    あの声", 50)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    あの言葉", 50)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    全部", 50)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    ベルの記憶だったんだ", 50)
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("    ベル「...ずっとひとりだったの」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でも...あなたが来てくれた」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「それだけで...よかった」", 50)
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(500)
    # フェーズ6: 最後の選択
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    何か言おうとした", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    でも言葉が出なかった", 50)
    Thread.Sleep(1500)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    代わりに", 50)
    Thread.Sleep(1000)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    [1] スロットを回す")
    Console.WriteLine("    [2] 何も言わずに座る")
    Console.WriteLine("    [3] ベルの隣に立つ")
    Console.ResetColor()
    Console.ReadKey(True)
    # どれを選んでも同じ結末
    Console.clear()
    Thread.Sleep(500)
    # フェーズ7: エンディング
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("    2人で最後の夜を過ごした", 50)
    Thread.Sleep(2000)
    Console.WriteLine("\n")
    ui_mod.TypewriterEffect("    スロットの音だけが響いていた", 50)
    Thread.Sleep(2000)
    Console.clear()
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("    ベル「...また来てね♪」", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「待ってるから」", 50)
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(2000)
    # フェーズ8: タイトル表示
    for i in range(0, 5):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Cyan if i % 2 == 0 else ConsoleColor.White)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ═══════════════════════════════════════")
        Console.WriteLine("                                           ")
        Console.WriteLine("                 TRUE END                 ")
        Console.WriteLine("                                           ")
        Console.WriteLine("              - また来てね♪ -             ")
        Console.WriteLine("                                           ")
        Console.WriteLine("    ═══════════════════════════════════════")
        Console.ResetColor()
        Thread.Sleep(400)
    Thread.Sleep(3000)
    # 永続GOD MODE解放
    st.godModePermanent = True
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ★ 隠し要素解放 ★")
    Console.WriteLine("    「永続GOD MODE」が解放されました")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("TRUE END" in st.unlockedEvents):
        st.unlockedEvents.append("TRUE END")
    ShowEnding()

def ShowEnding():
    persistence.SaveRanking()
    Console.clear()
    playTime = DateTimeNS.Now - st.startTime
    if st.debt > 0:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ==============================")
        Console.WriteLine("              BAD  END")
        Console.WriteLine("    ==============================")
        Console.ResetColor()
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        if st.addictionLevel >= 80:
            ui_mod.TypewriterEffect(f"    {st.playerName}は気づけばまたカジノにいた", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    借金は膨れ上がり、止める気力もなかった", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    それでも、スロットのリールだけが輝いていた...", 50)
        elif st.devilContractActive:
            ui_mod.TypewriterEffect("    悪魔との契約は果たされなかった", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect(f"\n\n    {st.playerName}が支払うべきものは、お金ではなかった", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    ...代償は静かに、確実に回収された", 50)
        elif st.debt >= 20000:
            ui_mod.TypewriterEffect(f"    {st.playerName}の借金は限界を超えた", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    黒服たちが静かに近づいてきた...", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    カジノは今日も回り続ける", 50)
        else:
            ui_mod.TypewriterEffect(f"    {st.playerName}はカジノを後にした", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    借金だけが残った...", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    また来る気がした", 50)
        Console.ResetColor()
        Thread.Sleep(2500)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("    ベル「...また来てね♪」", 50)
        Thread.Sleep(1500)
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    ...小さな声だった", 50)
        Console.ResetColor()
        Thread.Sleep(3000)
    elif st.money >= 5000 and st.debt == 0:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★")
        Console.WriteLine("    ★                                ★")
        Console.WriteLine("    ★          GOOD  END             ★")
        Console.WriteLine("    ★                                ★")
        Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★")
        Console.ResetColor()
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        if st.total777Count >= 5:
            ui_mod.TypewriterEffect(f"    {st.playerName}は777を{st.total777Count}回揃えた", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    それは運なのか、才能なのか", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    本人にも、わからなかった...", 50)
        elif st.hasEverBorrowedMoney:
            ui_mod.TypewriterEffect(f"    {st.playerName}は借金を完済し、カジノを後にした", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    あの夜、全てを失いかけた記憶は", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    今でも、薄く残っている...", 50)
        else:
            ui_mod.TypewriterEffect(f"    {st.playerName}は大金を手に入れてカジノを後にした", 50)
            Thread.Sleep(2000)
            ui_mod.TypewriterEffect("\n\n    また来るだろう、という気がした", 50)
        Console.ResetColor()
        Thread.Sleep(2500)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Magenta
        ui_mod.TypewriterEffect("    帰り際、ベルが声をかけてきた", 50)
        Thread.Sleep(2000)
        Console.WriteLine("\n")
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("    ベル「おめでとう♪ よかったわね」", 50)
        Thread.Sleep(2000)
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
        Thread.Sleep(1500)
        Console.ForegroundColor = ConsoleColor.Cyan
        if st.addictionLevel >= 50:
            ui_mod.TypewriterEffect("\n\n    ベル「...でも、もう来ないでね♪」", 50)
        elif st.shopCloseWithoutBuyCount >= 20:
            ui_mod.TypewriterEffect("\n\n    ベル「...また来るでしょ。わかってる♪」", 50)
        else:
            ui_mod.TypewriterEffect("\n\n    ベル「...また来てね♪ 待ってるから」", 50)
        Thread.Sleep(3000)
        Console.ResetColor()
        Thread.Sleep(3000)
    else:
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ===============================")
        Console.WriteLine("             NORMAL END")
        Console.WriteLine("    ===============================")
        Console.ResetColor()
        Console.WriteLine(f"\n\n    {st.playerName}はカジノを後にした...")
        # ベルとの別れ
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Magenta
        ui_mod.TypewriterEffect("    出口に向かうと、ベルが手を振っていた", 50)
        Thread.Sleep(2000)
        Console.WriteLine("\n")
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("    ベル「またいつでも来てね♪」", 50)
        Thread.Sleep(2000)
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
        Thread.Sleep(1500)
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("\n\n    ベル「...待ってるから」", 50)
        Thread.Sleep(3000)
        Console.ResetColor()
        Thread.Sleep(3000)
    if st.money >= 100000 and st.total777Count >= 3 and playTime.Hours >= 3:
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    スロットが回る音...")
        Thread.Sleep(2000)
        Console.WriteLine("\n    ...デン")
        Thread.Sleep(2000)
        Console.WriteLine("\n    ...デン")
        Thread.Sleep(2000)
        Console.WriteLine("\n    ...デデン！")
        Thread.Sleep(2000)
        Console.WriteLine("\n    ...")
        Thread.Sleep(2000)
        Console.clear()
        Console.WriteLine(f"    俺は {st.playerName} ")
        Console.WriteLine("    伝説のスロッターだ！")
        Thread.Sleep(3000)
        Console.WriteLine("\n    777を3回も揃えた俺に")
        Console.WriteLine("    敵う奴なんていない！...と")
        Thread.Sleep(4000)
        Console.WriteLine("\n    思っていた時期が俺にもあった...")
        Thread.Sleep(4000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Gray
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ...なあ..おい")
        Thread.Sleep(3000)
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n    何だよ？")
        Thread.Sleep(2000)
        Console.WriteLine("\n    知らない男が話しかけてきた...")
        Thread.Sleep(3000)
        Console.ForegroundColor = ConsoleColor.Gray
        Console.WriteLine("\n    お前...とうとうココの禁忌に触れてなおかつ破った...")
        Thread.Sleep(4000)
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n    何のことだ？")
        Thread.Sleep(2000)
        Console.ForegroundColor = ConsoleColor.Gray
        Console.WriteLine("\n    ここはな...選ばれし者しか来てはいけない場所なんだよ...")
        Thread.Sleep(4000)
        Console.WriteLine("\n    お前はその資格がなかった...")
        Thread.Sleep(4000)
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n    そんなの関係ないだろ...")
        Thread.Sleep(3000)
        Console.ForegroundColor = ConsoleColor.Gray
        Console.WriteLine("\n    そうかもしれないな...")
        Thread.Sleep(3000)
        Console.WriteLine("\n    だがな...お前はもうここから出られない...")
        Thread.Sleep(4000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Gray
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ダッ..ダッ..")
        Thread.Sleep(2000)
        Console.clear()
        Console.WriteLine("黒服が現れた..!")
        Console.WriteLine("    奴を捕らえよ..!")
        Thread.Sleep(3000)
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n    くそっ..逃げるしかない！")
        Thread.Sleep(3000)
        Console.WriteLine(f"\n  {st.playerName}は今になって事態の深刻さに気づき ")
        Thread.Sleep(4000)
        Console.WriteLine("\n  さっきからずっと押していたボタンから手を放し、ここにきて席を立ったのだ...")
        Thread.Sleep(5000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ===============================")
        Console.WriteLine("          BAD? END?? - 永遠の迷宮")
        Console.WriteLine("    ===============================")
        Console.WriteLine("    逃亡生活は順調かな？")
        Console.ResetColor()
    ShowCredits()
    # ========== 統計画面（グラフ付き2カラム） ==========
    Console.clear()
    w = Math.Max(Console.WindowWidth, 80)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n  ╔══════════════════════════════════════════════════════════════════════════╗")
    Console.WriteLine("  ║                          P L A Y  S T A T S                            ║")
    Console.WriteLine("  ╚══════════════════════════════════════════════════════════════════════════╝")
    Console.ResetColor()
    # --- ヘルパー：バー計算はインライン ---
    # --- 左カラム：基本情報 ---
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐")
    Console.WriteLine("  │         基 本 情 報             │  │         戦 績 グ ラ フ          │")
    Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤")
    Console.ResetColor()
    # プレイヤー名・時間
    Console.Write(f"  │  プレイヤー: {st.playerName:<18} │  │  ")
    Console.ForegroundColor = ConsoleColor.Green
    Console.Write(f"所持金  ")
    Console.ResetColor()
    barLen = 20
    moneyBar = int(float(st.money) / Math.Max(st.maxMoney, 1000) * barLen)
    moneyBar = Math.Clamp(moneyBar, 0, barLen)
    Console.ForegroundColor =(ConsoleColor.Green if st.money >= 1000 else ConsoleColor.Red)
    Console.Write("[" + ("█" * (moneyBar)) + ("░" * (barLen - moneyBar)) + "]")
    Console.ResetColor()
    Console.WriteLine("  │")
    Console.Write(f"  │  プレイ時間: {ui_mod.FormatTimeSpan(playTime):<16} │  │  ")
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.Write(f"最高額  ")
    Console.ResetColor()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.Write("[" + ("█" * (barLen)) + "]")
    Console.ResetColor()
    Console.WriteLine(f" {st.maxMoney:>6}G│")
    Console.Write(f"  │  最終所持金: {st.money:>7,}G          │  │  ")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.Write(f"回転数  ")
    Console.ResetColor()
    spinBar = Math.Min(int(st.totalSpins * barLen / Math.Max(st.totalSpins, 100)), barLen)
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.Write("[" + ("█" * (spinBar)) + ("░" * (barLen - spinBar)) + "]")
    Console.ResetColor()
    Console.WriteLine(f"{st.totalSpins:>4}回 │")
    Console.Write(f"  │  最高所持金: {st.maxMoney:>7,}G          │  │  ")
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.Write(f"777回数 ")
    Console.ResetColor()
    bar777 = Math.Min(st.total777Count * 4, barLen)
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.Write("[" + ("█" * (bar777)) + ("░" * (barLen - bar777)) + "]")
    Console.ResetColor()
    Console.WriteLine(f"  x{st.total777Count:<3}  │")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤")
    Console.ResetColor()
    # 勝敗
    totalPlays = ((st.totalSpins) if st.totalWinAmount + st.totalLoseAmount > 0 else 1)
    Console.Write(f"  │  総回転数:   {st.totalSpins:>5}回            │  │  ")
    Console.ForegroundColor = ConsoleColor.Green
    Console.Write("獲得額  ")
    Console.ResetColor()
    winBar = (int(float(st.totalWinAmount) / (st.totalWinAmount + st.totalLoseAmount) * barLen) if st.totalWinAmount + st.totalLoseAmount > 0 else 0)
    winBar = Math.Clamp(winBar, 0, barLen)
    Console.ForegroundColor = ConsoleColor.Green
    Console.Write("[" + ("█" * (winBar)) + ("░" * (barLen - winBar)) + "]")
    Console.ResetColor()
    Console.WriteLine("  │")
    Console.Write(f"  │  777達成:    {st.total777Count:>5}回            │  │  ")
    Console.ForegroundColor = ConsoleColor.Red
    Console.Write("損失額  ")
    Console.ResetColor()
    loseBar = barLen - winBar
    Console.ForegroundColor = ConsoleColor.Red
    Console.Write("[" + ("█" * (loseBar)) + ("░" * (barLen - loseBar)) + "]")
    Console.ResetColor()
    Console.WriteLine("  │")
    Console.Write(f"  │  最大連勝:   {st.maxConsecutiveWins:>5}回            │  │  ")
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.Write("中毒度  ")
    Console.ResetColor()
    addBar = int(st.addictionLevel * barLen / 100)
    addColor = (ConsoleColor.Green if st.addictionLevel < 40 else (ConsoleColor.Yellow if st.addictionLevel < 70 else ConsoleColor.Red))
    Console.ForegroundColor = addColor
    Console.Write("[" + ("█" * (addBar)) + ("░" * (barLen - addBar)) + "]")
    Console.ResetColor()
    Console.WriteLine(f" {st.addictionLevel:>3}%  │")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤")
    Console.ResetColor()
    # 収支
    netProfit = st.money - 1000
    Console.Write(f"  │  総獲得額:  {st.totalWinAmount:>8,}G        │  │  ")
    if netProfit >= 0:
        Console.ForegroundColor = ConsoleColor.Green
        Console.Write(f"★ 純利益: +{netProfit:,}G")
    else:
        Console.ForegroundColor = ConsoleColor.Red
        Console.Write(f"▼ 純損失:  {-netProfit:,}G")
    Console.ResetColor()
    Console.WriteLine(("").ljust(int(Math.Max(0, 17 - len(str(netProfit))))) + "  │")
    Console.Write(f"  │  総損失額:  {st.totalLoseAmount:>8,}G        │  │  ")
    completedM = py_count_completed(st.missions)
    missionBar = (int(completedM * barLen / len(st.missions)) if len(st.missions) > 0 else 0)
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.Write(f"実績 [{('█' * (missionBar))}{('░' * (barLen - missionBar))}]")
    Console.ResetColor()
    Console.WriteLine("  │")
    Console.Write(f"  │  最大借金:  {st.maxDebt:>8,}G        │  │  ")
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.Write(f"  {completedM}/{len(st.missions)} ミッション達成")
    Console.ResetColor()
    Console.WriteLine("             │")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("  └─────────────────────────────────┘  └─────────────────────────────────┘")
    Console.ResetColor()
    # 解放コレクション
    Console.ForegroundColor = ConsoleColor.DarkYellow
    Console.WriteLine(f"\n  絵柄: {len(st.unlockedSymbols)}/8  │  イベント: {len(st.unlockedEvents)}種  │  VIP訪問: {st.vipTotalVisits}回  │  地下訪問: {st.undergroundVisits}回")
    Console.ResetColor()
    # 強欲の指輪情報
    if st.greedRingLoseCount > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"  強欲の指輪: 負け{st.greedRingLoseCount}回 / 総損失 {st.greedRingLoseCount * 500:,}G")
        Console.ResetColor()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n  何かキーを押してタイトルに戻る...")
    Console.ResetColor()
    Console.ReadKey(True)

def ShowCredits():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n\n")
    Console.WriteLine("         ━━━━━━━━━━━━━━━━━")
    Console.WriteLine("              STAFF ROLL")
    Console.WriteLine("         ━━━━━━━━━━━━━━━━━")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n         Game Director")
    Console.WriteLine("              Claude(AI)")
    Console.WriteLine("              Chisato Sugita")
    Console.WriteLine("              Rito Matsuhashi")
    Console.WriteLine("              Hinata Hase")
    Console.WriteLine("              Tomu Usui")
    Thread.Sleep(1500)
    Console.WriteLine("\n         Programming")
    Console.WriteLine("              C# / .NET")
    Thread.Sleep(1500)
    Console.WriteLine("\n         Special Thanks")
    Console.WriteLine("              Haru Setugetu")
    Thread.Sleep(1500)
    Console.WriteLine("\n\n━━━━━━━━━━━━━━━━━")
    Console.WriteLine("   _____                     ")
    Console.WriteLine("  |_   _|                    ")
    Console.WriteLine("    | |                      ")
    Console.WriteLine("    |_|hanks for playing      ")
    Console.WriteLine("\n\n━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(3000)
# ========== 血塗られたお守り BAD ENDING ==========

def BloodAmuletBadEnding():
    Console.clear()
    # 点滅演出
    for i in range(0, 5):
        Console.clear()
        Console.BackgroundColor =(ConsoleColor.DarkRed if i % 2 == 0 else ConsoleColor.Black)
        Console.ForegroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.Red)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸")
        Console.WriteLine("    🩸                          🩸")
        Console.WriteLine("    🩸    呪いの発動...      🩸")
        Console.WriteLine("    🩸                          🩸")
        Console.WriteLine("    🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸")
        Thread.Sleep(300)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    お守りから血が溢れ出す...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    それはあなたの体を包み込む...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    動けない...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    息ができない...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    血の呪いに飲み込まれた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    意識が...遠のく...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    ...")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("        ===============================")
    Console.WriteLine("          BAD END - 血の代償")
    Console.WriteLine("        ===============================")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("血の代償" in st.unlockedEvents):
        st.unlockedEvents.append("血の代償")
    ShowEnding()
