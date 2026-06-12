# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 開発者モード (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import abandoned, events, shop

# ========================================
# ========== DEV MODE ==========
# ========================================

def DevModeEntry():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGreen
    Console.WriteLine("\n\n\n    [DEV] パスワードを入力してください > ")
    Console.ResetColor()
    Console.CursorVisible = True
    input = coalesce(Console.ReadLine(), "")
    Console.CursorVisible = False
    if input.strip() != "youmukawaii":
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n    アクセス拒否")
        Console.ResetColor()
        Thread.Sleep(1200)
        return
    # 初期化（ゲーム開始前でも使えるように）
    if not ("お守り" in st.itemInventory):
        st.itemInventory["お守り"] = 0
    if not ("幸運のコイン" in st.itemInventory):
        st.itemInventory["幸運のコイン"] = 0
    if not ("返済猶予券" in st.itemInventory):
        st.itemInventory["返済猶予券"] = 0
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine("\n    ✓ DEV MODE アクセス許可")
    Console.ResetColor()
    Thread.Sleep(800)
    DevModeMenu()

def DevModeMenu():
    while True:
        Console.clear()
        Console.BackgroundColor = ConsoleColor.DarkGreen
        Console.ForegroundColor = ConsoleColor.Black
        Console.WriteLine("  ╔══════════════════════════════════════╗  ")
        Console.WriteLine("  ║         ⚙  DEV MODE MENU  ⚙        ║  ")
        Console.WriteLine("  ╚══════════════════════════════════════╝  ")
        Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine(f"\n  所持金: {st.money:,}G  借金: {st.debt:,}G  中毒度: {st.addictionLevel}%  設定: {st.setting}")
        Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  [1] ステータス操作")
        Console.WriteLine("  [2] フラグ操作")
        Console.WriteLine("  [3] アイテム操作")
        Console.WriteLine("  [4] スロット設定")
        Console.WriteLine("  [5] 時間・ターン設定")
        Console.WriteLine("  [6] デバッグ情報表示")
        Console.WriteLine("  [7] 全解放（テスト用）")
        Console.WriteLine("  [8] 全フラグリセット")
        Console.WriteLine("  [G] イベントギャラリー")
        Console.WriteLine("  [0] DEV MODE終了")
        Console.ResetColor()
        Console.Write("\n  選択 > ")
        key = Console.ReadKey(True)
        _sw8 = key.KeyChar
        if _sw8 == "1":
            DevStatusMenu()
        elif _sw8 == "2":
            DevFlagMenu()
        elif _sw8 == "3":
            DevItemMenu()
        elif _sw8 == "4":
            DevSlotMenu()
        elif _sw8 == "5":
            DevTimeMenu()
        elif _sw8 == "6":
            DevDebugInfo()
        elif _sw8 == "7":
            DevUnlockAll()
        elif _sw8 == "8":
            DevResetAll()
        elif _sw8 == "g":
            pass
        elif _sw8 == "G":
            DevEventGallery()
        elif _sw8 == "0":
            return
# ========== [1] ステータス操作 ==========

def DevStatusMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  ═══ ステータス操作 ═══")
        Console.WriteLine(f"\n  現在値: 所持金={st.money:,}G  借金={st.debt:,}G  中毒度={st.addictionLevel}%  設定={st.setting}")
        Console.WriteLine("\n  [1] 所持金を設定")
        Console.WriteLine("  [2] 借金を設定")
        Console.WriteLine("  [3] 中毒度を設定 (0-100)")
        Console.WriteLine("  [4] 設定を変更 (1-6)")
        Console.WriteLine("  [5] 所持金 +10000G")
        Console.WriteLine("  [6] 借金をゼロにする")
        Console.WriteLine("  [7] 中毒度をゼロにする")
        Console.WriteLine("  [0] 戻る")
        Console.ResetColor()
        Console.Write("\n  選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            return
        Console.CursorVisible = True
        Console.WriteLine()
        _sw9 = key.KeyChar
        if _sw9 == "1":
            Console.Write("  所持金 > ")
            if ((m := try_parse_int(Console.ReadLine())) is not None):
                st.money = m
                DevMsg(f"所持金を {m:,}G に設定")
        elif _sw9 == "2":
            Console.Write("  借金 > ")
            if ((d := try_parse_int(Console.ReadLine())) is not None):
                st.debt = d
                if d > 0:
                    st.hasEverBorrowedMoney = True
                    st.debtTurnsRemaining = 10
                DevMsg(f"借金を {d:,}G に設定")
        elif _sw9 == "3":
            Console.Write("  中毒度 (0-100) > ")
            if ((a := try_parse_int(Console.ReadLine())) is not None):
                st.addictionLevel = Math.Clamp(a, 0, 100)
                DevMsg(f"中毒度を {st.addictionLevel}% に設定")
        elif _sw9 == "4":
            Console.Write("  設定 (1-6) > ")
            if ((s := try_parse_int(Console.ReadLine())) is not None) and s >= 1 and s <= 6:
                st.setting = s
                DevMsg(f"設定{s}に変更")
        elif _sw9 == "5":
            st.money += 10000
            DevMsg("+10000G")
        elif _sw9 == "6":
            st.debt = 0
            st.debtTurnsRemaining = 0
            DevMsg("借金ゼロ")
        elif _sw9 == "7":
            st.addictionLevel = 0
            st.isAddicted = False
            DevMsg("中毒度ゼロ")
        Console.CursorVisible = False
# ========== [2] フラグ操作 ==========

def DevFlagMenu():
    # (名前, getter, setter) のリスト
    flags = py_str_list("godMode", "godModePermanent", "luckyTimeActive", "vipRoomUnlocked", "isInVIPRoom", "undergroundUnlocked", "isInUnderground", "dreamCasinoUnlocked", "hasEverBorrowedMoney", "hasSeenConversation", "hasSeenMysteriousWoman", "hasSeenVIPDealer", "hasSeenUndergroundDealer", "mushroomManMet", "devilContractOffered", "devilContractActive", "devilContractSuccess", "contract1Complete", "hasGreedRing", "greedRingEquipped", "hasDevilCoin", "hasBloodAmulet", "hasDeathRing", "hasTimeClock", "hasOracleBall", "hasUsedRehab", "isAddicted", "trueEndingUnlocked", "vip5000BetWin", "undergroundAllInWin", "undergroundCursedMode", "bellMetFirst")
    page = 0
    perPage = 12
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  ═══ フラグ操作 ═══")
        Console.WriteLine("  数字キーでON/OFF切替  [N]次ページ  [P]前ページ  [0]戻る\n")
        start = page * perPage
        end = Math.Min(start + perPage, len(flags))
        for i in range(start, end):
            f = flags[i]
            val = st.py_getflag(f)
            Console.ForegroundColor =(ConsoleColor.Yellow if val else ConsoleColor.DarkGray)
            Console.WriteLine(f"  [{i - start + 1:>2}] {(('ON ' if val else 'OFF'))}  {f}")
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine(f"\n  ページ {page + 1} / {(len(flags) + perPage - 1) // perPage}")
        Console.ResetColor()
        Console.Write("  選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            return
        if key.Key == ConsoleKey.N:
            page = Math.Min(page + 1, (len(flags) - 1) // perPage)
            continue
        if key.Key == ConsoleKey.P:
            page = Math.Max(page - 1, 0)
            continue
        if key.KeyChar >= "1" and key.KeyChar <= "9":
            idx = start + ((ord(key.KeyChar) - ord("1")))
            if idx < len(flags):
                f = flags[idx]
                newVal = not st.py_getflag(f)
                st.py_setflag(f, newVal)
                DevMsg(f"{f} → {(('ON' if newVal else 'OFF'))}")
# ========== [3] アイテム操作 ==========

def DevItemMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  ═══ アイテム操作 ═══\n")
        Console.WriteLine(f"  お守り         : {st.itemInventory.get('お守り', 0)}個")
        Console.WriteLine(f"  幸運のコイン   : {st.itemInventory.get('幸運のコイン', 0)}個")
        Console.WriteLine(f"  返済猶予券     : {st.itemInventory.get('返済猶予券', 0)}個")
        Console.WriteLine(f"  強欲の指輪     : {(('所持' if st.hasGreedRing else 'なし'))}  装備={st.greedRingEquipped}")
        Console.WriteLine(f"  悪魔のコイン   : {(('所持' if st.hasDevilCoin else 'なし'))}")
        Console.WriteLine(f"  血塗られたお守り: {(('所持' if st.hasBloodAmulet else 'なし'))}")
        Console.WriteLine(f"  死神の指輪     : {(('所持' if st.hasDeathRing else 'なし'))}")
        Console.WriteLine(f"  時を刻む懐中時計 : {(('所持' if st.hasTimeClock else 'なし'))}")
        Console.WriteLine(f"  予言の水晶球   : {(('所持' if st.hasOracleBall else 'なし'))}")
        Console.WriteLine(f"\n  解放シンボル: {', '.join(st.unlockedSymbols)}")
        Console.WriteLine("\n  [1] お守り +1      [2] 幸運のコイン +1  [3] 返済猶予券 +1")
        Console.WriteLine("  [4] 強欲の指輪入手 [5] 呪いアイテム全入手")
        Console.WriteLine("  [6] 全シンボル解放 [7] イベント全解放")
        Console.WriteLine("  [8] アイテム全クリア")
        Console.WriteLine("  [0] 戻る")
        Console.ResetColor()
        Console.Write("\n  選択 > ")
        key = Console.ReadKey(True)
        _sw10 = key.KeyChar
        if _sw10 == "0":
            return
        elif _sw10 == "1":
            st.itemInventory["お守り"] = st.itemInventory.get("お守り", 0) + 1
            DevMsg("お守り +1")
        elif _sw10 == "2":
            st.itemInventory["幸運のコイン"] = st.itemInventory.get("幸運のコイン", 0) + 1
            DevMsg("幸運のコイン +1")
        elif _sw10 == "3":
            st.itemInventory["返済猶予券"] = st.itemInventory.get("返済猶予券", 0) + 1
            DevMsg("返済猶予券 +1")
        elif _sw10 == "4":
            st.hasGreedRing = True
            st.greedRingEquipped = True
            DevMsg("強欲の指輪 入手・装備")
        elif _sw10 == "5":
            st.hasDevilCoin = True
            st.hasBloodAmulet = True
            st.hasDeathRing = True
            st.hasTimeClock = True
            st.hasOracleBall = True
            st.cursedItemCount = 5
            DevMsg("呪いアイテム全入手")
        elif _sw10 == "6":
            allSymbols = [ "スライム", "ゴーレム", "ドラゴン", "フェニックス", "ユニコーン", "悪魔", "天使", "神" ]
            for s in allSymbols:
                if not (s in st.unlockedSymbols):
                    st.unlockedSymbols.append(s)
            DevMsg("全シンボル解放")
        elif _sw10 == "7":
            allEvents = [ "設定6解放", "VIPルーム解放", "地下カジノ解放", "夢カジノ解放", "悪魔契約1", "悪魔契約2", "悪魔契約3", "OVERFLOW END", "RTA達成", "謎の女性", "777達成", "GOD MODE", "TRUE END" ]
            for e in allEvents:
                if not (e in st.unlockedEvents):
                    st.unlockedEvents.append(e)
            DevMsg(f"イベント {len(st.unlockedEvents)}件解放")
        elif _sw10 == "8":
            st.itemInventory["お守り"] = 0
            st.itemInventory["幸運のコイン"] = 0
            st.itemInventory["返済猶予券"] = 0
            st.hasGreedRing = False
            st.greedRingEquipped = False
            st.hasDevilCoin = False
            st.hasBloodAmulet = False
            st.hasDeathRing = False
            st.hasTimeClock = False
            st.hasOracleBall = False
            st.cursedItemCount = 0
            DevMsg("アイテム全クリア")
# ========== [4] スロット設定 ==========

def DevSlotMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  ═══ スロット設定 ═══\n")
        Console.WriteLine(f"  totalSpins        = {st.totalSpins}")
        Console.WriteLine(f"  consecutiveWins   = {st.consecutiveWins}")
        Console.WriteLine(f"  consecutiveLosses = {st.consecutiveLosses}")
        Console.WriteLine(f"  total777Count     = {st.total777Count}")
        Console.WriteLine(f"  bigWinCount       = {st.bigWinCount}")
        Console.WriteLine(f"  godMode           = {st.godMode}  残り={st.godModeRemaining}")
        Console.WriteLine(f"  luckyTimeActive   = {st.luckyTimeActive}  残り={st.luckyTimeRemaining}")
        Console.WriteLine("\n  [1] totalSpins を設定")
        Console.WriteLine("  [2] 連続勝利数を設定")
        Console.WriteLine("  [3] 777回数を設定")
        Console.WriteLine("  [4] GOD MODE 即発動 (10ターン)")
        Console.WriteLine("  [5] LUCKY TIME 即発動 (10ターン)")
        Console.WriteLine("  [6] GOD MODE 解除")
        Console.WriteLine("  [7] LUCKY TIME 解除")
        Console.WriteLine("  [0] 戻る")
        Console.ResetColor()
        Console.Write("\n  選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            return
        Console.CursorVisible = True
        Console.WriteLine()
        _sw11 = key.KeyChar
        if _sw11 == "1":
            Console.Write("  totalSpins > ")
            if ((sp := try_parse_int(Console.ReadLine())) is not None):
                st.totalSpins = sp
                DevMsg(f"totalSpins = {sp}")
        elif _sw11 == "2":
            Console.Write("  連続勝利数 > ")
            if ((cw := try_parse_int(Console.ReadLine())) is not None):
                st.consecutiveWins = cw
                DevMsg(f"consecutiveWins = {cw}")
        elif _sw11 == "3":
            Console.Write("  777回数 > ")
            if ((s7 := try_parse_int(Console.ReadLine())) is not None):
                st.total777Count = s7
                DevMsg(f"total777Count = {s7}")
        elif _sw11 == "4":
            st.godMode = True
            st.godModeRemaining = 10
            DevMsg("GOD MODE 発動 (10ターン)")
        elif _sw11 == "5":
            st.luckyTimeActive = True
            st.luckyTimeRemaining = 10
            DevMsg("LUCKY TIME 発動 (10ターン)")
        elif _sw11 == "6":
            st.godMode = False
            st.godModeRemaining = 0
            DevMsg("GOD MODE 解除")
        elif _sw11 == "7":
            st.luckyTimeActive = False
            st.luckyTimeRemaining = 0
            DevMsg("LUCKY TIME 解除")
        Console.CursorVisible = False
# ========== [5] 時間・ターン設定 ==========

def DevTimeMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine("\n  ═══ 時間・ターン設定 ═══\n")
        Console.WriteLine(f"  debtTurnsRemaining     = {st.debtTurnsRemaining}")
        Console.WriteLine(f"  devilContractTurns     = {st.devilContractTurns}")
        Console.WriteLine(f"  devilContractType      = {st.devilContractType}")
        Console.WriteLine(f"  contract1WinCount      = {st.contract1WinCount}")
        Console.WriteLine(f"  dreamLayerCleared      = {st.dreamLayerCleared}")
        Console.WriteLine(f"  undergroundVisits      = {st.undergroundVisits}")
        Console.WriteLine(f"  vipTotalVisits         = {st.vipTotalVisits}")
        Console.WriteLine(f"  autoSaveTurns          = {st.autoSaveTurns}")
        Console.WriteLine("\n  [1] 借金返済ターン数を設定")
        Console.WriteLine("  [2] 悪魔契約ターン数を設定")
        Console.WriteLine("  [3] 夢カジノクリア層数を設定")
        Console.WriteLine("  [4] 地下カジノ訪問回数を設定")
        Console.WriteLine("  [5] VIP訪問回数を設定")
        Console.WriteLine("  [6] 契約1勝利カウントを設定")
        Console.WriteLine("  [0] 戻る")
        Console.ResetColor()
        Console.Write("\n  選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            return
        Console.CursorVisible = True
        Console.WriteLine()
        _sw12 = key.KeyChar
        if _sw12 == "1":
            Console.Write("  借金返済ターン数 > ")
            if ((dt := try_parse_int(Console.ReadLine())) is not None):
                st.debtTurnsRemaining = dt
                DevMsg(f"debtTurnsRemaining = {dt}")
        elif _sw12 == "2":
            Console.Write("  悪魔契約ターン数 > ")
            if ((dct := try_parse_int(Console.ReadLine())) is not None):
                st.devilContractTurns = dct
                DevMsg(f"devilContractTurns = {dct}")
        elif _sw12 == "3":
            Console.Write("  夢カジノクリア層 (0-5) > ")
            if ((dl := try_parse_int(Console.ReadLine())) is not None):
                st.dreamLayerCleared = Math.Clamp(dl, 0, 5)
                DevMsg(f"dreamLayerCleared = {st.dreamLayerCleared}")
        elif _sw12 == "4":
            Console.Write("  地下カジノ訪問回数 > ")
            if ((uv := try_parse_int(Console.ReadLine())) is not None):
                st.undergroundVisits = uv
                DevMsg(f"undergroundVisits = {uv}")
        elif _sw12 == "5":
            Console.Write("  VIP訪問回数 > ")
            if ((vv := try_parse_int(Console.ReadLine())) is not None):
                st.vipTotalVisits = vv
                DevMsg(f"vipTotalVisits = {vv}")
        elif _sw12 == "6":
            Console.Write("  契約1勝利カウント > ")
            if ((c1 := try_parse_int(Console.ReadLine())) is not None):
                st.contract1WinCount = c1
                DevMsg(f"contract1WinCount = {c1}")
        Console.CursorVisible = False
# ========== [6] デバッグ情報表示 ==========

def DevDebugInfo():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine("\n  ════════════════════════════════════")
    Console.WriteLine("       DEV DEBUG INFO")
    Console.WriteLine("  ════════════════════════════════════")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine(f"  playerName          = {st.playerName}")
    Console.WriteLine(f"  money               = {st.money:,}")
    Console.WriteLine(f"  debt                = {st.debt:,}")
    Console.WriteLine(f"  setting             = {st.setting}")
    Console.WriteLine(f"  totalSpins          = {st.totalSpins}")
    Console.WriteLine(f"  totalWinAmount      = {st.totalWinAmount:,}")
    Console.WriteLine(f"  totalLoseAmount     = {st.totalLoseAmount:,}")
    Console.WriteLine(f"  addictionLevel      = {st.addictionLevel}%")
    Console.WriteLine(f"  consecutiveWins     = {st.consecutiveWins}")
    Console.WriteLine(f"  consecutiveLosses   = {st.consecutiveLosses}")
    Console.WriteLine(f"  total777Count       = {st.total777Count}")
    Console.WriteLine(f"  maxMoney            = {st.maxMoney:,}")
    Console.WriteLine(f"  maxDebt             = {st.maxDebt:,}")
    Console.WriteLine(f"  godMode             = {st.godMode} ({st.godModeRemaining}残)")
    Console.WriteLine(f"  luckyTimeActive     = {st.luckyTimeActive} ({st.luckyTimeRemaining}残)")
    Console.WriteLine(f"  vipRoomUnlocked     = {st.vipRoomUnlocked}")
    Console.WriteLine(f"  undergroundUnlocked = {st.undergroundUnlocked}")
    Console.WriteLine(f"  dreamCasinoUnlocked = {st.dreamCasinoUnlocked}")
    Console.WriteLine(f"  dreamLayerCleared   = {st.dreamLayerCleared}")
    Console.WriteLine(f"  devilContractActive = {st.devilContractActive} (type={st.devilContractType})")
    Console.WriteLine(f"  cursedItemCount     = {st.cursedItemCount}")
    Console.WriteLine(f"  unlockedSymbols     = {len(st.unlockedSymbols)}種")
    Console.WriteLine(f"  unlockedEvents      = {len(st.unlockedEvents)}件")
    Console.WriteLine(f"  missions completed  = {sum(1 for m in st.missions if m.Completed)} / {len(st.missions)}")
    Console.ForegroundColor = ConsoleColor.DarkGreen
    Console.WriteLine("\n  ════════════════════════════════════")
    Console.WriteLine("  [何かキー] 戻る")
    Console.ResetColor()
    Console.ReadKey(True)
# ========== [7] 全解放 ==========

def DevUnlockAll():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n  全解放しますか？ [Y/N]")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key != ConsoleKey.Y:
        return
    st.money = 999999
    st.debt = 0
    st.debtTurnsRemaining = 0
    st.addictionLevel = 0
    st.isAddicted = False
    st.setting = 6
    st.godMode = True
    st.godModeRemaining = 999
    st.luckyTimeActive = True
    st.luckyTimeRemaining = 999
    st.vipRoomUnlocked = True
    st.undergroundUnlocked = True
    st.dreamCasinoUnlocked = True
    st.dreamLayerCleared = 5
    st.hasGreedRing = True
    st.greedRingEquipped = True
    st.hasDevilCoin = True
    st.hasBloodAmulet = True
    st.hasDeathRing = True
    st.hasTimeClock = True
    st.hasOracleBall = True
    st.cursedItemCount = 5
    st.total777Count = 5
    st.totalSpins = 200
    st.hasEverBorrowedMoney = True
    st.hasUsedRehab = True
    st.vipTotalVisits = 10
    st.vipTotalWins = 5
    st.vipTotalSpins = 30
    st.undergroundVisits = 5
    st.undergroundWins = 3
    st.itemInventory["お守り"] = 9
    st.itemInventory["幸運のコイン"] = 9
    st.itemInventory["返済猶予券"] = 9
    allSymbols = [ "スライム", "ゴーレム", "ドラゴン", "フェニックス", "ユニコーン", "悪魔", "天使", "神" ]
    for s in allSymbols:
        if not (s in st.unlockedSymbols):
            st.unlockedSymbols.append(s)
    for m in st.missions:
        m.Completed = True
    DevMsg("全解放完了！")
# ========== [8] 全リセット ==========

def DevResetAll():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n  全フラグをリセットしますか？ [Y/N]")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.Key != ConsoleKey.Y:
        return
    st.money = 1000
    st.debt = 0
    st.debtTurnsRemaining = 0
    st.addictionLevel = 0
    st.isAddicted = False
    st.setting = 0
    st.godMode = False
    st.godModePermanent = False
    st.godModeRemaining = 0
    st.luckyTimeActive = False
    st.luckyTimeRemaining = 0
    st.vipRoomUnlocked = False
    st.isInVIPRoom = False
    st.undergroundUnlocked = False
    st.isInUnderground = False
    st.dreamCasinoUnlocked = False
    st.dreamLayerCleared = 0
    st.hasGreedRing = False
    st.greedRingEquipped = False
    st.hasDevilCoin = False
    st.hasBloodAmulet = False
    st.hasDeathRing = False
    st.hasTimeClock = False
    st.hasOracleBall = False
    st.cursedItemCount = 0
    st.total777Count = 0
    st.totalSpins = 0
    st.consecutiveWins = 0
    st.consecutiveLosses = 0
    st.hasEverBorrowedMoney = False
    st.hasUsedRehab = False
    st.devilContractActive = False
    st.devilContractOffered = False
    st.devilContractSuccess = False
    st.contract1Complete = False
    st.itemInventory["お守り"] = 0
    st.itemInventory["幸運のコイン"] = 0
    st.itemInventory["返済猶予券"] = 0
    st.unlockedSymbols.clear()
    st.unlockedSymbols.append("スライム")
    st.unlockedSymbols.append("ゴーレム")
    st.unlockedEvents.clear()
    for m in st.missions:
        m.Completed = False
    DevMsg("全フラグリセット完了")
# ========== イベントギャラリー ==========

def DevEventGallery():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n  ╔══════════════════════════════════════╗")
        Console.WriteLine("  ║       EVENT GALLERY                  ║")
        Console.WriteLine("  ╠══════════════════════════════════════╣")
        Console.ResetColor()
        Console.WriteLine("  ║  [1] チャプター1（最初の会話）       ║")
        Console.WriteLine("  ║  [2] 廃娯楽施設 1階                  ║")
        Console.WriteLine("  ║  [3] 廃娯楽施設 2階                  ║")
        Console.WriteLine("  ║  [4] 廃娯楽施設 3階                  ║")
        Console.WriteLine("  ║  [5] 地下室イベント（時計必要）      ║")
        Console.WriteLine("  ║  [6] クソエンディング（ごめん）      ║")
        Console.WriteLine("  ║  [7] エンディングA（ここにいるから） ║")
        Console.WriteLine("  ║  [8] エンディングB（行こ）           ║")
        Console.WriteLine("  ║  [9] BAD END（そういう人だったんだ） ║")
        Console.WriteLine("  ║  [A] 無垢な宝石 入手演出             ║")
        Console.WriteLine("  ║  [B] 虚栄のカギ 購入演出             ║")
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("  ╚══════════════════════════════════════╝")
        Console.ResetColor()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n  ※ 必要なフラグは自動でセットされます")
        Console.ResetColor()
        Console.Write("  > ")
        key = Console.ReadKey(True)
        Console.clear()
        _sw13 = key.KeyChar
        if _sw13 == "1":
            st.chapter1Seen = False
            events.Chapter1_FirstConversation()
        elif _sw13 == "2":
            st.hasInnocentGem = True
            st.vanityKeyPurchased = True
            st.abandonedCasinoUnlocked = True
            st.abandonedCasinoEntered = False
            if len(st.roomsOpened[0]) < 5:
                st.roomsOpened[0] = ([False] * 5)
            st.money = Math.Max(st.money, 10000)
            DevGalleryFloor1()
            continue
        elif _sw13 == "3":
            st.hasInnocentGem = True
            st.abandonedCasinoUnlocked = True
            st.abandonedCasinoEntered = True
            st.roomsOpened[0] = [ True, True, True, True, True ]
            if len(st.roomsOpened[1]) < 5:
                st.roomsOpened[1] = ([False] * 5)
            st.money = Math.Max(st.money, 20000)
            DevGalleryFloor2()
            continue
        elif _sw13 == "4":
            st.hasInnocentGem = True
            st.abandonedCasinoUnlocked = True
            st.abandonedCasinoEntered = True
            st.roomsOpened[0] = [ True, True, True, True, True ]
            st.roomsOpened[1] = [ True, True, True, True, True ]
            if len(st.roomsOpened[2]) < 5:
                st.roomsOpened[2] = ([False] * 5)
            st.money = Math.Max(st.money, 30000)
            DevGalleryFloor3()
            continue
        elif _sw13 == "5":
            st.hasInnocentGem = True
            st.timeClockEquipped = True
            st.hasTimeClock = True
            abandoned.BasementDoorFound()
        elif _sw13 == "6":
            st.hasInnocentGem = True
            st.timeClockEquipped = False
            st.roomsOpened[2] = [ True, True, True, True, True ]
            abandoned.AbandonedCasinoExitEvent()
        elif _sw13 == "7":
            st.hasInnocentGem = False
            st.hasJewelRing = True
            abandoned.EndingRouteA_Owner()
        elif _sw13 == "8":
            st.hasInnocentGem = False
            st.hasJewelRing = True
            abandoned.EndingRouteB_Bell()
        elif _sw13 == "9":
            st.hasInnocentGem = True
            st.hasExchangedMoney = False
            st.money = Math.Max(st.money, 5000)
            shop.BuyExchangedMoney()
        elif _sw13 in ("a", "A"):
            st.hasInnocentGem = False
            events.InnocentGemFound()
        elif _sw13 in ("b", "B"):
            st.chapter1Seen = True
            st.vanityKeyPurchased = False
            st.abandonedCasinoUnlocked = False
            st.money = Math.Max(st.money, 5000)
            shop.ShopHiddenPage()
        elif _sw13 == "0":
            return
        else:
            continue
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n\n  ── イベント終了 ──")
        Console.WriteLine("\n  [何かキー] ギャラリーに戻る")
        Console.ResetColor()
        Console.ReadKey(True)

def DevGalleryFloor1():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n  ── 廃娯楽施設 1階 ──")
        Console.ResetColor()
        Console.WriteLine("\n  [1] 部屋A：笑ってる女の子の絵")
        Console.WriteLine("  [2] 部屋B：片方だけの靴")
        Console.WriteLine("  [3] 部屋C：大きな手と小さな手")
        Console.WriteLine("  [4] 部屋D：ベルと書いた紙")
        Console.WriteLine("  [5] 最終部屋：全部繋がる")
        Console.WriteLine("  [6] 1階まるごと（入口から）")
        Console.WriteLine("  [0] 戻る")
        Console.Write("\n  > ")
        k = Console.ReadKey(True)
        Console.clear()
        _sw14 = k.KeyChar
        if _sw14 == "1":
            st.roomsOpened[0][0] = False
            abandoned.OpenRoom(0, 0, 0, abandoned.Room1F_A)
        elif _sw14 == "2":
            st.roomsOpened[0][1] = False
            abandoned.OpenRoom(0, 1, 0, abandoned.Room1F_B)
        elif _sw14 == "3":
            st.roomsOpened[0][2] = False
            abandoned.OpenRoom(0, 2, 0, abandoned.Room1F_C)
        elif _sw14 == "4":
            st.roomsOpened[0][3] = False
            abandoned.OpenRoom(0, 3, 0, abandoned.Room1F_D)
        elif _sw14 == "5":
            st.roomsOpened[0] = [ True, True, True, True, False ]
            abandoned.OpenRoom(0, 4, 0, abandoned.Room1F_Final)
        elif _sw14 == "6":
            st.abandonedCasinoEntered = False
            st.roomsOpened[0] = ([False] * 5)
            abandoned.EnterAbandonedCasino()
            return
        elif _sw14 == "0":
            return
        else:
            continue
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る")
        Console.ResetColor()
        Console.ReadKey(True)

def DevGalleryFloor2():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n  ── 廃娯楽施設 2階 ──")
        Console.ResetColor()
        Console.WriteLine("\n  [1] 部屋A：古いコート")
        Console.WriteLine("  [2] 部屋B：二人で食卓")
        Console.WriteLine("  [3] 部屋C：半分の本")
        Console.WriteLine("  [4] 部屋D：空っぽの椅子")
        Console.WriteLine("  [5] 最終部屋：また来る")
        Console.WriteLine("  [6] 2階まるごと（入口から）")
        Console.WriteLine("  [0] 戻る")
        Console.Write("\n  > ")
        k = Console.ReadKey(True)
        Console.clear()
        _sw15 = k.KeyChar
        if _sw15 == "1":
            st.roomsOpened[1][0] = False
            abandoned.OpenRoom(1, 0, 0, abandoned.Room2F_A)
        elif _sw15 == "2":
            st.roomsOpened[1][1] = False
            abandoned.OpenRoom(1, 1, 0, abandoned.Room2F_B)
        elif _sw15 == "3":
            st.roomsOpened[1][2] = False
            abandoned.OpenRoom(1, 2, 0, abandoned.Room2F_C)
        elif _sw15 == "4":
            st.roomsOpened[1][3] = False
            abandoned.OpenRoom(1, 3, 0, abandoned.Room2F_D)
        elif _sw15 == "5":
            st.roomsOpened[1] = [ True, True, True, True, False ]
            abandoned.OpenRoom(1, 4, 0, abandoned.Room2F_Final)
        elif _sw15 == "6":
            st.roomsOpened[1] = ([False] * 5)
            abandoned.GoToFloor2()
            return
        elif _sw15 == "0":
            return
        else:
            continue
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る")
        Console.ResetColor()
        Console.ReadKey(True)

def DevGalleryFloor3():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n  ── 廃娯楽施設 3階 ──")
        Console.ResetColor()
        Console.WriteLine("\n  [1] 部屋A：使い込まれたエプロン")
        Console.WriteLine("  [2] 部屋B：仕事中のベル（顔のない絵）")
        Console.WriteLine("  [3] 部屋C：折れたネームプレート")
        Console.WriteLine("  [4] 部屋D：窓のない部屋に星")
        Console.WriteLine("  [5] 最終部屋：オーナーの手紙")
        Console.WriteLine("  [6] 3階まるごと（入口から）")
        Console.WriteLine("  [0] 戻る")
        Console.Write("\n  > ")
        k = Console.ReadKey(True)
        Console.clear()
        _sw16 = k.KeyChar
        if _sw16 == "1":
            st.roomsOpened[2][0] = False
            abandoned.OpenRoom(2, 0, 0, abandoned.Room3F_A)
        elif _sw16 == "2":
            st.roomsOpened[2][1] = False
            abandoned.OpenRoom(2, 1, 0, abandoned.Room3F_B)
        elif _sw16 == "3":
            st.roomsOpened[2][2] = False
            abandoned.OpenRoom(2, 2, 0, abandoned.Room3F_C)
        elif _sw16 == "4":
            st.roomsOpened[2][3] = False
            abandoned.OpenRoom(2, 3, 0, abandoned.Room3F_D)
        elif _sw16 == "5":
            st.roomsOpened[2] = [ True, True, True, True, False ]
            abandoned.OpenRoom(2, 4, 0, abandoned.Room3F_Final)
        elif _sw16 == "6":
            st.roomsOpened[2] = ([False] * 5)
            abandoned.GoToFloor3()
            return
        elif _sw16 == "0":
            return
        else:
            continue
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGreen
        Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る")
        Console.ResetColor()
        Console.ReadKey(True)
# ========== DEV共通メッセージ ==========

def DevMsg(msg):
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine(f"\n  ✓ {msg}")
    Console.ResetColor()
    Thread.Sleep(800)
