# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — ゲーム状態 (旧グローバル変数) (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime


cs_runtime.SAVEDATA_FIELDS.extend([('OverflowCleared', 'bool'), ('RtaCleared', 'bool'), ('GameStartTime', 'DateTime'), ('PlayerName', 'string'), ('SaveDate', 'DateTime'), ('PlayTime', 'TimeSpan'), ('SaveSlot', 'int'), ('Money', 'int'), ('Debt', 'int'), ('MaxMoney', 'int'), ('MaxDebt', 'int'), ('GodModeActivateCount', 'int'), ('ConsecutiveLosses', 'int'), ('TotalSpins', 'int'), ('Total777Count', 'int'), ('ConsecutiveWins', 'int'), ('MaxConsecutiveWins', 'int'), ('TotalWinAmount', 'int'), ('TotalLoseAmount', 'int'), ('TotalLoses', 'int'), ('BigWinCount', 'int'), ('Setting', 'int'), ('DebtTurnsRemaining', 'int'), ('HasEverBorrowedMoney', 'bool'), ('GodMode', 'bool'), ('GodModeRemaining', 'int'), ('ConsecutiveHundredPlays', 'int'), ('LuckyTimeActive', 'bool'), ('LuckyTimeRemaining', 'int'), ('HasSeenConversation', 'bool'), ('HasSeenMysteriousWoman', 'bool'), ('UndergroundConsecutiveLoses', 'int'), ('UndergroundTotalSpins', 'int'), ('UndergroundCursedMode', 'bool'), ('ItemInventory', 'dict'), ('TotalLuckyCoinsPurchased', 'int'), ('HasGreedRing', 'bool'), ('GreedRingEquipped', 'bool'), ('GreedRingLoseCount', 'int'), ('VipRoomUnlocked', 'bool'), ('IsInVIPRoom', 'bool'), ('VipConsecutiveLoses', 'int'), ('Vip777Count', 'int'), ('Vip5000BetWin', 'bool'), ('VipTotalVisits', 'int'), ('VipTotalWins', 'int'), ('VipTotalSpins', 'int'), ('HasSeenVIPDealer', 'bool'), ('UndergroundUnlocked', 'bool'), ('IsInUnderground', 'bool'), ('UndergroundVisits', 'int'), ('UndergroundWins', 'int'), ('UndergroundAllInWin', 'bool'), ('HasSeenUndergroundDealer', 'bool'), ('DevilContractOffered', 'bool'), ('DevilContractType', 'int'), ('DevilContractActive', 'bool'), ('DevilContractTurns', 'int'), ('ContractStartTime', 'DateTime'), ('Contract1Complete', 'bool'), ('DevilContractSuccess', 'bool'), ('AddictionLevel', 'int'), ('IsAddicted', 'bool'), ('AddictionWarningCount', 'int'), ('HasUsedRehab', 'bool'), ('CursedItemCount', 'int'), ('HasDevilCoin', 'bool'), ('DevilCoinCurse', 'int'), ('DevilCoinWin', 'bool'), ('HasBloodAmulet', 'bool'), ('BloodAmuletLoses', 'int'), ('BloodAmulet5Wins', 'int'), ('HasDeathRing', 'bool'), ('DeathRing10Wins', 'int'), ('HasTimeClock', 'bool'), ('HasOracleBall', 'bool'), ('OracleBallPrediction', 'int'), ('DevilCoinActive', 'bool'), ('BloodAmuletEquipped', 'bool'), ('DeathRingEquipped', 'bool'), ('TimeClockEquipped', 'bool'), ('MetaEventCount', 'int'), ('UnlockedSymbols', 'list'), ('UnlockedEvents', 'list'), ('Missions', 'list_mission'), ('Rankings', 'list_highscore'), ('TrueEndingUnlocked', 'bool'), ('GodModePermanent', 'bool'), ('Contract1WinCount', 'int'), ('Contract2Deadline', 'DateTime'), ('Contract2OriginalDebt', 'int'), ('ShopVisitCount', 'int'), ('ShopCloseWithoutBuyCount', 'int'), ('BellMetFirst', 'bool'), ('MissionOpenCount', 'int'), ('DreamCasinoUnlocked', 'bool'), ('DreamLayerCleared', 'int'), ('MushroomManMet', 'bool'), ('LuckyCoinsTotal', 'int'), ('Chapter1Seen', 'bool'), ('MemoryFragmentsCleared', 'bool'), ('BlackSuitIntroduced', 'bool'), ('AbandonedCasinoUnlocked', 'bool'), ('AbandonedCasinoEntered', 'bool'), ('VanityKeyPurchased', 'bool'), ('RoomsOpened', 'rooms'), ('HasInnocentGem', 'bool'), ('HasJewelRing', 'bool'), ('HasExchangedMoney', 'bool'), ('HasUnknownCoin', 'bool'), ('UnknownCoinFlipCount', 'int'), ('BellRouteACompleted', 'bool'), ('BellRouteBCompleted', 'bool')])

def py_getflag(name):
    return globals()[name]

def py_setflag(name, v):
    globals()[name] = v

# ========== リールシンボル定義 ==========
symbols = [ [ "   ___   ", "  /   \\  ", " | o o | ", "  \\___/  ", "    |    " ], [ "   ___   ", "  /   \\  ", " |  O  | ", " |_____| ", "    |    " ], [ " _______ ", " |_____ |", "      / /", "     / / ", "    /_/  " ], [ "   ___   ", "  /   \\  ", " | \\_/ | ", "  \\___/  ", "         " ], [ "    *    ", "   ***   ", "  *****  ", "   ***   ", "    *    " ], [ "  @@@@   ", " @    @  ", " @    @  ", "  @@@@   ", "         " ], [ " ####### ", " #     # ", " ####### ", " #     # ", " ####### " ], [ "  $$$$$  ", " $     $ ", "  $$$$$  ", " $     $ ", "  $$$$$  " ] ]
# ========== 基本ゲーム変数 ==========
money = 1000
debt = 0
rand = Random()
consecutiveHundredPlays = 0
godMode = False
godModeRemaining = 0
hasSeenConversation = False
hasSeenMysteriousWoman = False
consecutiveWins = 0
consecutiveLosses = 0
bigWinCount = 0
luckyTimeActive = False
luckyTimeRemaining = 0
totalSpins = 0
debtTurnsRemaining = 0
setting = 0
missions = []
totalLoses = 0
hasEverBorrowedMoney = False
# ========== プレイヤー情報 ==========
playerName = "プレイヤー"
maxMoney = 1000
total777Count = 0
maxConsecutiveWins = 0
unlockedSymbols = [ "スライム", "ゴーレム" ]
unlockedEvents = []
itemInventory = {}
rankings = []
startTime = DateTimeNS.MinValue
totalWinAmount = 0
totalLoseAmount = 0
# ========== 強欲の指輪関連 ==========
hasGreedRing = False
greedRingEquipped = False
greedRingLoseCount = 0
totalLuckyCoinsPurchased = 0
# ========== VIPルーム関連 ==========
vipRoomUnlocked = False
isInVIPRoom = False
vipConsecutiveLoses = 0
vip777Count = 0
vip5000BetWin = False
vipTotalVisits = 0
vipTotalWins = 0
vipTotalSpins = 0
hasSeenVIPDealer = False
vipDealerName = "ミス・フォーチュン"
# ========== 地下カジノ関連 ==========
undergroundUnlocked = False
isInUnderground = False
undergroundVisits = 0
undergroundWins = 0
undergroundAllInWin = False
undergroundDealerName = "ダークロード"
hasSeenUndergroundDealer = False
# ========== 地下カジノ追加変数 ==========
undergroundConsecutiveLoses = 0
undergroundTotalSpins = 0
undergroundCursedMode = False
# ========== 悪魔契約関連 ==========
devilContractOffered = False
devilContractType = 0
devilContractActive = False
devilContractTurns = 0
contractStartTime = DateTimeNS.MinValue
contract1Complete = False
devilContractSuccess = False
contract1WinCount = 0
# 契約1勝利回数
contract2Deadline = DateTimeNS.MinValue
# 契約2期限
contract2OriginalDebt = 0
# 契約2開始時借金額
# ========== 中毒システム関連 ==========
addictionLevel = 0
isAddicted = False
addictionWarningCount = 0
hasUsedRehab = False
# ========== 呪いアイテム関連 ==========
cursedItemCount = 0
hasDevilCoin = False
devilCoinCurse = 0
devilCoinWin = False
hasBloodAmulet = False
bloodAmuletLoses = 0
bloodAmulet5Wins = 0
hasDeathRing = False
deathRing10Wins = 0
hasTimeClock = False
hasOracleBall = False
oracleBallPrediction = -1
# ========== 呪いアイテム追加変数 ==========
devilCoinActive = False
bloodAmuletEquipped = False
deathRingEquipped = False
timeClockEquipped = False
# ========== メタ演出関連 ==========
metaEventCount = 0
# ========== 特殊フラグ ==========
trueEndingUnlocked = False
godModePermanent = False
maxDebt = 0
# ベル関連
shopVisitCount = 0
shopCloseWithoutBuyCount = 0
bellMetFirst = False
# 隠しミッション関連
missionOpenCount = 0
# ========== チャプター・ストーリー関連 ==========
chapter1Seen = False
memoryFragmentsCleared = False
blackSuitIntroduced = False
# ========== 廃娯楽施設 ==========
abandonedCasinoUnlocked = False
abandonedCasinoEntered = False
vanityKeyPurchased = False
roomsOpened = [ ([False] * 5),  ([False] * 5),  ([False] * 5),  ([False] * 4),  ]
# ========== 新アイテム ==========
hasInnocentGem = False
hasJewelRing = False
hasExchangedMoney = False
hasUnknownCoin = False
unknownCoinFlipCount = 0
# ========== 新エンディングフラグ ==========
bellRouteACompleted = False
bellRouteBCompleted = False
    # 総回転数200回以上
# ========== オートセーブ ==========
autoSaveTurns = 0
AUTO_SAVE_INTERVAL = 20
# 夢カジノ関連
dreamCasinoUnlocked = False
# コイン10個で解放
dreamLayerCleared = 0
# クリア済みの層数
mushroomManMet = False
# キノコ男初回済み
luckyCoinsTotal = 0
# ========== クラス定義 ==========
# チャプター・ストーリー
# 廃娯楽施設
# 新アイテム
# 新エンディング
# ========== メイン関数 ==========
overflowCleared = False
rtaCleared = False
gameStartTime = DateTimeNS.MinValue
# ========== 中毒システム追加変数 ==========
addictionMessages = [ "もう1回だけ...", "次で取り戻せる...", "やめられない...", "あと少しで大当たり...", "画面が...歪んで見える...", "これは...夢か...？", "声が...聞こえる...", "誰かが...呼んでいる..." ]
godModeActivateCount = 0
# ========================================
# ========== コンソールグリッチ演出 ==========
# ========================================
glitchChars = [ "█","▓","▒","░","╬","╪","╫","║","═","╔","╗","╚","╝", "▲","▼","◆","◇","★","☆","※","〓","■","□","●","○", "?","!","#","%","&","@","$","/","\\","|","+","-","~" ]
