# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 装備アイテム (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import events

# ========== 装備管理 ==========

def EquipmentMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║          ⚔ 装備管理 ⚔          ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine("\n【現在の装備】\n")
        if st.greedRingEquipped:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("  💀 強欲の指輪 [装備中]")
            Console.WriteLine("     効果: 負け-500G / 勝ち×5倍")
            Console.WriteLine("     デメリット: 他装備無効、演出なし、運気大幅DOWN")
            Console.ResetColor()
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("  装備なし")
            Console.ResetColor()
        Console.WriteLine("\n\n【所持アイテム】\n")
        # 強欲の指輪
        if st.hasGreedRing:
            Console.ForegroundColor =(ConsoleColor.DarkGray if st.greedRingEquipped else ConsoleColor.Red)
            Console.WriteLine("  [1] 💀 強欲の指輪")
            if not st.greedRingEquipped:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("      [装備する]")
            else:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("      [装備中 - 2で外す]")
            Console.ResetColor()
        # 悪魔のコイン
        if st.hasDevilCoin:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("  [3] 💀 悪魔のコイン")
            Console.WriteLine("      次回100%勝利 → その後5回100%負け")
            if st.devilCoinActive:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("      [使用済み - 呪い発動中]")
            else:
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("      [使用する]")
            Console.ResetColor()
        # 血塗られたお守り
        if st.hasBloodAmulet:
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine("  [4] 🩸 血塗られたお守り")
            Console.WriteLine("      当たり確率2倍 / 3敗でBAD END")
            if st.bloodAmuletEquipped:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine(f"      [装備中 - 負け: {st.bloodAmuletLoses}/3]")
            else:
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("      [装備する]")
            Console.ResetColor()
        # 死神の指輪
        if st.hasDeathRing:
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("  [5] 💀 死神の指輪")
            Console.WriteLine("      勝ち×10倍 / 負け-1000G")
            if st.deathRingEquipped:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("      [装備中]")
            else:
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("      [装備する]")
            Console.ResetColor()
        # 時を刻む懐中時計
        if st.hasTimeClock:
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.WriteLine("  [6] ⏰ 時を刻む懐中時計")
            Console.WriteLine("      GOD MODE+5 / 1回転3秒制限")
            if st.timeClockEquipped:
                Console.ForegroundColor = ConsoleColor.Yellow
                Console.WriteLine("      [装備中]")
            else:
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("      [装備する]")
            Console.ResetColor()
        # 禁断の水晶玉
        if st.hasOracleBall:
            Console.ForegroundColor = ConsoleColor.Blue
            Console.WriteLine("  [7] 🔮 禁断の水晶玉")
            Console.WriteLine("      次回出目予知 / 50%没収")
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine("      [使用する]")
            Console.ResetColor()
        # 🆕 リハビリ券
        if st.itemInventory["返済猶予券"] > 0:
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.WriteLine("\n  [8] 🩺 リハビリ券")
            Console.WriteLine("      中毒度-50 / 心の回復")
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine(f"      [使用する - 所持数: {st.itemInventory['返済猶予券']}個]")
            Console.ResetColor()
        Console.WriteLine("\n  [9] 全装備を外す")
        Console.WriteLine("\n  [0] 戻る")
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            break
        # 強欲の指輪装備
        if key.KeyChar == "1" and st.hasGreedRing and not st.greedRingEquipped:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n⚠ 警告 ⚠\n")
            Console.WriteLine("強欲の指輪を装備しますか？\n")
            Console.WriteLine("装備すると：")
            Console.WriteLine("  ・負けるたびに-500G（所持金不足なら借金）")
            Console.WriteLine("  ・勝つと獲得金×5倍")
            Console.WriteLine("  ・お守り、幸運のコイン無効化")
            Console.WriteLine("  ・全ての特殊演出が発生しなくなる")
            Console.WriteLine("  ・当たり確率が大幅DOWN（約14%）")
            Console.WriteLine("  ・借金5000G到達でBAD END")
            Console.WriteLine("\n本当に装備しますか？ [Y/N]")
            Console.ResetColor()
            confirm = Console.ReadKey(True)
            if confirm.Key == ConsoleKey.Y:
                st.greedRingEquipped = True
                events.GreedRingEquipAnimation()
                if not ("強欲の指輪装備" in st.unlockedEvents):
                    st.unlockedEvents.append("強欲の指輪装備")
        # 強欲の指輪を外す
        elif key.KeyChar == "2" and st.greedRingEquipped:
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n\n強欲の指輪を外しますか？ [Y/N]")
            Console.ResetColor()
            confirm = Console.ReadKey(True)
            if confirm.Key == ConsoleKey.Y:
                st.greedRingEquipped = False
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("\n\n強欲の指輪を外した...")
                Console.WriteLine("オーラが消えていく...")
                Console.ResetColor()
                Thread.Sleep(2000)
        # 悪魔のコイン使用
        elif key.KeyChar == "3" and st.hasDevilCoin and not st.devilCoinActive:
            UseDevilCoin()
        # 血塗られたお守り装備/解除
        elif key.KeyChar == "4" and st.hasBloodAmulet:
            ToggleBloodAmulet()
        # 死神の指輪装備/解除
        elif key.KeyChar == "5" and st.hasDeathRing:
            ToggleDeathRing()
        # 時を刻む懐中時計装備/解除
        elif key.KeyChar == "6" and st.hasTimeClock:
            ToggleTimeClock()
        # 禁断の水晶玉使用
        elif key.KeyChar == "7" and st.hasOracleBall:
            UseOracleBall()
        # 🆕 リハビリ券使用
        elif key.KeyChar == "8" and st.itemInventory["返済猶予券"] > 0:
            UseRehabTicket()
        # 全装備解除
        elif key.KeyChar == "9":
            UnequipAll()
# ========== 悪魔のコイン使用 ==========

def UseDevilCoin():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n⚠ 悪魔のコインを使用しますか？ ⚠\n")
    Console.WriteLine("次回は100%勝利")
    Console.WriteLine("その後5回は100%敗北")
    Console.WriteLine("\n本当に使用しますか？ [Y/N]")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key == ConsoleKey.Y:
        st.devilCoinActive = True
        st.devilCoinWin = False
        st.devilCoinCurse = 0
        Console.clear()
        for i in range(0, 5):
            Console.BackgroundColor =(ConsoleColor.DarkRed if i % 2 == 0 else ConsoleColor.Black)
            Console.ForegroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.Red)
            Console.clear()
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    💀 悪魔のコインが輝く... 💀")
            Thread.Sleep(300)
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n悪魔のコインを使用した！")
        Console.WriteLine("次回は必ず勝つ...しかし...")
        Console.ResetColor()
        Thread.Sleep(2500)
# ========== 血塗られたお守り装備/解除 ==========

def ToggleBloodAmulet():
    if st.bloodAmuletEquipped:
        st.bloodAmuletEquipped = False
        st.bloodAmuletLoses = 0
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n血塗られたお守りを外した...")
        Console.ResetColor()
        Thread.Sleep(1500)
    else:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n⚠ 血塗られたお守りを装備しますか？ ⚠\n")
        Console.WriteLine("当たり確率が2倍")
        Console.WriteLine("3回負けるとBAD END")
        Console.WriteLine("\n本当に装備しますか？ [Y/N]")
        Console.ResetColor()
        key = Console.ReadKey(True)
        if key.Key == ConsoleKey.Y:
            st.bloodAmuletEquipped = True
            st.bloodAmuletLoses = 0
            Console.clear()
            Console.ForegroundColor = ConsoleColor.DarkRed
            Console.WriteLine("\n\n血塗られたお守りを装備した...")
            Console.WriteLine("血の匂いがする...")
            Console.ResetColor()
            Thread.Sleep(2000)
# ========== 死神の指輪装備/解除 ==========

def ToggleDeathRing():
    if st.deathRingEquipped:
        st.deathRingEquipped = False
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n死神の指輪を外した...")
        Console.ResetColor()
        Thread.Sleep(1500)
    else:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n⚠ 死神の指輪を装備しますか？ ⚠\n")
        Console.WriteLine("勝利時の獲得金×10倍")
        Console.WriteLine("敗北時-1000G（強制）")
        Console.WriteLine("\n本当に装備しますか？ [Y/N]")
        Console.ResetColor()
        key = Console.ReadKey(True)
        if key.Key == ConsoleKey.Y:
            st.deathRingEquipped = True
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n\n死神の指輪を装備した...")
            Console.WriteLine("冷たい金属が指に食い込む...")
            Console.ResetColor()
            Thread.Sleep(2000)
# ========== 時を刻む懐中時計装備/解除 ==========

def ToggleTimeClock():
    if st.timeClockEquipped:
        st.timeClockEquipped = False
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n時を刻む懐中時計を外した...")
        Console.ResetColor()
        Thread.Sleep(1500)
    else:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n⚠ 時を刻む懐中時計を装備しますか？ ⚠\n")
        Console.WriteLine("GOD MODE持続+5回")
        Console.WriteLine("1回転3秒以内に決定必須")
        Console.WriteLine("\n本当に装備しますか？ [Y/N]")
        Console.ResetColor()
        key = Console.ReadKey(True)
        if key.Key == ConsoleKey.Y:
            st.timeClockEquipped = True
            # 🆕 GOD MODE追加
            if not st.godMode:
                st.godMode = True
                st.godModeRemaining = 5
            else:
                st.godModeRemaining += 5
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Cyan
            Console.WriteLine("\n\n時を刻む懐中時計を装備した...")
            Console.WriteLine("カチ...カチ...カチ...")
            Thread.Sleep(1500)
            Console.ForegroundColor = ConsoleColor.Magenta
            Console.WriteLine("\n⏰ GOD MODE +5回 発動！")
            Console.ResetColor()
            Thread.Sleep(2000)
# ========== 禁断の水晶玉使用 ==========

def UseOracleBall():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Blue
    Console.WriteLine("\n\n禁断の水晶玉を使用しますか？\n")
    Console.WriteLine("次回の出目を予知できる")
    Console.WriteLine("ただし50%の確率で没収される")
    Console.WriteLine("\n本当に使用しますか？ [Y/N]")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key == ConsoleKey.Y:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n\n水晶玉が輝く...")
        Thread.Sleep(1500)
        # 50%没収判定
        if st.rand.Next(2) == 0:
            st.hasOracleBall = False
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n水晶玉が砕け散った！")
            Console.WriteLine("没収された...")
            Console.ResetColor()
            Thread.Sleep(2500)
        else:
            # 次回の出目を予知
            st.oracleBallPrediction = st.rand.Next(len(st.symbols))
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("\n未来が見える...")
            Console.WriteLine(f"\n次回の出目: シンボル#{st.oracleBallPrediction}")
            Console.ResetColor()
            Thread.Sleep(3000)
# ========== 全装備解除 ==========

def UnequipAll():
    st.bloodAmuletEquipped = False
    st.deathRingEquipped = False
    st.timeClockEquipped = False
    st.greedRingEquipped = False
    st.bloodAmuletLoses = 0
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine("\n\n全ての装備を外しました")
    Console.ResetColor()
    Thread.Sleep(1500)

def UseRehabTicket():
    if st.itemInventory["返済猶予券"] <= 0:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\nリハビリ券を持っていません")
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\nリハビリ券を使用しますか？ [Y/N]")
    Console.WriteLine("（中毒度-50、1枚消費）")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key == ConsoleKey.Y:
        st.itemInventory["返済猶予券"] -= 1
        st.addictionLevel = Math.Max(0, st.addictionLevel - 50)
        st.hasUsedRehab = True
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    深呼吸をする...")
        Thread.Sleep(2000)
        Console.WriteLine("\n    心が落ち着いてきた...")
        Thread.Sleep(2000)
        Console.WriteLine("\n    少し...楽になった...")
        Thread.Sleep(2000)
        Console.WriteLine(f"\n\n    中毒度: {st.addictionLevel}%")
        Console.ResetColor()
        Thread.Sleep(2000)
