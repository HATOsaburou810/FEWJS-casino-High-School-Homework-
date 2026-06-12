# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — VIPルーム (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import missions as missions_mod
from . import ui as ui_mod
from . import abandoned, endings, events, items, shop, stats

# ========== VIPルーム解放イベント ==========

def VIPRoomUnlockEvent():
    Console.clear()
    for i in range(0, 5):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Magenta if i % 2 == 0 else ConsoleColor.White)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
        Console.WriteLine("    ♦                           ♦")
        Console.WriteLine("    ♦    VIPルーム 解放！！！   ♦")
        Console.WriteLine("    ♦                           ♦")
        Console.WriteLine("    ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
        Console.ResetColor()
        Thread.Sleep(300)
    Thread.Sleep(1000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    店員が近づいてきた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「お客様...所持金10000Gを突破されましたね」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「特別なお部屋へご案内いたします...」")
    Thread.Sleep(2000)
    Console.clear()
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    重厚な扉が開かれる...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    そこには豪華絢爛な空間が広がっていた")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n    ★★★ VIPルームが利用可能になりました！ ★★★")
    Console.ResetColor()
    Console.WriteLine("\n    ・通常の3倍の配当")
    Console.WriteLine("    ・高額ベット可能（500G/1000G/5000G）")
    Console.WriteLine("    ・専属ディーラーが対応")
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n    ⚠ ただし...連敗には気をつけて... ⚠")
    Console.ResetColor()
    Thread.Sleep(4000)
    # 中毒度増加
    if st.addictionLevel < 100:
        st.addictionLevel += st.rand.Next(1, 3)
        if st.addictionLevel > 100:
            st.addictionLevel = 100
# ========== VIPディーラー初対面 ==========

def VIPDealerFirstMeeting():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    美しい女性ディーラーが微笑んだ...")
    Thread.Sleep(2000)
    Console.WriteLine(f"\n    「初めまして、{st.playerName}様」")
    Thread.Sleep(2000)
    Console.WriteLine(f"\n    「私は{st.vipDealerName}」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「VIPルーム専属ディーラーです」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「ここでは...大きな幸運も...」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n    「...大きな不幸も訪れます」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n    「どうぞ...お楽しみください」")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("ミス・フォーチュン登場" in st.unlockedEvents):
        st.unlockedEvents.append("ミス・フォーチュン登場")
# ========== VIPルーム入退室 ==========

def EnterVIPRoom():
    if not st.hasSeenVIPDealer:
        VIPDealerFirstMeeting()
        st.hasSeenVIPDealer = True
    st.isInVIPRoom = True
    st.vipTotalVisits += 1
    st.vipConsecutiveLoses = 0
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ════════════════════════════════")
    Console.WriteLine("         VIPルームへようこそ")
    Console.WriteLine("    ════════════════════════════════")
    Console.ResetColor()
    Thread.Sleep(2000)

def ExitVIPRoom():
    st.isInVIPRoom = False
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    VIPルームを退室しました")
    Console.ResetColor()
    Thread.Sleep(1500)
# ========== VIPルームメインループ ==========

def VIPRoomLoop():
    EnterVIPRoom()
    while st.isInVIPRoom:
        if st.greedRingEquipped and st.debt >= 5000:
            endings.GreedRingBadEnding()
            return
        if st.money <= 0 and st.debt > 0:
            events.DebtCollectionEvent()
            return
        if st.debt > 0 and st.debtTurnsRemaining > 0:
            st.debtTurnsRemaining -= 1
            if st.debtTurnsRemaining == 0:
                Console.clear()
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n借金の期限が切れた...")
                Thread.Sleep(2000)
                Console.ResetColor()
                events.DebtCollectionEvent()
                return
        if st.vipConsecutiveLoses >= 3 and not st.undergroundUnlocked:
            VIPThreeLossEvent()
            st.vipConsecutiveLoses = 0
        if st.rand.Next(100) < 5:
            VIPRandomEvent()
        Console.clear()
        Console.BackgroundColor = ConsoleColor.DarkMagenta
        Console.ForegroundColor = ConsoleColor.White
        DrawVIPTitle()
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n♦♦♦ VIPルーム - {st.vipDealerName}が対応中 ♦♦♦")
        Console.ResetColor()
        if st.godMode and st.godModeRemaining > 0:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
            Console.ResetColor()
        if st.luckyTimeActive and st.luckyTimeRemaining > 0:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine(f"\n☆☆☆ ラッキータイム！残り{st.luckyTimeRemaining}回 ☆☆☆")
            Console.ResetColor()
        Console.WriteLine(f"\nプレイヤー: {st.playerName}")
        Console.WriteLine(f"所持金: {st.money}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            if st.debtTurnsRemaining > 0:
                Console.WriteLine(f"返済期限: あと{st.debtTurnsRemaining}回転")
            Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"\nVIP統計:")
        Console.WriteLine(f"  訪問回数: {st.vipTotalVisits}回")
        Console.WriteLine(f"  総回転数: {st.vipTotalSpins}回")
        Console.WriteLine(f"  勝利回数: {st.vipTotalWins}回")
        if st.vipConsecutiveLoses > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  連敗中: {st.vipConsecutiveLoses}回")
        Console.ResetColor()
        missions_mod.ShowUncompletedMissions()
        Console.WriteLine("\n┌────────────────────────────┐")
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("│  [1] 500G でプレイ        │")
        Console.WriteLine("│  [2] 1000G でプレイ       │")
        Console.WriteLine("│  [3] 5000G でプレイ       │")
        Console.ResetColor()
        if st.money < 500:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("│  [4] 借金する (500G)      │")
            Console.ResetColor()
        Console.WriteLine("│  [M] ミッション確認       │")
        Console.WriteLine("│  [S] ショップ             │")
        if st.abandonedCasinoUnlocked:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("│  [A] 廃娯楽施設           │")
            Console.ResetColor()
        Console.WriteLine("│  [E] 装備管理             │")
        Console.WriteLine("│  [X] VIP退室              │")
        Console.WriteLine("│  [0] ゲーム終了           │")
        Console.WriteLine("└────────────────────────────┘")
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
        if key.KeyChar == "m" or key.KeyChar == "M":
            missions_mod.ShowAllMissions()
            continue
        if key.KeyChar == "x" or key.KeyChar == "X":
            ExitVIPRoom()
            break
        if key.KeyChar == "0":
            st.isInVIPRoom = False
            return
        elif key.KeyChar == "1":
            bet = 500
        elif key.KeyChar == "2":
            bet = 1000
        elif key.KeyChar == "3":
            bet = 5000
        elif key.KeyChar == "4" and st.money < 500:
            events.BlackSuitArrival()
            st.money += 500
            st.debt += 500
            st.hasEverBorrowedMoney = True
            st.debtTurnsRemaining = 20
            if not ("黒服登場" in st.unlockedEvents):
                st.unlockedEvents.append("黒服登場")
            continue
        else:
            Console.WriteLine("\n正しい選択をしてください")
            Thread.Sleep(1000)
            continue
        if bet > st.money:
            Console.WriteLine("\n所持金不足！")
            Thread.Sleep(1500)
            continue
        VIPSpin(bet)
        Console.WriteLine("\n\n何かキーを押して続ける...")
        Console.ReadKey(True)
# ========== VIPスピン処理 ==========

def VIPSpin(bet):
    spinStartTime = DateTimeNS.Now
    st.money -= bet
    st.totalSpins += 1
    st.vipTotalSpins += 1
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkMagenta
    Console.ForegroundColor = ConsoleColor.White
    DrawVIPTitle()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine(f"\n♦♦♦ VIPルーム - ベット: {bet}G ♦♦♦")
    Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels([ 0, 1, 2 ])
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine(f"        ▼ {st.vipDealerName}がレバーを引く ▼")
    Console.ResetColor()
    Thread.Sleep(1000)
    for t in range(0, 20):
        reels = [ st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)) ]
        Console.clear()
        Console.BackgroundColor = ConsoleColor.DarkMagenta
        Console.ForegroundColor = ConsoleColor.White
        DrawVIPTitle()
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n♦♦♦ VIPルーム - ベット: {bet}G ♦♦♦")
        Console.ResetColor()
        Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            Console.ResetColor()
        Console.WriteLine("\n")
        Console.ForegroundColor =(ConsoleColor.Magenta if t % 2 == 0 else ConsoleColor.White)
        ui_mod.DrawReels(reels)
        Console.ResetColor()
        delay = (50 if t < 10 else 50 + (t - 10) * 30)
        Thread.Sleep(delay)
    result = ([0] * 3)
    luckBonus = 0
    if st.itemInventory["お守り"] > 0:
        luckBonus += 3
    if st.itemInventory["幸運のコイン"] > 0:
        luckBonus += 8
        st.itemInventory["幸運のコイン"] -= 1
    # 🆕 水晶玉予知
    if st.oracleBallPrediction >= 0:
        result[0] = st.oracleBallPrediction
        result[1] = st.oracleBallPrediction
        result[2] = st.oracleBallPrediction
        st.oracleBallPrediction = -1
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n🔮 予知通りの未来...！ 🔮")
        Console.ResetColor()
        Thread.Sleep(1500)
    else:
        luckyBonus = (10 if st.luckyTimeActive and st.luckyTimeRemaining > 0 else 0)
        settingBonus = st.setting * 1
        vipBonus = 8
        for i in range(0, 3):
            rnd = st.rand.Next(100)
            threshold777 = 6 + luckyBonus + settingBonus + luckBonus + vipBonus
            threshold0 = 18 + luckyBonus + settingBonus + luckBonus + vipBonus
            threshold1 = 30 + luckyBonus + settingBonus + luckBonus + vipBonus
            threshold4 = 45 + luckyBonus + settingBonus + luckBonus + vipBonus
            if rnd < threshold777:
                result[i] = 2
            elif rnd < threshold0:
                result[i] = 0
            elif rnd < threshold1:
                result[i] = 1
            elif rnd < threshold4:
                result[i] = 4
            else:
                result[i] = st.rand.Next(5, len(st.symbols))
    isReach = (result[0] == result[2] and result[0] != result[1]) and st.rand.Next(100) < 20
    if isReach:
        VIPReachEffect(result)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkMagenta
    Console.ForegroundColor = ConsoleColor.White
    DrawVIPTitle()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine(f"\n♦♦♦ VIPルーム - 結果 ♦♦♦")
    Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels(result)
    Thread.Sleep(800)
    Console.WriteLine("\n")
    winAmount = 0
    multiplier = 3
    if st.godMode and st.godModeRemaining > 0:
        multiplier *= 2
    if st.deathRingEquipped:
        multiplier *= 10
    isWin = False
    if result[0] == 2 and result[1] == 2 and result[2] == 2:
        winAmount = bet * 10 * multiplier
        isWin = True
        st.vip777Count += 1
        VIPMegaWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.bigWinCount += 1
        st.total777Count += 1
        st.vipTotalWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.vipConsecutiveLoses = 0
        st.totalLoses = 0
        if not ("VIP777" in st.unlockedEvents):
            st.unlockedEvents.append("VIP777")
        stats.UnlockSymbol()
    elif result[0] == result[1] and result[1] == result[2]:
        winAmount = bet * 5 * multiplier
        isWin = True
        VIPBigWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.vipTotalWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.vipConsecutiveLoses = 0
        st.totalLoses = 0
        if bet == 5000:
            st.vip5000BetWin = True
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        winAmount = bet * 2 * multiplier
        isWin = True
        VIPSmallWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.vipTotalWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.vipConsecutiveLoses = 0
        st.totalLoses = 0
    else:
        st.totalLoseAmount += bet
        VIPLoseAnimation()
        st.consecutiveWins = 0
        st.totalLoses += 1
        st.vipConsecutiveLoses += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses += 1
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine(f"\n🩸 血の呪い: {st.bloodAmuletLoses}/3回")
            Console.ResetColor()
            Thread.Sleep(1500)
            if st.bloodAmuletLoses >= 3:
                endings.BloodAmuletBadEnding()
                return
        if st.deathRingEquipped:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n💀 死神の呪い: -1000G")
            Console.ResetColor()
            Thread.Sleep(1500)
            if st.money >= 1000:
                st.money -= 1000
                st.totalLoseAmount += 1000
            else:
                shortage = 1000 - st.money
                st.totalLoseAmount += st.money
                st.money = 0
                st.debt += shortage
                st.hasEverBorrowedMoney = True
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n所持金不足...{shortage}Gが借金に追加された")
                Console.ResetColor()
                Thread.Sleep(2000)
    if st.devilContractActive and st.devilContractType == 1 and isWin:
        st.contract1WinCount += 1
        Console.ForegroundColor = ConsoleColor.DarkMagenta
        Console.WriteLine(f"\n😈 契約勝利: {st.contract1WinCount}/10回")
        Console.ResetColor()
        if st.contract1WinCount >= 10:
            st.contract1Complete = True
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n★ 10回勝利達成！次の回転で... ★")
            Console.ResetColor()
        Thread.Sleep(1500)
    if st.consecutiveWins > st.maxConsecutiveWins:
        st.maxConsecutiveWins = st.consecutiveWins
    if st.money > st.maxMoney:
        st.maxMoney = st.money
    if st.godMode and st.godModeRemaining > 0:
        st.godModeRemaining -= 1
        if st.godModeRemaining == 0:
            st.godMode = False
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("\n[GOD MODE 終了...]")
            Console.ResetColor()
            Thread.Sleep(1500)
    if st.luckyTimeActive and st.luckyTimeRemaining > 0:
        st.luckyTimeRemaining -= 1
        if st.luckyTimeRemaining == 0:
            st.luckyTimeActive = False
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("\n[ラッキータイム 終了...]")
            Console.ResetColor()
            Thread.Sleep(1500)
    if winAmount > 0 and st.rand.Next(100) < 60:
        winAmount = VIPDoubleUpChallenge(winAmount)
    # スピンごとの中毒度上昇（VIPは多め）
    if st.addictionLevel < 100:
        addIncrease = 2
        # VIP基本+2
        if bet >= 1000:
            addIncrease += 1
        # 高額ベットで+1
        if not isWin:
            addIncrease += 1
        # 負けで+1
        st.addictionLevel = Math.Min(100, st.addictionLevel + addIncrease)
    missions_mod.CheckMissions()
    if st.debt > 0 and winAmount > 0:
        Thread.Sleep(500)
        Console.WriteLine("\n")
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("借金を返済しますか？ [Y/N]")
        Console.ResetColor()
        repay = Console.ReadKey(True)
        if repay.Key == ConsoleKey.Y:
            repayAmount = Math.Min(st.money, st.debt)
            st.money -= repayAmount
            st.debt -= repayAmount
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine(f"\n{repayAmount}G返済しました！")
            Console.ResetColor()
            if st.debt == 0:
                st.debtTurnsRemaining = 0
                Console.WriteLine("\n借金完済！黒服たちが去っていった...")
                if not ("借金完済" in st.unlockedEvents):
                    st.unlockedEvents.append("借金完済")
            Thread.Sleep(1500)
# ========== VIP専用演出 ==========

def DrawVIPTitle():
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("╔═══════════════════════════════════╗")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("║      ♦♦ VIP ROOM ♦♦             ║")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("╚═══════════════════════════════════╝")
    Console.ResetColor()

def VIPMegaWinAnimation(amount):
    lines = [
        "  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦",
        "  ♦                                    ♦",
        f"  ♦    VIP 777大当たり！×30倍！     ♦",
        f"  ♦         {(amount).rjust(int(10))}           ♦",
        "  ♦                                    ♦",
        "  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦",
    ]
    ui_mod.FlashBlock(lines, 6, [ConsoleColor.Magenta, ConsoleColor.White], ConsoleColor.Magenta, 250, 150)

def VIPBigWinAnimation(amount):
    lines = [f"     ♦♦ VIP大当たり×15倍！{amount} ♦♦"]
    ui_mod.FlashBlock(lines, 4, [ConsoleColor.Magenta, ConsoleColor.Magenta], ConsoleColor.Magenta, 200, 150)

def VIPSmallWinAnimation(amount):
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine(f"        ♦ VIP当たり×6倍！{amount} ♦")
    Console.ResetColor()

def VIPLoseAnimation():
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("           × ハズレ… ×")
    Console.ResetColor()

def VIPReachEffect(result):
    Console.clear()
    DrawVIPTitle()
    Console.WriteLine("\n")
    tempResult = [ result[0], result[1], result[0] ]
    ui_mod.DrawReels(tempResult)
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n        ♦♦♦ VIPリーチ！！ ♦♦♦")
    Console.WriteLine(f"        {st.vipDealerName}が微笑んだ...")
    Console.ResetColor()
    Thread.Sleep(1500)
    for i in range(0, 12):
        tempResult[1] = st.rand.Next(len(st.symbols))
        Console.clear()
        DrawVIPTitle()
        Console.WriteLine("\n")
        ui_mod.DrawReels(tempResult)
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("\n        ♦♦♦ VIPリーチ！！ ♦♦♦")
        Console.WriteLine(f"        {st.vipDealerName}が微笑んだ...")
        Console.ResetColor()
        Thread.Sleep(120 + i * 40)

def VIPDoubleUpChallenge(winAmount):
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine(f"  {st.vipDealerName}のダブルアップ！")
    Console.WriteLine(f"  現在の獲得金: {winAmount}G")
    Console.WriteLine("  ━━━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("  成功で2倍、失敗で半分")
    Console.WriteLine("  挑戦しますか？ [Y/N]")
    Console.ResetColor()
    choice = Console.ReadKey(True)
    if choice.Key == ConsoleKey.Y:
        Console.WriteLine(f"\n\n  {st.vipDealerName}がカードを裏返す...")
        Thread.Sleep(1500)
        for i in range(0, 5):
            Console.Write(("\r  ♦ ハート " if i % 2 == 0 else "\r  ♠ スペード "))
            Thread.Sleep(300)
        success = st.rand.Next(2) == 0
        Thread.Sleep(500)
        Console.WriteLine()
        if success:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n  ★★★ 成功！2倍獲得！ ★★★")
            oldAmount = winAmount
            winAmount *= 2
            st.money += winAmount - oldAmount
            Console.WriteLine(f"  獲得金: {winAmount}G")
            Console.ResetColor()
        else:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n  × 失敗...半分に減った ×")
            oldAmount = winAmount
            winAmount //= 2
            st.money -= (oldAmount - winAmount)
            Console.WriteLine(f"  獲得金: {winAmount}G")
            Console.ResetColor()
        Thread.Sleep(2000)
    return winAmount
# ========== VIPイベント ==========

def VIPThreeLossEvent():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         VIP 3連敗ペナルティ")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine(f"\n\n    {st.vipDealerName}が近づいてきた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「お客様...運が悪いようですね」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...もっと刺激的な場所をご存知ですか？」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    彼女が手渡したのは黒い招待状だった")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n    『地下カジノへようこそ』")
    Console.ResetColor()
    Thread.Sleep(2000)
    st.undergroundUnlocked = True
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    ★★★ 地下カジノが解放されました ★★★")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("地下への招待" in st.unlockedEvents):
        st.unlockedEvents.append("地下への招待")

def VIPRandomEvent():
    eventType = st.rand.Next(5)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    _sw1 = eventType
    if _sw1 == 0:
        Console.WriteLine(f"    {st.vipDealerName}: 「今日の運勢は...まずまずですね」")
    elif _sw1 == 1:
        Console.WriteLine("    天井から豪華なシャンデリアが輝いている...")
    elif _sw1 == 2:
        Console.WriteLine("    他のVIP客が大勝ちして歓声を上げている")
    elif _sw1 == 3:
        Console.WriteLine(f"    {st.vipDealerName}が意味深に微笑んだ...")
    elif _sw1 == 4:
        Console.WriteLine("    監視カメラが静かにあなたを見ている...")
        if not ("監視カメラ" in st.unlockedEvents):
            st.unlockedEvents.append("監視カメラ")
    Console.ResetColor()
    Thread.Sleep(2500)
