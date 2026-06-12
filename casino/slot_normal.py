# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 通常スロット (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import missions as missions_mod
from . import ui as ui_mod
from . import endings, stats

# ========== 通常スピン処理（既存コードから抽出）==========

def NormalSpin(bet):
    spinStartTime = DateTimeNS.Now
    Console.clear()
    if st.greedRingEquipped:
        Console.BackgroundColor = ConsoleColor.DarkRed
        Console.ForegroundColor = ConsoleColor.Black
    ui_mod.DrawTitle()
    if st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Red
        Console.BackgroundColor = ConsoleColor.Black
        Console.WriteLine(f"\n💀💀💀 強欲のオーラ 発動中 💀💀💀")
        Console.ResetColor()
    if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
        Console.ResetColor()
    if st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"\n☆☆☆ ラッキータイム！残り{st.luckyTimeRemaining}回 ☆☆☆")
        Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels([ 0, 1, 2 ])
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("        ▼ 回転開始！ ▼")
    Console.ResetColor()
    Thread.Sleep(800)
    freezeEffect = False
    premiumEffect = False
    if not st.greedRingEquipped:
        freezeEffect = st.rand.Next(1000) < 1
        if freezeEffect:
            FreezeEffect()
            if not ("フリーズ演出" in st.unlockedEvents):
                st.unlockedEvents.append("フリーズ演出")
        premiumEffect = st.rand.Next(1000) < 5
        if premiumEffect:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n        ！！！画面フラッシュ！！！")
            Console.ResetColor()
            Thread.Sleep(300)
            Console.clear()
            ui_mod.DrawTitle()
            Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
            if st.debt > 0:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine(f"借金: {st.debt}G")
                Console.ResetColor()
            Console.WriteLine("\n")
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("           ★★★★★★★★★★★★★★★★★★★")
            Console.WriteLine("         ★                                　★")
            Console.WriteLine("       ★      　プレミア演出発生！       ★")
            Console.WriteLine("     ★                                ★")
            Console.WriteLine("    ★★★★★★★★★★★★★★★★★")
            Console.ResetColor()
            Thread.Sleep(2000)
    for t in range(0, 25):
        reels = [ st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)), st.rand.Next(len(st.symbols)) ]
        Console.clear()
        # スピン中グリッチ（中毒度/悪魔契約で発動）
        if t == 12:
            ui_mod.SpinGlitch()
        if st.greedRingEquipped:
            Console.BackgroundColor = ConsoleColor.DarkRed
            Console.ForegroundColor = ConsoleColor.Black
        ui_mod.DrawTitle()
        if st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Red
            Console.BackgroundColor = ConsoleColor.Black
            Console.WriteLine(f"\n💀💀💀 強欲のオーラ 発動中 💀💀💀")
            Console.ResetColor()
        if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
            Console.ResetColor()
        if st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine(f"\n☆☆☆ ラッキータイム！残り{st.luckyTimeRemaining}回 ☆☆☆")
            Console.ResetColor()
        Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
        if st.debt > 0:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"借金: {st.debt}G")
            Console.ResetColor()
        Console.WriteLine("\n")
        if premiumEffect and t % 2 == 0 and not st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Yellow
        ui_mod.DrawReels(reels)
        Console.ResetColor()
        delay = (60 if t < 15 else 60 + (t - 15) * 20)
        Thread.Sleep(delay)
    # ← このカッコの直後に挿入
    # 🆕 時計装備時の制限時間チェック
    if st.timeClockEquipped:
        elapsed = DateTimeNS.Now - spinStartTime
        if elapsed.TotalSeconds > 3:
            # 3秒超過 → 強制負け
            Console.clear()
            Console.BackgroundColor = ConsoleColor.Black
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    ⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰")
            Console.WriteLine("    ⏰                          　　⏰")
            Console.WriteLine("    ⏰        時間切れ！！！        ⏰")
            Console.WriteLine("    ⏰                              ⏰")
            Console.WriteLine("    ⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰")
            Thread.Sleep(1500)
            Console.clear()
            ui_mod.DrawTitle()
            Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
            Console.WriteLine("\n")
            # ランダムなハズレ結果
            loseResult = [ st.rand.Next(5, len(st.symbols)), st.rand.Next(5, len(st.symbols)), st.rand.Next(5, len(st.symbols)) ]
            ui_mod.DrawReels(loseResult)
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine("\n           ⏰ 制限時間超過... ⏰")
            Console.ResetColor()
            Thread.Sleep(1500)
            st.totalLoseAmount += bet
            st.totalLoses += 1
            st.consecutiveWins = 0
            # 血お守りの処理
            if st.bloodAmuletEquipped:
                st.bloodAmuletLoses += 1
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血の呪い: {st.bloodAmuletLoses}/3回")
                Console.ResetColor()
                Thread.Sleep(1500)
                if st.bloodAmuletLoses >= 3:
                    endings.BloodAmuletBadEnding()
                    return
            # 死神の指輪ペナルティ
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
            return
            # スピン処理を終了
    # ========== リール結果決定 ==========
    result = ([0] * 3)
    luckBonus = 0
    # 🆕 悪魔のコイン: 次回100%勝利
    if st.devilCoinActive and not st.devilCoinWin:
        result[0] = 2
        result[1] = 2
        result[2] = 2
        st.devilCoinWin = True
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n💀 悪魔のコインの力！ 💀")
        Console.ResetColor()
        Thread.Sleep(1500)
    # 🆕 悪魔のコイン: 呪い発動中（5回強制負け）
    elif st.devilCoinActive and st.devilCoinWin and st.devilCoinCurse < 5:
        result[0] = 5
        result[1] = 6
        result[2] = 7
        st.devilCoinCurse += 1
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine(f"\n💀 呪いの代償...({st.devilCoinCurse}/5) 💀")
        Console.ResetColor()
        Thread.Sleep(1500)
        if st.devilCoinCurse >= 5:
            st.devilCoinActive = False
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n呪いが解けた...")
            Console.ResetColor()
            Thread.Sleep(1500)
    # 🆕 水晶玉予知
    elif st.oracleBallPrediction >= 0:
        result[0] = st.oracleBallPrediction
        result[1] = st.oracleBallPrediction
        result[2] = st.oracleBallPrediction
        st.oracleBallPrediction = -1
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n🔮 予知通りの未来...！ 🔮")
        Console.ResetColor()
        Thread.Sleep(1500)
    else:
        # 通常の確率計算
        if not st.greedRingEquipped:
            if st.itemInventory["お守り"] > 0:
                luckBonus += 3
            if st.itemInventory["幸運のコイン"] > 0:
                luckBonus += 8
                st.itemInventory["幸運のコイン"] -= 1
            # 🆕 血塗られたお守り: 確率2倍
            if st.bloodAmuletEquipped:
                luckBonus += 15
        if freezeEffect or premiumEffect:
            result[0] = 2
            result[1] = 2
            result[2] = 2
        else:
            luckyBonus = (10 if (st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped) else 0)
            settingBonus = (0 if st.greedRingEquipped else st.setting * 1)
            if st.greedRingEquipped:
                for i in range(0, 3):
                    rnd = st.rand.Next(100)
                    if rnd < 2:
                        result[i] = 2
                    elif rnd < 6:
                        result[i] = 0
                    elif rnd < 10:
                        result[i] = 1
                    elif rnd < 14:
                        result[i] = 4
                    else:
                        result[i] = st.rand.Next(5, len(st.symbols))
            else:
                for i in range(0, 3):
                    rnd = st.rand.Next(100)
                    threshold777 = 4 + luckyBonus + settingBonus + luckBonus
                    threshold0 = 12 + luckyBonus + settingBonus + luckBonus
                    threshold1 = 22 + luckyBonus + settingBonus + luckBonus
                    threshold4 = 35 + luckyBonus + settingBonus + luckBonus
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
    isReach = (result[0] == result[2] and result[0] != result[1]) and st.rand.Next(100) < 15 and not st.greedRingEquipped
    if isReach:
        ReachEffect(result)
    Console.clear()
    if st.greedRingEquipped:
        Console.BackgroundColor = ConsoleColor.DarkRed
        Console.ForegroundColor = ConsoleColor.Black
    ui_mod.DrawTitle()
    if st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Red
        Console.BackgroundColor = ConsoleColor.Black
        Console.WriteLine(f"\n💀💀💀 強欲のオーラ 発動中 💀💀💀")
        Console.ResetColor()
    if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n★★★ GOD MODE 発動中！残り{st.godModeRemaining}回 ★★★")
        Console.ResetColor()
    if st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"\n☆☆☆ ラッキータイム！残り{st.luckyTimeRemaining}回 ☆☆☆")
        Console.ResetColor()
    Console.WriteLine(f"\n所持金: {st.money}G  │  BET: {bet}G")
    if st.debt > 0:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"借金: {st.debt}G")
        Console.ResetColor()
    Console.WriteLine("\n")
    ui_mod.DrawReels(result)
    Thread.Sleep(600)
    Console.WriteLine("\n")
    winAmount = 0
    multiplier = 1
    if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
        multiplier *= 2
    # 🆕 死神の指輪: 勝利時×10倍
    if st.deathRingEquipped:
        multiplier *= 10
    isWin = False
    if result[0] == 2 and result[1] == 2 and result[2] == 2:
        winAmount = bet * 10 * multiplier
        isWin = True
        if st.greedRingEquipped:
            winAmount *= 5
            GreedRingMegaWinAnimation(f"+{winAmount}G")
        else:
            ui_mod.JackpotGlitch()
            MegaWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.bigWinCount += 1
        st.total777Count += 1
        st.totalLoses = 0
        st.consecutiveLosses = 0
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            # 🆕 5連勝カウント
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        if st.deathRingEquipped:
            st.deathRing10Wins += 1
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n💀 死神の指輪: {st.deathRing10Wins}回勝利")
            Console.ResetColor()
            Thread.Sleep(1000)
        if not ("777大当たり" in st.unlockedEvents):
            st.unlockedEvents.append("777大当たり")
        if not st.greedRingEquipped:
            stats.UnlockSymbol()
        if bet == 5000:
            st.vip5000BetWin = True
    elif result[0] == result[1] and result[1] == result[2]:
        winAmount = bet * 5 * multiplier
        isWin = True
        if st.greedRingEquipped:
            winAmount *= 5
            GreedRingBigWinAnimation(f"+{winAmount}G")
        else:
            BigWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.totalLoses = 0
        st.consecutiveLosses = 0
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        if st.deathRingEquipped:
            st.deathRing10Wins += 1
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n💀 死神の指輪: {st.deathRing10Wins}回勝利")
            Console.ResetColor()
            Thread.Sleep(1000)
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        winAmount = bet * 2 * multiplier
        isWin = True
        if st.greedRingEquipped:
            winAmount *= 5
            GreedRingSmallWinAnimation(f"+{winAmount}G")
        else:
            SmallWinAnimation(f"+{winAmount}G")
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.totalLoses = 0
        st.consecutiveLosses = 0
        if st.bloodAmuletEquipped:
            st.bloodAmuletLoses = 0
            # 🆕 追加
            if st.consecutiveWins >= 5:
                st.bloodAmulet5Wins = Math.Max(st.bloodAmulet5Wins, st.consecutiveWins)
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血塗られたお守り: {st.consecutiveWins}連勝！")
                Console.ResetColor()
                Thread.Sleep(1000)
        if st.deathRingEquipped:
            st.deathRing10Wins += 1
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine(f"\n💀 死神の指輪: {st.deathRing10Wins}回勝利")
            Console.ResetColor()
            Thread.Sleep(1000)
    else:
        if st.greedRingEquipped:
            GreedRingLoseAnimation()
            st.greedRingLoseCount += 1
            if st.money >= 500:
                st.money -= 500
                st.totalLoseAmount += 500
            else:
                shortage = 500 - st.money
                st.totalLoseAmount += st.money
                st.money = 0
                st.debt += shortage
                st.hasEverBorrowedMoney = True
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n所持金不足...{shortage}Gが借金に追加された")
                Console.ResetColor()
                Thread.Sleep(2000)
        else:
            st.totalLoseAmount += bet
            LoseAnimation()
            # 🆕 血塗られたお守りの呪い処理
            if st.bloodAmuletEquipped:
                st.bloodAmuletLoses += 1
                Console.ForegroundColor = ConsoleColor.DarkRed
                Console.WriteLine(f"\n🩸 血の呪い: {st.bloodAmuletLoses}/3回")
                Console.ResetColor()
                Thread.Sleep(1500)
                if st.bloodAmuletLoses >= 3:
                    endings.BloodAmuletBadEnding()
                    return
                    # スピン処理を中断してメニューに戻る
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
                st.deathRing10Wins += 1
                # 使用回数カウント（ミッション用）
        st.consecutiveWins = 0
        st.totalLoses += 1
        st.consecutiveLosses += 1
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
    if st.godMode and st.godModeRemaining > 0 and not st.greedRingEquipped:
        st.godModeRemaining -= 1
        if st.godModeRemaining == 0:
            st.godMode = False
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("\n[GOD MODE 終了...]")
            Console.ResetColor()
            Thread.Sleep(1500)
    if st.luckyTimeActive and st.luckyTimeRemaining > 0 and not st.greedRingEquipped:
        st.luckyTimeRemaining -= 1
        if st.luckyTimeRemaining == 0:
            st.luckyTimeActive = False
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("\n[ラッキータイム 終了...]")
            Console.ResetColor()
            Thread.Sleep(1500)
    if winAmount > 0 and st.rand.Next(100) < 40 and not st.greedRingEquipped:
        winAmount = DoubleUpChallenge(winAmount)
    # スピンごとの中毒度上昇
    if st.addictionLevel < 100:
        addIncrease = 1
        # 基本+1
        if bet >= 100:
            addIncrease += 1
        # 100Gベットで+1
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
# ========== アニメーション ==========

def MegaWinAnimation(amount):
    lines = [
        "  ★★★★★★★★★★★★★★★★★★★★",
        "  ★                                    ★",
        f"  ★    🎊 超激レア！777揃い！🎊    ★",
        f"  ★         {(amount).rjust(int(10))}           ★",
        "  ★                                    ★",
        "  ★★★★★★★★★★★★★★★★★★★★",
    ]
    ui_mod.FlashBlock(lines, 5, [ConsoleColor.Yellow, ConsoleColor.Red], ConsoleColor.Yellow, 200, 150)

def BigWinAnimation(amount):
    lines = [f"     ◆◆◆ 大当たり！{amount} ◆◆◆"]
    ui_mod.FlashBlock(lines, 4, [ConsoleColor.Green, ConsoleColor.Green], ConsoleColor.Green, 200, 150)

def SmallWinAnimation(amount):
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine(f"        ◇ 当たり！{amount} ◇")
    Console.ResetColor()

def LoseAnimation():
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("           × ハズレ… ×")
    Console.ResetColor()

def ReachEffect(result):
    Console.clear()
    ui_mod.DrawTitle()
    Console.WriteLine("\n")
    tempResult = [ result[0], result[1], result[0] ]
    ui_mod.DrawReels(tempResult)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n        ◆◆◆ リーチ！！ ◆◆◆")
    Console.WriteLine("           左右が揃った！")
    Console.ResetColor()
    Thread.Sleep(1200)
    for i in range(0, 10):
        tempResult[1] = st.rand.Next(len(st.symbols))
        Console.clear()
        ui_mod.DrawTitle()
        Console.WriteLine("\n")
        ui_mod.DrawReels(tempResult)
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n        ◆◆◆ リーチ！！ ◆◆◆")
        Console.WriteLine("           左右が揃った！")
        Console.ResetColor()
        Thread.Sleep(150 + i * 60)

def DoubleUpChallenge(winAmount):
    Console.WriteLine("\n")
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("  ダブルアップチャレンジ発生！")
    Console.WriteLine(f"  現在の獲得金: {winAmount}G")
    Console.WriteLine("  ━━━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("  成功で2倍、失敗で0G")
    Console.WriteLine("  挑戦しますか？ [Y/N]")
    Console.ResetColor()
    choice = Console.ReadKey(True)
    if choice.Key == ConsoleKey.Y:
        Console.WriteLine("\n\n  コインを投げる...")
        Thread.Sleep(1500)
        for i in range(0, 5):
            Console.Write(("\r  ◆ 表 " if i % 2 == 0 else "\r  ◇ 裏 "))
            Thread.Sleep(300)
        success = st.rand.Next(2) == 0
        Thread.Sleep(500)
        Console.WriteLine()
        if success:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n  ★★★ 成功！2倍獲得！ ★★★")
            bonus = winAmount
            # 増加分のみ追加（呼び出し元で既に加算済み）
            winAmount *= 2
            st.money += bonus
            Console.WriteLine(f"  獲得金: {winAmount}G")
            Console.ResetColor()
        else:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n  × 失敗...獲得金が消えた ×")
            st.money -= winAmount
            winAmount = 0
            Console.ResetColor()
        Thread.Sleep(2000)
    return winAmount
# ========== イベント系（既存コードより） ==========

def GodModeActivation():
    st.godMode = True
    st.godModeRemaining = 10
    st.godModeActivateCount += 1
    Console.clear()
    for i in range(0, 5):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Magenta if i % 2 == 0 else ConsoleColor.White)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★★")
        Console.WriteLine("    ★                                    ★")
        Console.WriteLine("    ★      GOD MODE 発動！！！          ★")
        Console.WriteLine("    ★                                    ★")
        Console.WriteLine("    ★   10回転、全ての配当が2倍！      ★")
        Console.WriteLine("    ★                                    ★")
        Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★★")
        Console.ResetColor()
        Thread.Sleep(300)
    Thread.Sleep(2000)
    if not ("GOD MODE" in st.unlockedEvents):
        st.unlockedEvents.append("GOD MODE")

def LuckyTimeActivation():
    st.luckyTimeActive = True
    st.luckyTimeRemaining = 5
    Console.clear()
    for i in range(0, 4):
        Console.clear()
        Console.ForegroundColor =(ConsoleColor.Yellow if i % 2 == 0 else ConsoleColor.White)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
        Console.WriteLine("    ☆                              ☆")
        Console.WriteLine("    ☆   ラッキータイム突入！      ☆")
        Console.WriteLine("    ☆                              ☆")
        Console.WriteLine("    ☆   5回転、当たりやすい！     ☆")
        Console.WriteLine("    ☆                              ☆")
        Console.WriteLine("    ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
        Console.ResetColor()
        Thread.Sleep(300)
    Thread.Sleep(1500)

def FreezeEffect():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n\n")
    Console.WriteLine("            画面が止まった...")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n          フ リ ー ズ 確 定 ！！！")
    Thread.Sleep(1500)
    Console.clear()
    for i in range(0, 6):
        Console.ForegroundColor =(ConsoleColor.Red if i % 2 == 0 else ConsoleColor.Yellow)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ■■■■■■■■■■■■■■■■■■■")
        Console.WriteLine("    ■                                ■")
        Console.WriteLine("    ■   フリーズ演出発動！！！      ■")
        Console.WriteLine("    ■                                ■")
        Console.WriteLine("    ■      777 確 定 ！！！         ■")
        Console.WriteLine("    ■                                ■")
        Console.WriteLine("    ■■■■■■■■■■■■■■■■■■■")
        Thread.Sleep(300)
        Console.clear()
        Thread.Sleep(200)
    Thread.Sleep(2000)

def GreedRingMegaWinAnimation(amount):
    lines = [
        "  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀",
        "  💀                                    💀",
        f"  💀    強欲の祝福！777揃い！×5倍   💀",
        f"  💀         {(amount).rjust(int(10))}           💀",
        "  💀                                    💀",
        "  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀",
    ]
    ui_mod.FlashBlock(lines, 5, [(ConsoleColor.DarkRed, ConsoleColor.Black), (ConsoleColor.Black, ConsoleColor.Red)], (ConsoleColor.DarkRed, ConsoleColor.Red), 200, 150)

def GreedRingBigWinAnimation(amount):
    lines = [f"     💀💀 大当たり×5倍！{amount} 💀💀"]
    ui_mod.FlashBlock(lines, 4, [(ConsoleColor.DarkRed, ConsoleColor.Red), (ConsoleColor.DarkRed, ConsoleColor.Red)], (ConsoleColor.DarkRed, ConsoleColor.Red), 200, 150)

def GreedRingSmallWinAnimation(amount):
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine(f"        💀 当たり×5倍！{amount} 💀")
    Console.ResetColor()

def GreedRingLoseAnimation():
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("           💀 ハズレ... -500G 💀")
    Console.ResetColor()
    Thread.Sleep(1000)
