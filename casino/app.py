# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — メインフロー (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import missions as missions_mod
from . import ui as ui_mod
from . import underground as underground_mod
from . import vip as vip_mod
from . import abandoned, addiction, contracts, devmode, endings, events, items, persistence, shop, slot_normal, stats

# ========== TRUEエンディング条件チェック ==========

def CheckTrueEndCondition():
    return st.dreamLayerCleared >= 5  and st.hasEverBorrowedMoney  and st.debt == 0  and st.total777Count >= 3  and st.hasUsedRehab  and st.addictionLevel <= 50  and st.totalSpins >= 200
# 幸運のコイン累計購入数
# ========== 設定示唆演出 ==========

def ShowSettingSuggestion():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         今日の台の調子は...")
    Console.WriteLine("    ================================")
    Thread.Sleep(1500)
    suggestions = [ "起動音が普通だ...", "起動音が少し高い...", "起動音がやや高い！", "起動音が高い！！", "起動音がかなり高い！！！", "起動音が異常に高い！！！！" ]
    hints = [ "今日は渋そうだ...", "まあまあかな", "少し期待できるかも", "今日はいけるかもしれない！", "かなり良さそうだ！！", "これは...高設定の予感！？" ]
    Console.ForegroundColor = ConsoleColor.Yellow
    if st.setting < 1 or st.setting > 6:
        return
    # 安全ガード
    Console.WriteLine(f"\n    {suggestions[st.setting - 1]}")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine(f"\n    {hints[st.setting - 1]}")
    Thread.Sleep(1500)
    if st.setting == 6:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n    （これは...高設定の予感！？）")
        Console.ResetColor()
        Thread.Sleep(2000)
        if not ("設定6解放" in st.unlockedEvents):
            st.unlockedEvents.append("設定6解放")
    Console.ResetColor()
    Thread.Sleep(1000)

def Main():
    try:
        pass
    except Exception:
        pass
        # UTF-8が使えない環境でもエラーにならないように
    Console.CursorVisible = False
    st.itemInventory["お守り"] = 0
    st.itemInventory["幸運のコイン"] = 0
    st.itemInventory["返済猶予券"] = 0
    persistence.LoadRankings()
    while True:
        # ===== ゲーム変数リセット（タイトルに戻るたびに初期化） =====
        st.money = 1000
        st.debt = 0
        st.debtTurnsRemaining = 0
        st.addictionLevel = 0
        st.isAddicted = False
        st.addictionWarningCount = 0
        st.setting = 0
        st.godMode = False
        st.godModePermanent = False
        st.godModeRemaining = 0
        st.luckyTimeActive = False
        st.luckyTimeRemaining = 0
        st.consecutiveWins = 0
        st.consecutiveLosses = 0
        st.consecutiveHundredPlays = 0
        st.totalSpins = 0
        st.totalWinAmount = 0
        st.totalLoseAmount = 0
        st.totalLoses = 0
        st.bigWinCount = 0
        st.total777Count = 0
        st.maxConsecutiveWins = 0
        st.maxMoney = 1000
        st.maxDebt = 0
        st.hasSeenConversation = False
        st.hasSeenMysteriousWoman = False
        st.vipRoomUnlocked = False
        st.isInVIPRoom = False
        st.vipConsecutiveLoses = 0
        st.vip777Count = 0
        st.vip5000BetWin = False
        st.vipTotalVisits = 0
        st.vipTotalWins = 0
        st.vipTotalSpins = 0
        st.hasSeenVIPDealer = False
        st.undergroundUnlocked = False
        st.isInUnderground = False
        st.undergroundVisits = 0
        st.undergroundWins = 0
        st.undergroundAllInWin = False
        st.undergroundConsecutiveLoses = 0
        st.undergroundTotalSpins = 0
        st.undergroundCursedMode = False
        st.hasSeenUndergroundDealer = False
        st.dreamCasinoUnlocked = False
        st.dreamLayerCleared = 0
        st.mushroomManMet = False
        st.luckyCoinsTotal = 0
        st.devilContractOffered = False
        st.devilContractActive = False
        st.devilContractType = 0
        st.devilContractTurns = 0
        st.devilContractSuccess = False
        st.contract1Complete = False
        st.contract1WinCount = 0
        st.hasGreedRing = False
        st.greedRingEquipped = False
        st.greedRingLoseCount = 0
        st.totalLuckyCoinsPurchased = 0
        st.hasDevilCoin = False
        st.devilCoinCurse = 0
        st.devilCoinWin = False
        st.devilCoinActive = False
        st.hasBloodAmulet = False
        st.bloodAmuletLoses = 0
        st.bloodAmulet5Wins = 0
        st.bloodAmuletEquipped = False
        st.hasDeathRing = False
        st.deathRing10Wins = 0
        st.deathRingEquipped = False
        st.hasTimeClock = False
        st.timeClockEquipped = False
        st.hasOracleBall = False
        st.oracleBallPrediction = -1
        st.cursedItemCount = 0
        st.metaEventCount = 0
        st.trueEndingUnlocked = False
        st.hasEverBorrowedMoney = False
        st.hasUsedRehab = False
        st.shopVisitCount = 0
        st.shopCloseWithoutBuyCount = 0
        st.bellMetFirst = False
        st.missionOpenCount = 0
        st.autoSaveTurns = 0
        st.overflowCleared = False
        st.rtaCleared = False
        st.playerName = "プレイヤー"
        st.itemInventory["お守り"] = 0
        st.itemInventory["幸運のコイン"] = 0
        st.itemInventory["返済猶予券"] = 0
        st.unlockedSymbols.clear()
        st.unlockedSymbols.append("スライム")
        st.unlockedSymbols.append("ゴーレム")
        st.unlockedEvents.clear()
        st.missions.clear()
        st.rankings.clear()
        persistence.LoadRankings()
        ShowTitleScreen()
        # ロードされていない場合のみ名前入力
        if st.playerName == "プレイヤー":
            InputPlayerName()
        st.startTime = DateTimeNS.Now
        st.gameStartTime = DateTimeNS.Now
        # 新規ゲームの場合のみ
        if st.setting == 0:
            ShowLoadingScreen()
            st.setting = st.rand.Next(1, 7)
            ShowSettingSuggestion()
            missions_mod.InitializeMissions()
        GameLoop()
        endings.ShowEnding()
# ========== タイトル画面 ==========

def ShowTitleScreen():
    # ========== 電源投入点滅 ==========
    for i in range(0, 4):
        Console.clear()
        Console.BackgroundColor = ConsoleColor.White
        Console.ForegroundColor = ConsoleColor.Black
        Console.WriteLine("\n\n\n\n\n\n\n\n          ■")
        Console.ResetColor()
        Thread.Sleep(80)
        Console.clear()
        Thread.Sleep(60)
    # ========== 全色フラッシュ ==========
    flashColors = [ ConsoleColor.Red, ConsoleColor.Yellow, ConsoleColor.White, ConsoleColor.Cyan, ConsoleColor.Magenta, ConsoleColor.Green ]
    for c in flashColors:
        Console.clear()
        Console.BackgroundColor = c
        Console.Write((" " * (200)))
        Console.ResetColor()
        Thread.Sleep(80)
        Console.clear()
        Thread.Sleep(40)
    # ========== ロゴ1行ずつ降臨 ==========
    logoLines = [ "    ╔════════════════════════════════════════╗", "    ║                                        ║", "    ║   Future Electric Wonder Jackpot Slot  ║", "    ║              - 運命の賭け -            ║", "    ║                                        ║", "    ║             FINAL  EDITION             ║", "    ║                                        ║", "    ╚════════════════════════════════════════╝" ]
    Console.clear()
    Console.WriteLine("\n\n\n")
    for i in range(0, len(logoLines)):
        Console.ForegroundColor =(ConsoleColor.Yellow if i == 2 else (ConsoleColor.Cyan if i == 3 else (ConsoleColor.White if i == 5 else ConsoleColor.DarkYellow)))
        Console.WriteLine(logoLines[i])
        Thread.Sleep(120)
    Console.ResetColor()
    Thread.Sleep(400)
    # ========== ★ 7 7 7 ★ JACKPOT ★ 点滅 ==========
    jackpotLogo = [ "    ╔════════════════════════════════════════╗", "    ║                                        ║", "    ║   Future Electric Wonder Jackpot Slot  ║", "    ║              - 運命の賭け -            ║", "    ║                                        ║", "    ║             FINAL  EDITION             ║", "    ║                                        ║", "    ╚════════════════════════════════════════╝" ]
    for i in range(0, 6):
        Console.clear()
        Console.WriteLine("\n\n\n")
        # ロゴ再描画
        for li in range(0, len(jackpotLogo)):
            Console.ForegroundColor =(ConsoleColor.Yellow if li == 2 else (ConsoleColor.Cyan if li == 3 else (ConsoleColor.White if li == 5 else ConsoleColor.DarkYellow)))
            Console.WriteLine(jackpotLogo[li])
        Console.ResetColor()
        Console.WriteLine()
        Console.ForegroundColor =(ConsoleColor.Red if i % 2 == 0 else ConsoleColor.Yellow)
        Console.WriteLine("          ★  7  7  7  ★  JACKPOT  ★")
        Console.ResetColor()
        Thread.Sleep((280 if i < 5 else 500))
    # ========== メニュー項目タイプライター表示 ==========
    Console.WriteLine()
    menuItems = [ "\n          [Enter] 新規ゲーム", "          [L]     ロード", "          [D]     セーブデータ削除", "          [Q]     ゲーム終了" ]
    Console.ForegroundColor = ConsoleColor.Cyan
    for item in menuItems:
        for ch in item:
            Console.Write(ch)
            Thread.Sleep(25)
        Console.WriteLine()
    Console.ResetColor()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n\n          ©2025~2026 FEWJS Casino Corporation")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key == ConsoleKey.L:
        persistence.LoadMenu()
    elif key.Key == ConsoleKey.D:
        persistence.DeleteSaveMenu()
        ShowTitleScreen()
    elif key.Key == ConsoleKey.Q:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n\n\n          またいつか...")
        Console.ResetColor()
        Thread.Sleep(1500)
        raise SystemExit
    elif key.KeyChar == "`" or key.KeyChar == "~":
        # ===== DEV MODE 入口 =====
        devmode.DevModeEntry()
        ShowTitleScreen()
# ========== プレイヤー名入力 ==========

def InputPlayerName():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    あなたの名前を教えてください")
    Console.WriteLine("    （10文字以内、Enterで決定）")
    Console.ResetColor()
    Console.Write("\n    名前 > ")
    Console.CursorVisible = True
    input = coalesce(Console.ReadLine(), "")
    st.playerName = input
    Console.CursorVisible = False
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine(f"\n\n    ようこそ、{st.playerName}さん。")
    Console.WriteLine("    運命の扉が今、開かれる...")
    Console.ResetColor()
    Thread.Sleep(2500)
# ========== ローディング画面 ==========

def ShowLoadingScreen():
    reelSymbols = [ " 7 ", " ★ ", " ♦ ", " ♣ ", " ♠ ", " ♥ ", "BAR", " $ " ]
    # ========== リール回転演出（毎フレームClear再描画） ==========
    spinFrames = 32
    for frame in range(0, spinFrames):
        r1 = frame % len(reelSymbols)
        r2 = (frame + 2) % len(reelSymbols)
        r3 = (frame + 4) % len(reelSymbols)
        # 後半から順番に止まる
        if frame >= spinFrames - 8:
            r1 = 0
        if frame >= spinFrames - 4:
            r2 = 0
        if frame >= spinFrames - 1:
            r3 = 0
        c1 = (ConsoleColor.Yellow if r1 == 0 else ConsoleColor.White)
        c2 = (ConsoleColor.Yellow if r2 == 0 else ConsoleColor.White)
        c3 = (ConsoleColor.Yellow if r3 == 0 else ConsoleColor.White)
        Console.clear()
        Console.WriteLine("\n\n\n")
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("    ╔═══════════════════════════════════╗")
        Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║")
        Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣")
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.Write("    ║    ")
        Console.ForegroundColor = c1
        Console.Write(reelSymbols[r1])
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.Write("    ║    ")
        Console.ForegroundColor = c2
        Console.Write(reelSymbols[r2])
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.Write("    ║    ")
        Console.ForegroundColor = c3
        Console.Write(reelSymbols[r3])
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("    ║")
        Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝")
        Console.ResetColor()
        Thread.Sleep((55 if frame < 15 else (110 if frame < 25 else 190)))
    # ========== 7 7 7 ピタ止め点滅 ==========
    for blink in range(0, 7):
        Console.clear()
        Console.WriteLine("\n\n\n")
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("    ╔═══════════════════════════════════╗")
        Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║")
        Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣")
        Console.ForegroundColor =(ConsoleColor.Red if blink % 2 == 0 else ConsoleColor.Yellow)
        Console.WriteLine("    ║     7     ║     7     ║     7     ║")
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝")
        Console.ResetColor()
        Thread.Sleep(240)
    # ========== JACKPOT 確定表示 ==========
    Console.clear()
    Console.WriteLine("\n\n\n")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("    ╔═══════════════════════════════════╗")
    Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║")
    Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣")
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("    ║     7     ║     7     ║     7     ║")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝")
    Console.ResetColor()
    Thread.Sleep(400)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n      ★★★  J A C K P O T  ★★★")
    Console.ResetColor()
    Thread.Sleep(800)
    # ========== プログレスバー ==========
    Console.WriteLine()
    barWidth = 30
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.Write("    [")
    Console.ResetColor()
    for i in range(0, barWidth):
        Console.ForegroundColor =(ConsoleColor.Green if i < barWidth * 0.5 else (ConsoleColor.Yellow if i < barWidth * 0.8 else ConsoleColor.Cyan))
        Console.Write("█")
        Thread.Sleep(38)
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.Write("]")
    Console.ResetColor()
    # ========== カジノへようこそ ==========
    Console.WriteLine("\n")
    for c in "    カジノへようこそ。":
        Console.ForegroundColor = ConsoleColor.White
        Console.Write(c)
        Thread.Sleep(80)
    Console.ResetColor()
    Thread.Sleep(1500)
# ========== 設定示唆 ==========

def ChangeMachine():
    if st.money < 2000:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n所持金が足りません... (2000G必要)")
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n台を変えますか？ (2000G) [Y/N]")
    Console.ResetColor()
    confirm = Console.ReadKey(True)
    if confirm.Key != ConsoleKey.Y:
        return
    st.money -= 2000
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n    台を移動する...")
    Thread.Sleep(1500)
    # 設定6だけ少し優遇
    settingPool = [ 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6 ]
    st.setting = settingPool[st.rand.Next(len(settingPool))]
    # 起動音演出
    suggestions = [ "起動音が普通だ...", "起動音が少し高い...", "起動音がやや高い！", "起動音が高い！！", "起動音がかなり高い！！！", "起動音が異常に高い！！！！" ]
    Console.WriteLine(f"\n    {suggestions[st.setting - 1]}")
    Thread.Sleep(1500)
    if st.setting == 6:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n    （これは...高設定の予感！？）")
        Console.ResetColor()
        Thread.Sleep(2000)
        if not ("設定6解放" in st.unlockedEvents):
            st.unlockedEvents.append("設定6解放")
    Thread.Sleep(1500)
# ========== メインゲームループ ==========
# ========== GameLoop内、冒頭部分を修正 ==========

def GameLoop():
    while True:
        # 🆕 オーバーフローチェック（マイナス表示検出）
        # int型の限界を超えてマイナスになった場合
        # より確実なオーバーフロー検出
        if st.money < 0 or st.money >= 2147483647 - 10000:
            endings.OverflowHiddenEnding()
            break
        # godModePermanent有効時は常にGOD MODE維持
        if st.godModePermanent and not st.godMode:
            st.godMode = True
            st.godModeRemaining = 10
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n★ 永続GOD MODE 再発動！ ★")
            Console.ResetColor()
            Thread.Sleep(1500)
        # または、1億以上でも発動（安全装置）
        if st.money >= 100000000:
            endings.OverflowHiddenEnding()
            break
        # VIPルーム解放チェック
        if not st.vipRoomUnlocked and st.money >= 10000:
            vip_mod.VIPRoomUnlockEvent()
            st.vipRoomUnlocked = True
            if not ("VIPルーム解放" in st.unlockedEvents):
                st.unlockedEvents.append("VIPルーム解放")
        # GameLoop内に追加（VIP解放チェックの下）
        # 借金5000G以上で地下解放
        if not st.undergroundUnlocked and st.debt >= 5000:
            underground_mod.UndergroundUnlockByDebt()
            st.undergroundUnlocked = True
            if not ("地下カジノ解放" in st.unlockedEvents):
                st.unlockedEvents.append("地下カジノ解放")
        # GameLoop内、イベントチェック部分に追加
        # メタ演出1: セーブ削除の脅し
        if st.metaEventCount < 1 and st.totalSpins > 30 and st.rand.Next(500) == 0:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    ⚠⚠⚠ 警告 ⚠⚠⚠")
            Console.WriteLine("\n    セーブデータを削除しますか？")
            Console.WriteLine("\n    [Y] 削除する")
            Console.WriteLine("    [N] キャンセル")
            Console.ResetColor()
            metaKey = Console.ReadKey(True)
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n\n\n    ...冗談だよ")
            Console.WriteLine("\n    でも次は本当かもしれない")
            Console.ResetColor()
            Thread.Sleep(3000)
            st.metaEventCount += 1
            if not ("メタ演出1" in st.unlockedEvents):
                st.unlockedEvents.append("メタ演出1")
        # GameLoop内にこれがない
        if st.addictionLevel >= 100:
            endings.AddictionBadEnding()
            break
        # メタ演出2: フェイクエラー画面
        if st.metaEventCount >= 1 and st.metaEventCount < 2 and st.totalSpins > 50 and st.rand.Next(500) == 0:
            Console.clear()
            Console.BackgroundColor = ConsoleColor.Blue
            Console.ForegroundColor = ConsoleColor.White
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    :(")
            Console.WriteLine("\n    FEWJS_CASINO_CRITICAL_ERROR")
            Console.WriteLine("\n    問題が発生したため、ゲームを再起動します。")
            Console.WriteLine("    セーブデータは...保護されています。多分。")
            Thread.Sleep(3000)
            Console.WriteLine("\n\n    0% 回復中...")
            i = 0
            while i <= 100:
                if i > 100:
                    i = 100
                Console.SetCursorPosition(4, Console.CursorTop)
                Console.Write(f"    {i}% 回復中...")
                Thread.Sleep(80)
                i += st.rand.Next(3, 15)
            Thread.Sleep(1000)
            Console.BackgroundColor = ConsoleColor.Black
            Console.ResetColor()
            Console.clear()
            Console.WriteLine("\n\n    ...再起動完了")
            Console.WriteLine("\n    やっぱり冗談だよ")
            Thread.Sleep(2000)
            st.metaEventCount += 1
            if not ("メタ演出2" in st.unlockedEvents):
                st.unlockedEvents.append("メタ演出2")
        # メタ演出3: 実名呼び出し
        if st.metaEventCount >= 2 and st.metaEventCount < 3 and st.totalSpins > 70 and st.rand.Next(500) == 0:
            realName = py_username()
            Console.clear()
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    ...ねえ")
            Thread.Sleep(2000)
            Console.WriteLine(f"\n    {realName}さん")
            Thread.Sleep(2000)
            Console.WriteLine("\n    まだやめないの？")
            Thread.Sleep(2000)
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("\n\n    （あなたのPCのユーザー名から取得しました）")
            Console.ResetColor()
            Thread.Sleep(3000)
            st.metaEventCount += 1
            if not ("メタ演出3" in st.unlockedEvents):
                st.unlockedEvents.append("メタ演出3")
        # メタ演出4: カーソル異常
        if st.metaEventCount >= 3 and st.metaEventCount < 4 and st.totalSpins > 90 and st.rand.Next(500) == 0:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.White
            Console.WriteLine("\n\n\n    何かがおかしい...")
            Thread.Sleep(1500)
            # カーソルが暴れる
            Console.CursorVisible = True
            for i in range(0, 20):
                x = st.rand.Next(0, Console.WindowWidth - 1)
                y = st.rand.Next(0, Console.WindowHeight - 1)
                try:
                    Console.SetCursorPosition(x, y)
                except Exception:
                    pass
                Thread.Sleep(100)
            # カーソルが消える
            Console.CursorVisible = False
            Console.clear()
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.SetCursorPosition(0, 0)
            Console.WriteLine("\n\n\n    カーソルが...言うことを聞かない...")
            Thread.Sleep(2000)
            Console.WriteLine("\n    ...落ち着いた")
            Thread.Sleep(2000)
            Console.ResetColor()
            st.metaEventCount += 1
            if not ("メタ演出4" in st.unlockedEvents):
                st.unlockedEvents.append("メタ演出4")
        # メタ演出5: 時間逆行演出
        if st.metaEventCount >= 4 and st.metaEventCount < 5 and st.totalSpins > 110 and st.rand.Next(500) == 0:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.WriteLine("\n\n\n    時間が...")
            Thread.Sleep(1500)
            Console.WriteLine("\n    逆流している...")
            Thread.Sleep(1500)
            # 回転数が戻っていくように見せる
            for i in range(st.totalSpins, (st.totalSpins - 10) - 1, -1):
                Console.clear()
                Console.ForegroundColor = ConsoleColor.Cyan
                Console.WriteLine("\n\n\n")
                Console.WriteLine(f"    総回転数: {i}回")
                Console.WriteLine("\n    時間が巻き戻っている...")
                Thread.Sleep(200)
            Thread.Sleep(500)
            Console.clear()
            Console.ForegroundColor = ConsoleColor.White
            Console.WriteLine("\n\n\n    ...元に戻った")
            Console.WriteLine(f"\n    総回転数: {st.totalSpins}回")
            Console.WriteLine("\n    （回転数は実際には減っていません）")
            Console.ResetColor()
            Thread.Sleep(3000)
            st.metaEventCount += 1
            if not ("メタ演出5" in st.unlockedEvents):
                st.unlockedEvents.append("メタ演出5")
        # 中毒幻覚
        if st.addictionLevel >= 61 and st.rand.Next(100) < 10:
            addiction.AddictionHallucinationEffect()
        # 中毒メッセージ
        if st.addictionLevel >= 21 and st.rand.Next(100) < 15:
            addiction.ShowAddictionMessage()
        # 中毒度100でBAD END
        if st.addictionLevel >= 100:
            endings.AddictionBadEnding()
            break
        # 悪魔契約発動条件チェック
        if not st.devilContractOffered and not st.devilContractActive:
            if st.debt >= 10000 or st.totalLoses >= 50 or (st.undergroundTotalSpins > 0 and st.undergroundConsecutiveLoses >= 10):
                contracts.DevilContractOfferEvent()
                st.devilContractOffered = True
                if not ("悪魔の誘惑" in st.unlockedEvents):
                    st.unlockedEvents.append("悪魔の誘惑")
        # 契約1（魂の担保）処理
        if st.devilContractActive and st.devilContractType == 1:
            if st.contract1Complete:
                # 10連勝達成 → 成功演出
                endings.DevilContract1Success()
                st.devilContractActive = False
                st.devilContractSuccess = True
                if not ("悪魔契約成功" in st.unlockedEvents):
                    st.unlockedEvents.append("悪魔契約成功")
            elif st.consecutiveLosses >= 1 and st.contract1WinCount > 0:
                # 連勝が途切れた → BAD END
                endings.DevilContract1BadEnding()
                break
        # 契約2（時間との取引）処理
        if st.devilContractActive and st.devilContractType == 2:
            remaining = st.contract2Deadline - DateTimeNS.Now
            if remaining.TotalSeconds <= 0:
                endings.DevilContract2TimeUpEnding()
                break
            # 完済チェック
            if st.debt == 0:
                endings.DevilContract2Success()
                st.devilContractActive = False
                st.devilContractSuccess = True
        # 強欲の指輪装備中で借金5000G以上
        if st.greedRingEquipped and st.debt >= 5000:
            endings.GreedRingBadEnding()
            break
        # TRUEエンディングチェック
        if not st.trueEndingUnlocked and CheckTrueEndCondition():
            st.trueEndingUnlocked = True
            endings.TrueEnding()
            break
        # チャプター1：夢カジノ1層クリア後に解放
        if st.dreamLayerCleared >= 1 and not st.chapter1Seen:
            events.Chapter1_FirstConversation()
            st.chapter1Seen = True
        # 廃娯楽施設：チャプター1クリア後にショップ隠しページ解放通知（初回のみ）
        if st.chapter1Seen and not st.vanityKeyPurchased and not st.abandonedCasinoUnlocked and st.totalSpins > 0 and st.totalSpins % 10 == 0 and st.rand.Next(3) == 0:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            ui_mod.TypewriterEffect("\n\n    ベルのショップに　何か新しいページが...", 40)
            Console.ResetColor()
            Thread.Sleep(2000)
        if st.money <= 0 and st.debt > 0:
            events.DebtCollectionEvent()
            break
        if st.debt > 0 and st.debtTurnsRemaining > 0:
            st.debtTurnsRemaining -= 1
            if st.debtTurnsRemaining == 0:
                Console.clear()
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n借金の期限が切れた...")
                Thread.Sleep(2000)
                Console.ResetColor()
                events.DebtCollectionEvent()
                break
        # 借金最大値記録
        if st.debt > st.maxDebt:
            st.maxDebt = st.debt
        if not st.hasSeenConversation and st.rand.Next(100) < 8:
            events.RandomConversationEvent()
            st.hasSeenConversation = True
            if not ("謎のおじさん" in st.unlockedEvents):
                st.unlockedEvents.append("謎のおじさん")
        if not st.hasSeenMysteriousWoman and st.rand.Next(100) < 10 and st.totalSpins > 10:
            events.MysteriousWomanEvent()
            st.hasSeenMysteriousWoman = True
            if not ("ミステリアスなお姉さん" in st.unlockedEvents):
                st.unlockedEvents.append("ミステリアスなお姉さん")
        if st.rand.Next(2000) == 0 and st.totalSpins > 5 and not st.greedRingEquipped:
            events.Devilmonster()
            if not ("悪魔の怪物" in st.unlockedEvents):
                st.unlockedEvents.append("悪魔の怪物")
        if st.bigWinCount >= 3 and st.rand.Next(100) < 30 and not st.greedRingEquipped:
            events.BlackSuitWarningEvent()
            st.bigWinCount = 0
            if not ("黒服の警告" in st.unlockedEvents):
                st.unlockedEvents.append("黒服の警告")
        if st.greedRingEquipped and st.rand.Next(100) < 15:
            events.GreedWhisperEvent()
        Console.clear()
        if st.greedRingEquipped:
            Console.BackgroundColor = ConsoleColor.DarkRed
            Console.ForegroundColor = ConsoleColor.Black
        ui_mod.DrawTitle()
        if st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Red
            Console.BackgroundColor = ConsoleColor.Black
            Console.WriteLine(f"\n💀💀💀 強欲のオーラ 発動中 💀💀💀")
            Console.WriteLine(f"負け: -500G | 勝ち: ×5倍")
            Console.ResetColor()
        if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
            Console.ResetColor()
        if st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine(f"\n☆☆☆ ラッキータイム！残り{st.luckyTimeRemaining}回 ☆☆☆")
            Console.ResetColor()
        if st.addictionLevel >= 1:
            Console.Write("\n⚠ 中毒度: ")
            Console.Write(ui_mod.GetAddictionBar(st.addictionLevel))
            Console.ResetColor()
            Console.WriteLine(" ⚠")
        if st.hasTimeClock:
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.WriteLine(f"\n🕐 現在時刻: {DateTimeNS.Now:HH:mm}")
            Console.ResetColor()
        Console.WriteLine(f"\nプレイヤー: {st.playerName}")
        Console.WriteLine(f"所持金: {st.money}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            if st.debtTurnsRemaining > 0:
                Console.WriteLine(f"返済期限: あと{st.debtTurnsRemaining}回転")
            Console.ResetColor()
        if st.consecutiveHundredPlays > 0 and not st.godMode and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine(f"100G連続プレイ: {st.consecutiveHundredPlays}/20回")
            Console.ResetColor()
        missions_mod.ShowUncompletedMissions()
        Console.WriteLine("\n┌────────────────────────────┐")
        Console.WriteLine("│  [1] 50G でプレイ         │")
        Console.WriteLine("│  [2] 100G でプレイ        │")
        if st.money < 50:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("│  [3] 借金する (500G)      │")
            Console.ResetColor()
        if st.vipRoomUnlocked:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("│  [V] VIPルームへ          │")
            Console.ResetColor()
        if st.undergroundUnlocked:
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine("│  [U] 地下カジノへ         │")
            Console.ResetColor()
        # 🆕 悪魔契約メニュー追加
        if st.devilContractOffered and not st.devilContractActive:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("│  [D] 悪魔との契約...      │")
            Console.ResetColor()
        Console.WriteLine("│  [M] ミッション確認       │")
        Console.WriteLine("│  [S] ショップ             │")
        if st.abandonedCasinoUnlocked:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("│  [A] 廃娯楽施設           │")
            Console.ResetColor()
        Console.WriteLine("│  [E] 装備管理             │")
        Console.WriteLine("│  [R] ランキング           │")
        Console.WriteLine("│  [C] コレクション         │")
        Console.WriteLine("│  [T] 台を変える (2000G)   │")
        Console.WriteLine("│  [F5] セーブ              │")
        Console.WriteLine("│  [F9] ロード              │")
        Console.WriteLine("│  [0] 終了                 │")
        Console.WriteLine("└────────────────────────────┘")
        # メニューグリッチ（中毒度80%以上で低確率発動）
        ui_mod.MenuGlitch()
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        bet = 0
        if key.KeyChar == "s" or key.KeyChar == "S":
            shop.ShopMenu()
            continue
        if (key.KeyChar == "a" or key.KeyChar == "A") and st.abandonedCasinoUnlocked:
            abandoned.EnterAbandonedCasino()
            continue
        if key.KeyChar == "e" or key.KeyChar == "E":
            items.EquipmentMenu()
            continue
        if (key.KeyChar == "d" or key.KeyChar == "D") and st.devilContractOffered and not st.devilContractActive:
            contracts.DevilContractMenu()
            continue
        if key.KeyChar == "r" or key.KeyChar == "R":
            stats.ShowRankings()
            continue
        if key.KeyChar == "c" or key.KeyChar == "C":
            stats.ShowCollection()
            continue
        if key.KeyChar == "m" or key.KeyChar == "M":
            missions_mod.ShowAllMissions()
            continue
        if key.Key == ConsoleKey.F5:
            persistence.SaveMenu()
            continue
        if key.Key == ConsoleKey.F9:
            persistence.LoadMenu()
            continue
        if (key.KeyChar == "v" or key.KeyChar == "V") and st.vipRoomUnlocked:
            vip_mod.VIPRoomLoop()
            continue
        if (key.KeyChar == "u" or key.KeyChar == "U") and st.undergroundUnlocked:
            underground_mod.UndergroundLoop()
            continue
        if key.KeyChar == "t" or key.KeyChar == "T":
            ChangeMachine()
            continue
        if key.KeyChar == "0":
            # メタ演出6: 終了拒否強化
            if st.metaEventCount >= 5 and st.rand.Next(3) == 0:
                Console.clear()
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine("\n\n\n    終了？")
                Thread.Sleep(1500)
                Console.WriteLine("\n    ...できないよ")
                Thread.Sleep(1500)
                # フェイク終了処理
                Console.WriteLine("\n\n    終了中...")
                i = 0
                while i <= 100:
                    if i > 100:
                        i = 100
                    Console.Write(f"\r    [{i}%]")
                    Thread.Sleep(100)
                    i += st.rand.Next(5, 20)
                Thread.Sleep(500)
                Console.clear()
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("\n\n\n    ...やっぱりまだ終われない")
                Console.WriteLine("\n    もう1回だけ")
                Console.ResetColor()
                Thread.Sleep(2000)
                if not ("メタ演出6" in st.unlockedEvents):
                    st.unlockedEvents.append("メタ演出6")
                continue
            # 中毒度61以上で終了拒否（既存コード）
            if st.addictionLevel >= 61:
                confirmCount = (5 if st.addictionLevel >= 81 else 3)
                for i in range(0, confirmCount):
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.DarkRed
                    Console.WriteLine("\n\n本当にやめますか？ [Y/N]")
                    if st.addictionLevel >= 81:
                        Console.WriteLine("\n...やめられない...")
                        Console.WriteLine("...もう1回...")
                    Console.ResetColor()
                    confirm = Console.ReadKey(True)
                    if confirm.Key == ConsoleKey.Y:
                        if i == confirmCount - 1:
                            break
                    else:
                        continue
                if st.addictionLevel >= 81:
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.Red
                    Console.WriteLine("\n\n...もう1回だけ...")
                    Console.ResetColor()
                    Thread.Sleep(2000)
                    continue
            break
        elif key.KeyChar == "1":
            # 中毒度41以上で50Gベット不可
            if st.addictionLevel >= 41 and st.addictionLevel < 81:
                Console.clear()
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine("\n\n50Gじゃ...足りない...")
                Console.WriteLine("もっと...もっと賭けたい...")
                Console.ResetColor()
                Thread.Sleep(2000)
                continue
            bet = 50
            if not st.godMode and not st.greedRingEquipped:
                st.consecutiveHundredPlays = 0
        elif key.KeyChar == "2":
            # 中毒度81以上で自動的に100Gに変更
            if st.addictionLevel >= 81:
                Console.clear()
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n制御できない...")
                Console.WriteLine("100Gを賭けてしまう...")
                Console.ResetColor()
                Thread.Sleep(2000)
            bet = 100
            if not st.godMode and not st.greedRingEquipped:
                st.consecutiveHundredPlays += 1
                if st.consecutiveHundredPlays >= 20:
                    slot_normal.GodModeActivation()
                    st.consecutiveHundredPlays = 0
        elif key.KeyChar == "3" and st.money < 50:
            events.BlackSuitArrival()
            st.money += 500
            st.debt += 500
            st.hasEverBorrowedMoney = True
            st.debtTurnsRemaining = 20
            if not st.godMode and not st.greedRingEquipped:
                st.consecutiveHundredPlays = 0
            if not ("黒服登場" in st.unlockedEvents):
                st.unlockedEvents.append("黒服登場")
            continue
        else:
            Console.WriteLine("\n正しい選択をしてください")
            Thread.Sleep(1000)
            continue
        if bet > st.money:
            Console.WriteLine("\n所持金不足！借金しますか？")
            Thread.Sleep(1500)
            continue
        st.money -= bet
        st.totalSpins += 1
        # オートセーブ
        st.autoSaveTurns += 1
        if st.autoSaveTurns >= st.AUTO_SAVE_INTERVAL:
            try:
                persistence.SaveGame(0)
                st.autoSaveTurns = 0
            except Exception:
                pass
        if not st.luckyTimeActive and st.rand.Next(1000) < 5 and not st.greedRingEquipped:
            slot_normal.LuckyTimeActivation()
        # 通常スピン処理（既存コードと同じ）
        slot_normal.NormalSpin(bet)
        Console.WriteLine("\n\n何かキーを押して続ける...")
        Console.ReadKey(True)
