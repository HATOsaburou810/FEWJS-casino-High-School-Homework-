# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 悪魔契約 (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st

# ========== 悪魔契約システム ==========

def DevilContractOfferEvent():
    Console.clear()
    # 画面を暗転
    for i in range(0, 5):
        Console.clear()
        Console.BackgroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.DarkRed)
        Thread.Sleep(300)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         悪魔の囁き")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    突然、世界が静止した...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    音が消える...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    時が止まる...")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    闇の中から声が響く...")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n    「...苦しいか...？」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...絶望しているか...？」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「...力が...欲しいか...？」")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    巨大な影が現れた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    それは...悪魔だった...")
    Thread.Sleep(2000)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈")
    Console.WriteLine("    😈                              😈")
    Console.WriteLine("    😈      悪魔が現れた！        😈")
    Console.WriteLine("    😈                              😈")
    Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    悪魔「我と契約を結ばぬか...？」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔「その苦しみ...我が救おう...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n    悪魔「...ただし、代償を払え...」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    ★ 悪魔との契約が可能になりました ★")
    Console.WriteLine("    ★ ゲームメニューから[D]で契約画面へ ★")
    Console.ResetColor()
    Thread.Sleep(4000)

def DevilContractMenu():
    if not st.devilContractOffered:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n悪魔はまだ現れていない...")
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    if st.devilContractActive:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n既に契約中です")
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    while True:
        Console.clear()
        Console.BackgroundColor = ConsoleColor.DarkRed
        Console.ForegroundColor = ConsoleColor.Black
        Console.WriteLine("\n╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║        😈 悪魔との契約 😈       ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.BackgroundColor = ConsoleColor.Black
        Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.DarkMagenta
        Console.WriteLine("\n\n悪魔「さあ...選ぶがよい...」\n")
        Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("【契約1】魂の担保")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("  効果: 次の10回転必ず勝つ")
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine("  代償: 11回目で即GAME OVER")
        Console.ResetColor()
        Console.WriteLine()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("【契約2】時間との取引")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("  効果: 借金が半額になる")
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine("  代償: 5分以内に完済必須")
        Console.ResetColor()
        Console.WriteLine()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("【契約3】記憶の代償")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("  効果: 借金全額帳消し")
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine("  代償: 全データリセット")
        Console.WriteLine("        (アイテム/実績/コレクション消失)")
        Console.ResetColor()
        Console.WriteLine("\n\n  [1] 契約1を結ぶ")
        Console.WriteLine("  [2] 契約2を結ぶ")
        Console.WriteLine("  [3] 契約3を結ぶ")
        Console.WriteLine("  [0] 契約しない")
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            Console.clear()
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("\n\n\n悪魔「...いつでも呼ぶがよい...」")
            Console.ResetColor()
            Thread.Sleep(2000)
            break
        elif key.KeyChar >= "1" and key.KeyChar <= "3":
            choice = cs_int_parse(str(key.KeyChar))
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n\n\n⚠⚠⚠ 最終確認 ⚠⚠⚠\n")
            Console.WriteLine(f"契約{choice}を結びますか？\n")
            Console.WriteLine("一度契約すると取り消せません")
            Console.WriteLine("\n本当に契約しますか？ [Y/N]")
            Console.ResetColor()
            confirmKey = Console.ReadKey(True)
            # ← 変数名を変更
            if confirmKey.Key == ConsoleKey.Y:  # ← key を confirmKey に変更
                ExecuteDevilContract(choice)
                break
# ← DevilContractMenu() の終了
# ========== 中毒システム強化 ==========

def ExecuteDevilContract(contractType):
    st.devilContractActive = True
    st.devilContractType = contractType
    st.contractStartTime = DateTimeNS.Now
    Console.clear()
    for i in range(0, 7):
        Console.clear()
        Console.BackgroundColor =(ConsoleColor.DarkRed if i % 2 == 0 else ConsoleColor.Black)
        Console.ForegroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.Red)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈")
        Console.WriteLine("    😈                              😈")
        Console.WriteLine("    😈      契約成立！！！        😈")
        Console.WriteLine("    😈                              😈")
        Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈")
        Thread.Sleep(300)
    Console.clear()
    Console.BackgroundColor = ConsoleColor.Black
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n\n")
    _sw7 = contractType
    if _sw7 == 1:
        Console.WriteLine("    悪魔「魂を担保に...10回の勝利を与えよう...」")
        Thread.Sleep(2000)
        Console.WriteLine("\n    悪魔「...だが11回目には...魂を頂く...」")
        Thread.Sleep(2000)
        st.contract1WinCount = 0
    elif _sw7 == 2:
        Console.WriteLine("    悪魔「借金を半額にしてやろう...」")
        Thread.Sleep(2000)
        reduction = st.debt // 2
        st.debt -= reduction
        st.contract2OriginalDebt = st.debt
        st.contract2Deadline = DateTimeNS.Now.AddMinutes(5)
        Console.WriteLine(f"\n    借金が{reduction}G減少した！")
        Thread.Sleep(2000)
        Console.WriteLine("\n    悪魔「...だが5分以内に完済せよ...」")
        Thread.Sleep(2000)
        Console.WriteLine("\n    悪魔「...さもなくば...魂を頂く...」")
        Thread.Sleep(2000)
    elif _sw7 == 3:
        Console.WriteLine("    悪魔「借金を全て消してやろう...」")
        Thread.Sleep(2000)
        st.debt = 0
        st.debtTurnsRemaining = 0
        Console.WriteLine("\n    借金が消えた！")
        Thread.Sleep(2000)
        Console.WriteLine("\n    悪魔「...だが、お前の記憶は消える...」")
        Thread.Sleep(2000)
        # データリセット
        st.itemInventory["お守り"] = 0
        st.itemInventory["幸運のコイン"] = 0
        st.itemInventory["返済猶予券"] = 0
        st.hasGreedRing = False
        st.greedRingEquipped = False
        st.unlockedSymbols.clear()
        st.unlockedSymbols.append("スライム")
        st.unlockedSymbols.append("ゴーレム")
        st.unlockedEvents.clear()
        for mission in st.missions:
            mission.Completed = False
        Console.WriteLine("\n    全てのアイテム・実績が消失した...")
        Thread.Sleep(2000)
        st.devilContractActive = False
        st.devilContractSuccess = True
        st.contract1Complete = True
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n    契約は完了した...")
    Console.ResetColor()
    Thread.Sleep(3000)
    if not (f"悪魔契約{contractType}" in st.unlockedEvents):
        st.unlockedEvents.append(f"悪魔契約{contractType}")
