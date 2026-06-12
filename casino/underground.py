# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 地下カジノ (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import missions as missions_mod
from . import ui as ui_mod
from . import abandoned, endings, events, shop, stats

# ========== 地下カジノ（スタブ） ==========

def UndergroundUnlockByDebt():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         絶望の淵")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    黒服の一人が近づいてきた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「おい...借金が膨れ上がってるな」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...一か八かの勝負に出るか？」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    黒い招待状を手渡された")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Black
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n    『奈落の底へようこそ』")
    Console.ResetColor()
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    ★★★ 地下カジノが解放されました ★★★")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("絶望からの招待" in st.unlockedEvents):
        st.unlockedEvents.append("絶望からの招待")

def UndergroundDealerFirstMeeting():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    暗闇の中...仮面を被った男が現れた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「ようこそ...奈落へ...」")
    Thread.Sleep(2000)
    Console.WriteLine(f"\n    「私は{st.undergroundDealerName}」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「ここは...最後の賭場だ...」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n    「勝てば天国...負ければ...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...地獄だ」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n    仮面の奥から不気味な笑い声が聞こえた...")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("ダークロード登場" in st.unlockedEvents):
        st.unlockedEvents.append("ダークロード登場")

def EnterUnderground():
    if not st.hasSeenUndergroundDealer:
        UndergroundDealerFirstMeeting()
        st.hasSeenUndergroundDealer = True
    st.isInUnderground = True
    st.undergroundVisits += 1
    st.undergroundConsecutiveLoses = 0
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ════════════════════════════════")
    Console.WriteLine("         奈落へ...降りていく...")
    Console.WriteLine("    ════════════════════════════════")
    Thread.Sleep(2000)
    Console.WriteLine("\n    階段を降りるたびに空気が重くなる...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    血の匂いがする...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("          地下カジノ - 奈落")
    Console.WriteLine("    ================================")
    Console.ResetColor()
    Thread.Sleep(2000)

def ExitUnderground():
    st.isInUnderground = False
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    地下カジノを後にした...")
    Console.WriteLine("\n    生きて戻れた...それだけで奇跡だ...")
    Console.ResetColor()
    Thread.Sleep(2000)

def UndergroundLoop():
    EnterUnderground()
    while st.isInUnderground:
        # 強欲の指輪チェック
        if st.greedRingEquipped and st.debt >= 5000:
            endings.GreedRingBadEnding()
            return
        if st.money <= 0 and st.debt > 0:
            events.DebtCollectionEvent()
            return
        # 借金期限チェック
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
        # 地下5連敗で呪いモード（既存）
        if st.undergroundConsecutiveLoses >= 5:
            UndergroundCursedEvent()
            st.undergroundConsecutiveLoses = 0
        # ↓ 下に追加！勝利後に呪い解除
        if st.undergroundCursedMode and st.undergroundWins > 0 and st.rand.Next(3) == 0:
            st.undergroundCursedMode = False
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n\n\n    呪いが...解けた...")
            Console.WriteLine(f"\n    {st.undergroundDealerName}が舌打ちをした...")
            Console.ResetColor()
            Thread.Sleep(2500)
        # ランダムイベント
        if st.rand.Next(100) < 10:
            UndergroundRandomEvent()
        Console.clear()
        # 地下専用背景色
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.DarkRed
        DrawUndergroundTitle()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"\n🔥🔥🔥 地下カジノ - {st.undergroundDealerName}が見つめている 🔥🔥🔥")
        Console.ResetColor()
        if st.undergroundCursedMode:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("\n💀 呪いモード発動中 💀")
            Console.ResetColor()
        if st.godMode and st.godModeRemaining > 0:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
            Console.ResetColor()
        Console.WriteLine(f"\nプレイヤー: {st.playerName}")
        Console.WriteLine(f"所持金: {st.money}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            if st.debtTurnsRemaining > 0:
                Console.WriteLine(f"返済期限: あと{st.debtTurnsRemaining}回転")
            Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.DarkYellow
        Console.WriteLine(f"\n地下統計:")
        Console.WriteLine(f"  訪問回数: {st.undergroundVisits}回")
        Console.WriteLine(f"  総回転数: {st.undergroundTotalSpins}回")
        Console.WriteLine(f"  勝利回数: {st.undergroundWins}回")
        if st.undergroundConsecutiveLoses > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  連敗中: {st.undergroundConsecutiveLoses}回")
        Console.ResetColor()
        missions_mod.ShowUncompletedMissions()
        Console.WriteLine("\n┌────────────────────────────┐")
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine("│  [1] 500G でプレイ        │")
        Console.WriteLine("│  [2] 1000G でプレイ       │")
        Console.WriteLine("│  [3] 5000G でプレイ       │")
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("│  [4] 全財産を賭ける       │")
        Console.ResetColor()
        if st.money < 500:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("│  [5] 借金する (500G)      │")
            Console.ResetColor()
        Console.WriteLine("│  [M] ミッション確認       │")
        Console.WriteLine("│  [S] ショップ             │")
        if st.abandonedCasinoUnlocked:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("│  [A] 廃娯楽施設           │")
            Console.ResetColor()
        Console.WriteLine("│  [X] 地下退出             │")
        Console.WriteLine("│  [0] ゲーム終了           │")
        Console.WriteLine("└────────────────────────────┘")
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        bet = 0
        isAllIn = False
        if key.KeyChar == "s" or key.KeyChar == "S":
            shop.ShopMenu()
            continue
        if (key.KeyChar == "a" or key.KeyChar == "A") and st.abandonedCasinoUnlocked:
            abandoned.EnterAbandonedCasino()
            continue
        if key.KeyChar == "m" or key.KeyChar == "M":
            missions_mod.ShowAllMissions()
            continue
        if key.KeyChar == "x" or key.KeyChar == "X":
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n\n本当に地上へ戻りますか？ [Y/N]")
            Console.ResetColor()
            confirm = Console.ReadKey(True)
            if confirm.Key == ConsoleKey.Y:
                ExitUnderground()
                break
            continue
        if key.KeyChar == "0":
            st.isInUnderground = False
            return
        elif key.KeyChar == "1":
            bet = 500
        elif key.KeyChar == "2":
            bet = 1000
        elif key.KeyChar == "3":
            bet = 5000
        elif key.KeyChar == "4":
            if st.money < 100:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n所持金が少なすぎる...")
                Console.ResetColor()
                Thread.Sleep(1500)
                continue
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n\n⚠⚠⚠ 警告 ⚠⚠⚠\n")
            Console.WriteLine("全財産を賭けますか？\n")
            Console.WriteLine(f"ベット額: {st.money}G")
            Console.WriteLine("\n成功: 10倍〜100倍")
            Console.WriteLine("失敗: 全てを失う")
            Console.WriteLine("\n本当に賭けますか？ [Y/N]")
            Console.ResetColor()
            confirm = Console.ReadKey(True)
            if confirm.Key != ConsoleKey.Y:
                continue
            bet = st.money
            isAllIn = True
        elif key.KeyChar == "5" and st.money < 500:
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
        UndergroundSpin(bet, isAllIn)
        Console.WriteLine("\n\n何かキーを押して続ける...")
        Console.ReadKey(True)

def UndergroundSpin(bet, isAllIn):
    spinStartTime = DateTimeNS.Now
    st.money -= bet
    st.totalSpins += 1
    st.undergroundTotalSpins += 1
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    DrawUndergroundTitle()
    Console.ForegroundColor = ConsoleColor.Red
    if isAllIn:
        Console.WriteLine(f"\n🔥🔥🔥 全財産ベット: {bet}G 🔥🔥🔥")
    else:
        Console.WriteLine(f"\n🔥🔥🔥 地下カジノ - ベット: {bet}G 🔥🔥🔥")
    Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels([ 0, 1, 2 ])
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine(f"        ▼ {st.undergroundDealerName}が不気味に笑う ▼")
    Console.ResetColor()
    Thread.Sleep(1200)
    # 血の演出
    if st.rand.Next(100) < 30:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n        💀 血が滴る... 💀")
        Console.ResetColor()
        Thread.Sleep(800)
    # リール回転（遅め＆不気味）
    for t in range(0, 25):
        reels = [ st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)) ]
        Console.clear()
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.DarkRed
        DrawUndergroundTitle()
        Console.ForegroundColor = ConsoleColor.Red
        if isAllIn:
            Console.WriteLine(f"\n🔥🔥🔥 全財産ベット: {bet}G 🔥🔥🔥")
        else:
            Console.WriteLine(f"\n🔥🔥🔥 地下カジノ - ベット: {bet}G 🔥🔥🔥")
        Console.ResetColor()
        Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            Console.ResetColor()
        Console.WriteLine("\n")
        # 血のエフェクト
        if t % 3 == 0:
            Console.ForegroundColor = ConsoleColor.DarkRed
        else:
            Console.ForegroundColor = ConsoleColor.Red
        ui_mod.DrawReels(reels)
        Console.ResetColor()
        delay = (70 if t < 15 else 70 + (t - 15) * 25)
        Thread.Sleep(delay)
    # 結果決定（超低確率）
    result = ([0] * 3)
    # 地下カジノは当たり確率激減
    baseChance = (15 if isAllIn else 10)
    # 全財産は少し優遇
    if st.undergroundCursedMode:
        baseChance //= 2
    # 呪いモードで更に半減
    for i in range(0, 3):
        rnd = st.rand.Next(100)
        if rnd < baseChance / 3:
            result[i] = 2
        # 777: 約3%
        elif rnd < baseChance:
            result[i] = 0
        # 他当たり: 約7%
        else:
            result[i] = st.rand.Next(5, len(st.symbols))
        # ハズレ: 約90%
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    DrawUndergroundTitle()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine(f"\n🔥🔥🔥 地下カジノ - 結果 🔥🔥🔥")
    Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels(result)
    Thread.Sleep(1000)
    Console.WriteLine("\n")
    winAmount = 0
    # 配当倍率（ランダム）
    multipliers = [ 10, 20, 50, 100 ]
    multiplier = multipliers[st.rand.Next(len(multipliers))]
    if st.godMode and st.godModeRemaining > 0:
        multiplier *= 2
    if st.deathRingEquipped:
        multiplier *= 10
    isWin = False
    if result[0] == 2 and result[1] == 2 and result[2] == 2:
        winAmount = bet * multiplier
        isWin = True
        UndergroundMegaWinAnimation(f"+{winAmount}G", multiplier)
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.undergroundWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.undergroundConsecutiveLoses = 0
        st.total777Count += 1
        if isAllIn:
            st.undergroundAllInWin = True
            if not ("地下全財産勝利" in st.unlockedEvents):
                st.unlockedEvents.append("地下全財産勝利")
        if not ("地下777" in st.unlockedEvents):
            st.unlockedEvents.append("地下777")
        stats.UnlockSymbol()
    elif result[0] == result[1] and result[1] == result[2]:
        winAmount = bet * (multiplier // 2)
        isWin = True
        UndergroundBigWinAnimation(f"+{winAmount}G", multiplier // 2)
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.undergroundWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.undergroundConsecutiveLoses = 0
        if isAllIn:
            st.undergroundAllInWin = True
            if not ("地下全財産勝利" in st.unlockedEvents):
                st.unlockedEvents.append("地下全財産勝利")
        if st.deathRingEquipped:
            st.deathRing10Wins += 1
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n💀 死神の指輪: {st.deathRing10Wins}回勝利")
            Console.ResetColor()
            Thread.Sleep(1000)
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        winAmount = bet * (multiplier // 5)
        isWin = True
        UndergroundSmallWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.undergroundWins += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        st.undergroundConsecutiveLoses = 0
        if st.deathRingEquipped:
            st.deathRing10Wins += 1
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n💀 死神の指輪: {st.deathRing10Wins}回勝利")
            Console.ResetColor()
            Thread.Sleep(1000)
    else:
        st.totalLoseAmount += bet
        UndergroundLoseAnimation(isAllIn)
        st.consecutiveWins = 0
        st.totalLoses += 1
        st.undergroundConsecutiveLoses += 1
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses += 1
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine(f"\n🩸 血の呪い: {st.bloodAmuletLoses}/3回")
            Console.ResetColor()
            Thread.Sleep(1500)
            if st.bloodAmuletLoses >= 3:
                endings.BloodAmuletBadEnding()
                return
        if isAllIn:
            # 全財産を失った
            UndergroundAllInLoseEvent()
        if st.deathRingEquipped:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n💀 死神の呪い: -1000G")
            Console.ResetColor()
            Thread.Sleep(1500)
            if st.money >= 1000:
                st.money -= 1000
                st.totalLoseAmount += 1000
            else:
                # 所持金不足なら借金に
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
    # スピンごとの中毒度上昇（地下は最多）
    if st.addictionLevel < 100:
        addIncrease = 3
        # 地下基本+3
        if isAllIn:
            addIncrease += 2
        # 全財産ベットで+2
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

def DrawUndergroundTitle():
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("╔═══════════════════════════════════╗")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("║      🔥🔥 地下カジノ 🔥🔥      ║")
    Console.WriteLine("║           - 奈落 -                ║")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("╚═══════════════════════════════════╝")
    Console.ResetColor()

def UndergroundMegaWinAnimation(amount, multiplier):
    lines = [
        "  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        "  🔥                                    🔥",
        f"  🔥   地下777揃い！×{multiplier}倍！！！   🔥",
        f"  🔥         {(amount).rjust(int(12))}         🔥",
        "  🔥                                    🔥",
        "  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
    ]
    ui_mod.FlashBlock(lines, 7, [ConsoleColor.Red, ConsoleColor.DarkRed], ConsoleColor.Red, 250, 150)

def UndergroundBigWinAnimation(amount, multiplier):
    lines = [f"     🔥🔥 地下大当たり×{multiplier}倍！{amount} 🔥🔥"]
    ui_mod.FlashBlock(lines, 5, [ConsoleColor.Red, ConsoleColor.Red], ConsoleColor.Red, 200, 150)

def UndergroundSmallWinAnimation(amount):
    Console.ForegroundColor = ConsoleColor.DarkYellow
    Console.WriteLine(f"        🔥 地下当たり！{amount} 🔥")
    Console.ResetColor()

def UndergroundLoseAnimation(isAllIn):
    if isAllIn:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n           💀💀💀 全てを失った... 💀💀💀")
    else:
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("           💀 ハズレ… 💀")
    Console.ResetColor()
    Thread.Sleep(1000)

def UndergroundCursedEvent():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkMagenta
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         呪いの発動")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.BackgroundColor = ConsoleColor.Black
    Console.WriteLine(f"\n\n    {st.undergroundDealerName}が何かを唱え始めた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「五度の敗北...魂に呪いを刻む...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    仮面が赤く光り始める...")
    Thread.Sleep(2000)
    st.undergroundCursedMode = True
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n    💀 呪いモード発動！当たり確率が半減！ 💀")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not ("地下の呪い" in st.unlockedEvents):
        st.unlockedEvents.append("地下の呪い")

def UndergroundRandomEvent():
    eventType = st.rand.Next(6)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    _sw2 = eventType
    if _sw2 == 0:
        Console.WriteLine("    壁から血が滴っている...")
    elif _sw2 == 1:
        Console.WriteLine("    どこからか悲鳴が聞こえる...")
    elif _sw2 == 2:
        Console.WriteLine(f"    {st.undergroundDealerName}が不気味に笑っている...")
    elif _sw2 == 3:
        Console.WriteLine("    床に血痕が...誰かがここで...")
    elif _sw2 == 4:
        Console.WriteLine("    鎖の音が響く...誰かが繋がれている...")
        if not ("地下の囚人" in st.unlockedEvents):
            st.unlockedEvents.append("地下の囚人")
    elif _sw2 == 5:
        Console.WriteLine("    仮面の奥から赤い目が光った...")
    Console.ResetColor()
    Thread.Sleep(2500)

def UndergroundAllInLoseEvent():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         全財産喪失")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    全てを失った...")
    Thread.Sleep(2000)
    Console.WriteLine(f"\n    {st.undergroundDealerName}が静かに語りかける...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「運がなかったな...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...だが、まだチャンスはある」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「もっと...深い場所へ行くか？」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n    仮面の奥で何かがうごめいている...")
    Console.ResetColor()
    Thread.Sleep(2000)
    if not ("全財産喪失" in st.unlockedEvents):
        st.unlockedEvents.append("全財産喪失")
