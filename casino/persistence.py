# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — セーブ/ロード (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import missions as missions_mod

# ========== セーブ機能 ==========

def SaveGame(slot):
    try:
        if not Directory.Exists("saves"):
            Directory.CreateDirectory("saves")
        saveData = SaveData()
        saveData.PlayerName = st.playerName
        saveData.SaveDate = DateTimeNS.Now
        saveData.PlayTime = DateTimeNS.Now - st.startTime
        saveData.SaveSlot = slot
        saveData.Money = st.money
        saveData.Debt = st.debt
        saveData.MaxMoney = st.maxMoney
        saveData.MaxDebt = st.maxDebt
        saveData.TotalSpins = st.totalSpins
        saveData.Total777Count = st.total777Count
        saveData.ConsecutiveWins = st.consecutiveWins
        saveData.MaxConsecutiveWins = st.maxConsecutiveWins
        saveData.TotalWinAmount = st.totalWinAmount
        saveData.TotalLoseAmount = st.totalLoseAmount
        saveData.TotalLoses = st.totalLoses
        saveData.BigWinCount = st.bigWinCount
        saveData.Setting = st.setting
        saveData.DebtTurnsRemaining = st.debtTurnsRemaining
        saveData.HasEverBorrowedMoney = st.hasEverBorrowedMoney
        saveData.GodMode = st.godMode
        saveData.GodModeRemaining = st.godModeRemaining
        saveData.ConsecutiveHundredPlays = st.consecutiveHundredPlays
        saveData.LuckyTimeActive = st.luckyTimeActive
        saveData.LuckyTimeRemaining = st.luckyTimeRemaining
        saveData.HasSeenConversation = st.hasSeenConversation
        saveData.HasSeenMysteriousWoman = st.hasSeenMysteriousWoman
        saveData.ItemInventory = dict(st.itemInventory)
        saveData.TotalLuckyCoinsPurchased = st.totalLuckyCoinsPurchased
        saveData.HasGreedRing = st.hasGreedRing
        saveData.GreedRingEquipped = st.greedRingEquipped
        saveData.GreedRingLoseCount = st.greedRingLoseCount
        saveData.VipRoomUnlocked = st.vipRoomUnlocked
        saveData.IsInVIPRoom = st.isInVIPRoom
        saveData.VipConsecutiveLoses = st.vipConsecutiveLoses
        saveData.Vip777Count = st.vip777Count
        saveData.Vip5000BetWin = st.vip5000BetWin
        saveData.VipTotalVisits = st.vipTotalVisits
        saveData.VipTotalWins = st.vipTotalWins
        saveData.VipTotalSpins = st.vipTotalSpins
        saveData.HasSeenVIPDealer = st.hasSeenVIPDealer
        saveData.UndergroundUnlocked = st.undergroundUnlocked
        saveData.IsInUnderground = st.isInUnderground
        saveData.UndergroundVisits = st.undergroundVisits
        saveData.UndergroundWins = st.undergroundWins
        saveData.UndergroundAllInWin = st.undergroundAllInWin
        saveData.HasSeenUndergroundDealer = st.hasSeenUndergroundDealer
        saveData.DevilContractOffered = st.devilContractOffered
        saveData.DevilContractType = st.devilContractType
        saveData.DevilContractActive = st.devilContractActive
        saveData.DevilContractTurns = st.devilContractTurns
        saveData.ContractStartTime = st.contractStartTime
        saveData.Contract1Complete = st.contract1Complete
        saveData.DevilContractSuccess = st.devilContractSuccess
        saveData.AddictionLevel = st.addictionLevel
        saveData.IsAddicted = st.isAddicted
        saveData.AddictionWarningCount = st.addictionWarningCount
        saveData.HasUsedRehab = st.hasUsedRehab
        saveData.CursedItemCount = st.cursedItemCount
        saveData.HasDevilCoin = st.hasDevilCoin
        saveData.DevilCoinCurse = st.devilCoinCurse
        saveData.DevilCoinWin = st.devilCoinWin
        saveData.HasBloodAmulet = st.hasBloodAmulet
        saveData.BloodAmuletLoses = st.bloodAmuletLoses
        saveData.BloodAmulet5Wins = st.bloodAmulet5Wins
        saveData.HasDeathRing = st.hasDeathRing
        saveData.DeathRing10Wins = st.deathRing10Wins
        saveData.HasTimeClock = st.hasTimeClock
        saveData.HasOracleBall = st.hasOracleBall
        saveData.OracleBallPrediction = st.oracleBallPrediction
        saveData.DevilCoinActive = st.devilCoinActive
        saveData.BloodAmuletEquipped = st.bloodAmuletEquipped
        saveData.DeathRingEquipped = st.deathRingEquipped
        saveData.TimeClockEquipped = st.timeClockEquipped
        saveData.MetaEventCount = st.metaEventCount
        saveData.UnlockedSymbols = list(st.unlockedSymbols)
        saveData.UnlockedEvents = list(st.unlockedEvents)
        saveData.UndergroundConsecutiveLoses = st.undergroundConsecutiveLoses
        saveData.UndergroundTotalSpins = st.undergroundTotalSpins
        saveData.UndergroundCursedMode = st.undergroundCursedMode
        saveData.Missions = make_mission_savedata_list(st.missions)
        saveData.Rankings = list(st.rankings)
        saveData.TrueEndingUnlocked = st.trueEndingUnlocked
        saveData.GodModePermanent = st.godModePermanent
        saveData.Contract1WinCount = st.contract1WinCount
        saveData.Contract2Deadline = st.contract2Deadline
        saveData.Contract2OriginalDebt = st.contract2OriginalDebt
        saveData.OverflowCleared = st.overflowCleared
        saveData.RtaCleared = st.rtaCleared
        saveData.GameStartTime = st.gameStartTime
        saveData.ShopVisitCount = st.shopVisitCount
        saveData.ShopCloseWithoutBuyCount = st.shopCloseWithoutBuyCount
        saveData.BellMetFirst = st.bellMetFirst
        saveData.MissionOpenCount = st.missionOpenCount
        saveData.GodModeActivateCount = st.godModeActivateCount
        saveData.DreamCasinoUnlocked = st.dreamCasinoUnlocked
        saveData.DreamLayerCleared = st.dreamLayerCleared
        saveData.MushroomManMet = st.mushroomManMet
        saveData.LuckyCoinsTotal = st.luckyCoinsTotal
        saveData.ConsecutiveLosses = st.consecutiveLosses
        saveData.Chapter1Seen = st.chapter1Seen
        saveData.MemoryFragmentsCleared = st.memoryFragmentsCleared
        saveData.BlackSuitIntroduced = st.blackSuitIntroduced
        saveData.AbandonedCasinoUnlocked = st.abandonedCasinoUnlocked
        saveData.AbandonedCasinoEntered = st.abandonedCasinoEntered
        saveData.VanityKeyPurchased = st.vanityKeyPurchased
        saveData.RoomsOpened = st.roomsOpened
        saveData.HasInnocentGem = st.hasInnocentGem
        saveData.HasJewelRing = st.hasJewelRing
        saveData.HasExchangedMoney = st.hasExchangedMoney
        saveData.HasUnknownCoin = st.hasUnknownCoin
        saveData.UnknownCoinFlipCount = st.unknownCoinFlipCount
        saveData.BellRouteACompleted = st.bellRouteACompleted
        saveData.BellRouteBCompleted = st.bellRouteBCompleted
        json = json_serialize(saveData)
        File.WriteAllText(f"saves/save_{slot}.json", json)
        if slot != 0:  # オートセーブ以外
            Console.clear()
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine("\n\n\n")
            Console.WriteLine("    ╔═══════════════════════════════╗")
            Console.WriteLine("    ║                               ║")
            Console.WriteLine(f"   ║ スロット{slot}にセーブ完了！  ║")
            Console.WriteLine("    ║                               ║")
            Console.WriteLine("    ╚═══════════════════════════════╝")
            Console.ResetColor()
            Console.WriteLine(f"\n    日時: {saveData.SaveDate:yyyy/MM/dd HH:mm:ss}")
            Console.WriteLine(f"    所持金: {st.money}G")
            Console.WriteLine(f"    総回転数: {st.totalSpins}回")
            Thread.Sleep(2000)
    except Exception as ex:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"\n\nセーブに失敗しました: {ex}")
        Console.ResetColor()
        Thread.Sleep(2000)
# ========== ロード機能 ==========

def LoadGame(slot):
    try:
        filePath = f"saves/save_{slot}.json"
        if not File.Exists(filePath):
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"\n\nスロット{slot}にセーブデータがありません")
            Console.ResetColor()
            Thread.Sleep(1500)
            return False
        json = File.ReadAllText(filePath)
        saveData = json_deserialize_savedata(json)
        if saveData == None:
            return False
        st.playerName = saveData.PlayerName
        st.startTime = DateTimeNS.Now - saveData.PlayTime
        st.money = saveData.Money
        st.debt = saveData.Debt
        st.maxMoney = saveData.MaxMoney
        st.maxDebt = saveData.MaxDebt
        st.totalSpins = saveData.TotalSpins
        st.total777Count = saveData.Total777Count
        st.consecutiveWins = saveData.ConsecutiveWins
        st.maxConsecutiveWins = saveData.MaxConsecutiveWins
        st.totalWinAmount = saveData.TotalWinAmount
        st.totalLoseAmount = saveData.TotalLoseAmount
        st.totalLoses = saveData.TotalLoses
        st.bigWinCount = saveData.BigWinCount
        st.setting = saveData.Setting
        st.debtTurnsRemaining = saveData.DebtTurnsRemaining
        st.hasEverBorrowedMoney = saveData.HasEverBorrowedMoney
        st.godMode = saveData.GodMode
        st.godModeRemaining = saveData.GodModeRemaining
        st.consecutiveHundredPlays = saveData.ConsecutiveHundredPlays
        st.luckyTimeActive = saveData.LuckyTimeActive
        st.luckyTimeRemaining = saveData.LuckyTimeRemaining
        st.hasSeenConversation = saveData.HasSeenConversation
        st.hasSeenMysteriousWoman = saveData.HasSeenMysteriousWoman
        st.itemInventory = dict(saveData.ItemInventory)
        st.totalLuckyCoinsPurchased = saveData.TotalLuckyCoinsPurchased
        st.hasGreedRing = saveData.HasGreedRing
        st.greedRingEquipped = saveData.GreedRingEquipped
        st.greedRingLoseCount = saveData.GreedRingLoseCount
        st.vipRoomUnlocked = saveData.VipRoomUnlocked
        st.isInVIPRoom = saveData.IsInVIPRoom
        st.vipConsecutiveLoses = saveData.VipConsecutiveLoses
        st.vip777Count = saveData.Vip777Count
        st.vip5000BetWin = saveData.Vip5000BetWin
        st.vipTotalVisits = saveData.VipTotalVisits
        st.vipTotalWins = saveData.VipTotalWins
        st.vipTotalSpins = saveData.VipTotalSpins
        st.hasSeenVIPDealer = saveData.HasSeenVIPDealer
        st.undergroundUnlocked = saveData.UndergroundUnlocked
        st.isInUnderground = saveData.IsInUnderground
        st.undergroundVisits = saveData.UndergroundVisits
        st.undergroundWins = saveData.UndergroundWins
        st.undergroundAllInWin = saveData.UndergroundAllInWin
        st.hasSeenUndergroundDealer = saveData.HasSeenUndergroundDealer
        st.devilContractOffered = saveData.DevilContractOffered
        st.devilContractType = saveData.DevilContractType
        st.devilContractActive = saveData.DevilContractActive
        st.devilContractTurns = saveData.DevilContractTurns
        st.contractStartTime = saveData.ContractStartTime
        st.contract1Complete = saveData.Contract1Complete
        st.devilContractSuccess = saveData.DevilContractSuccess
        st.addictionLevel = saveData.AddictionLevel
        st.isAddicted = saveData.IsAddicted
        st.addictionWarningCount = saveData.AddictionWarningCount
        st.hasUsedRehab = saveData.HasUsedRehab
        st.cursedItemCount = saveData.CursedItemCount
        st.hasDevilCoin = saveData.HasDevilCoin
        st.devilCoinCurse = saveData.DevilCoinCurse
        st.devilCoinWin = saveData.DevilCoinWin
        st.hasBloodAmulet = saveData.HasBloodAmulet
        st.bloodAmuletLoses = saveData.BloodAmuletLoses
        st.bloodAmulet5Wins = saveData.BloodAmulet5Wins
        st.hasDeathRing = saveData.HasDeathRing
        st.deathRing10Wins = saveData.DeathRing10Wins
        st.hasTimeClock = saveData.HasTimeClock
        st.hasOracleBall = saveData.HasOracleBall
        st.oracleBallPrediction = saveData.OracleBallPrediction
        st.devilCoinActive = saveData.DevilCoinActive
        st.bloodAmuletEquipped = saveData.BloodAmuletEquipped
        st.deathRingEquipped = saveData.DeathRingEquipped
        st.timeClockEquipped = saveData.TimeClockEquipped
        st.metaEventCount = saveData.MetaEventCount
        st.unlockedSymbols = list(saveData.UnlockedSymbols)
        st.unlockedEvents = list(saveData.UnlockedEvents)
        st.undergroundConsecutiveLoses = saveData.UndergroundConsecutiveLoses
        st.undergroundTotalSpins = saveData.UndergroundTotalSpins
        st.undergroundCursedMode = saveData.UndergroundCursedMode
        st.missions.clear()
        missions_mod.InitializeMissions()
        for i in range(0, min(len(saveData.Missions), len(st.missions))):
            st.missions[i].Completed = saveData.Missions[i].Completed
            st.missions[i].Name = saveData.Missions[i].Name
            st.missions[i].Description = saveData.Missions[i].Description
        st.rankings = list(saveData.Rankings)
        st.trueEndingUnlocked = saveData.TrueEndingUnlocked
        st.godModePermanent = saveData.GodModePermanent
        st.contract1WinCount = saveData.Contract1WinCount
        st.contract2Deadline = saveData.Contract2Deadline
        st.contract2OriginalDebt = saveData.Contract2OriginalDebt
        st.overflowCleared = saveData.OverflowCleared
        st.rtaCleared = saveData.RtaCleared
        st.gameStartTime = saveData.GameStartTime
        st.shopVisitCount = saveData.ShopVisitCount
        st.shopCloseWithoutBuyCount = saveData.ShopCloseWithoutBuyCount
        st.bellMetFirst = saveData.BellMetFirst
        st.missionOpenCount = saveData.MissionOpenCount
        st.godModeActivateCount = saveData.GodModeActivateCount
        st.dreamCasinoUnlocked = saveData.DreamCasinoUnlocked
        st.dreamLayerCleared = saveData.DreamLayerCleared
        st.mushroomManMet = saveData.MushroomManMet
        st.luckyCoinsTotal = saveData.LuckyCoinsTotal
        st.consecutiveLosses = saveData.ConsecutiveLosses
        st.chapter1Seen = saveData.Chapter1Seen
        st.memoryFragmentsCleared = saveData.MemoryFragmentsCleared
        st.blackSuitIntroduced = saveData.BlackSuitIntroduced
        st.abandonedCasinoUnlocked = saveData.AbandonedCasinoUnlocked
        st.abandonedCasinoEntered = saveData.AbandonedCasinoEntered
        st.vanityKeyPurchased = saveData.VanityKeyPurchased
        if saveData.RoomsOpened != None:
            st.roomsOpened = saveData.RoomsOpened
        st.hasInnocentGem = saveData.HasInnocentGem
        st.hasJewelRing = saveData.HasJewelRing
        st.hasExchangedMoney = saveData.HasExchangedMoney
        st.hasUnknownCoin = saveData.HasUnknownCoin
        st.unknownCoinFlipCount = saveData.UnknownCoinFlipCount
        st.bellRouteACompleted = saveData.BellRouteACompleted
        st.bellRouteBCompleted = saveData.BellRouteBCompleted
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ╔═══════════════════════════════╗")
        Console.WriteLine("    ║                               ║")
        Console.WriteLine(f"   ║ スロット{slot}からロード完了！║")
        Console.WriteLine("    ║                               ║")
        Console.WriteLine("    ╚═══════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine(f"\n    プレイヤー: {st.playerName}")
        Console.WriteLine(f"    セーブ日時: {saveData.SaveDate:yyyy/MM/dd HH:mm:ss}")
        Console.WriteLine(f"    所持金: {st.money}G")
        Console.WriteLine(f"    総回転数: {st.totalSpins}回")
        Thread.Sleep(2500)
        return True
    except Exception as ex:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"\n\nロードに失敗しました: {ex}")
        Console.ResetColor()
        Thread.Sleep(2000)
        return False
# ========== セーブメニュー ==========

def SaveMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║          💾 セーブ 💾            ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine(f"\n所持金: {st.money}G\n")
        Console.WriteLine("【セーブスロット選択】\n")
        for i in range(1, (3) + 1):
            Console.WriteLine(f"  [{i}] スロット{i}")
            filePath = f"saves/save_{i}.json"
            if File.Exists(filePath):
                try:
                    json = File.ReadAllText(filePath)
                    saveData = coalesce_throw(json_deserialize_savedata(json), Exception("データが空です"))
                    Console.ForegroundColor = ConsoleColor.Yellow
                    Console.WriteLine(f"      名前: {saveData.PlayerName}")
                    Console.WriteLine(f"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}")
                    Console.WriteLine(f"      所持金: {saveData.Money}G")
                    Console.WriteLine(f"      回転数: {saveData.TotalSpins}回")
                    Console.ResetColor()
                except Exception:
                    Console.ForegroundColor = ConsoleColor.Red
                    Console.WriteLine("      [データ破損]")
                    Console.ResetColor()
            else:
                Console.ForegroundColor = ConsoleColor.DarkGray
                Console.WriteLine("      [空きスロット]")
                Console.ResetColor()
            Console.WriteLine()
        Console.WriteLine("  [0] 戻る\n")
        Console.Write("選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            break
        elif key.KeyChar >= "1" and key.KeyChar <= "3":
            slot = cs_int_parse(str(key.KeyChar))
            if File.Exists(f"saves/save_{slot}.json"):
                Console.WriteLine(f"\n\nスロット{slot}に上書きしますか？ [Y/N]")
                confirm = Console.ReadKey(True)
                if confirm.Key != ConsoleKey.Y:
                    continue
            SaveGame(slot)
            break
# ========== ロードメニュー ==========

def LoadMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║          📂 ロード 📂            ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine("\n【ロードスロット選択】\n")
        hasAnySave = False
        for i in range(1, (3) + 1):
            filePath = f"saves/save_{i}.json"
            if File.Exists(filePath):
                hasAnySave = True
                Console.WriteLine(f"  [{i}] スロット{i}")
                try:
                    json = File.ReadAllText(filePath)
                    saveData = coalesce_throw(json_deserialize_savedata(json), Exception("データが空です"))
                    Console.ForegroundColor = ConsoleColor.Yellow
                    Console.WriteLine(f"      名前: {saveData.PlayerName}")
                    Console.WriteLine(f"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}")
                    Console.WriteLine(f"      所持金: {saveData.Money}G")
                    Console.WriteLine(f"      回転数: {saveData.TotalSpins}回")
                    Console.ResetColor()
                except Exception:
                    Console.ForegroundColor = ConsoleColor.Red
                    Console.WriteLine("      [データ破損]")
                    Console.ResetColor()
            else:
                Console.ForegroundColor = ConsoleColor.DarkGray
                Console.WriteLine(f"  [{i}] スロット{i}")
                Console.WriteLine("      [データなし]")
                Console.ResetColor()
            Console.WriteLine()
        if not hasAnySave:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine("\n  セーブデータがありません")
            Console.ResetColor()
            Thread.Sleep(2000)
            break
        Console.WriteLine("  [0] 戻る\n")
        Console.Write("選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            break
        elif key.KeyChar >= "1" and key.KeyChar <= "3":
            slot = cs_int_parse(str(key.KeyChar))
            if LoadGame(slot):
                return
# ========== セーブデータ削除 ==========

def DeleteSaveMenu():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║        ⚠ データ削除 ⚠          ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine("\n【削除するスロット選択】\n")
        for i in range(1, (3) + 1):
            Console.WriteLine(f"  [{i}] スロット{i}")
            filePath = f"saves/save_{i}.json"
            if File.Exists(filePath):
                try:
                    json = File.ReadAllText(filePath)
                    saveData = coalesce_throw(json_deserialize_savedata(json), Exception("データが空です"))
                    Console.ForegroundColor = ConsoleColor.Yellow
                    Console.WriteLine(f"      名前: {saveData.PlayerName}")
                    Console.WriteLine(f"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}")
                    Console.ResetColor()
                except Exception:
                    Console.ForegroundColor = ConsoleColor.Red
                    Console.WriteLine("      [データ破損]")
                    Console.ResetColor()
            else:
                Console.ForegroundColor = ConsoleColor.DarkGray
                Console.WriteLine("      [データなし]")
                Console.ResetColor()
            Console.WriteLine()
        Console.WriteLine("  [0] 戻る\n")
        Console.Write("選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            break
        elif key.KeyChar >= "1" and key.KeyChar <= "3":
            slot = cs_int_parse(str(key.KeyChar))
            filePath = f"saves/save_{slot}.json"
            if not File.Exists(filePath):
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\nデータがありません")
                Console.ResetColor()
                Thread.Sleep(1500)
                continue
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"\n\n本当にスロット{slot}を削除しますか？ [Y/N]")
            Console.ResetColor()
            confirm = Console.ReadKey(True)
            if confirm.Key == ConsoleKey.Y:
                try:
                    File.Delete(filePath)
                    Console.ForegroundColor = ConsoleColor.Green
                    Console.WriteLine("\n\n削除しました")
                    Console.ResetColor()
                    Thread.Sleep(1500)
                except Exception:
                    Console.ForegroundColor = ConsoleColor.Red
                    Console.WriteLine("\n\n削除に失敗しました")
                    Console.ResetColor()
                    Thread.Sleep(1500)
# ========== ランキング関連 ==========

def SaveRanking():
    _hs = HighScore()
    _hs.Name = st.playerName
    _hs.Money = st.maxMoney
    _hs.Spins = st.totalSpins
    _hs.Date = DateTimeNS.Now
    st.rankings.append(_hs)
    try:
        File.AppendLine("rankings.txt", f"{st.playerName},{st.maxMoney},{st.totalSpins},{DateTimeNS.Now:yyyy-MM-dd}")
    except Exception:
        pass

def LoadRankings():
    try:
        if File.Exists("rankings.txt"):
            lines = File.ReadAllLines("rankings.txt")
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 4:
                    _hs = HighScore()
                    _hs.Name = parts[0]
                    _hs.Money = cs_int_parse(parts[1])
                    _hs.Spins = cs_int_parse(parts[2])
                    _hs.Date = DateTime.Parse(parts[3])
                    st.rankings.append(_hs)
    except Exception:
        pass
