using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading;
using System.Text.Json;

namespace FEWJSCasinoSlot
{
    class Program
    {
        // ========== リールシンボル定義 ==========
        static string[][] symbols = new string[][]
        {
            new string[]{ "   ___   ", "  /   \\  ", " | o o | ", "  \\___/  ", "    |    " },
            new string[]{ "   ___   ", "  /   \\  ", " |  O  | ", " |_____| ", "    |    " },
            new string[]{ " _______ ", " |_____ |", "      / /", "     / / ", "    /_/  " },
            new string[]{ "   ___   ", "  /   \\  ", " | \\_/ | ", "  \\___/  ", "         " },
            new string[]{ "    *    ", "   ***   ", "  *****  ", "   ***   ", "    *    " },
            new string[]{ "  @@@@   ", " @    @  ", " @    @  ", "  @@@@   ", "         " },
            new string[]{ " ####### ", " #     # ", " ####### ", " #     # ", " ####### " },
            new string[]{ "  $$$$$  ", " $     $ ", "  $$$$$  ", " $     $ ", "  $$$$$  " }
        };

        // ========== 基本ゲーム変数 ==========
        static int money = 1000;
        static int debt = 0;
        static Random rand = new Random();
        static int consecutiveHundredPlays = 0;
        static bool godMode = false;
        static int godModeRemaining = 0;
        static bool hasSeenConversation = false;
        static bool hasSeenMysteriousWoman = false;
        static int consecutiveWins = 0;
        static int consecutiveLosses = 0;
        static int bigWinCount = 0;
        static bool luckyTimeActive = false;
        static int luckyTimeRemaining = 0;
        static int totalSpins = 0;
        static int debtTurnsRemaining = 0;
        static int setting = 0;
        static List<Mission> missions = new List<Mission>();
        static int totalLoses = 0;
        static bool hasEverBorrowedMoney = false;


        // ========== プレイヤー情報 ==========
        static string playerName = "プレイヤー";
        static int maxMoney = 1000;
        static int total777Count = 0;
        static int maxConsecutiveWins = 0;
        static List<string> unlockedSymbols = new List<string> { "スライム", "ゴーレム" };
        static List<string> unlockedEvents = new List<string>();
        static Dictionary<string, int> itemInventory = new Dictionary<string, int>();
        static List<HighScore> rankings = new List<HighScore>();
        static DateTime startTime;
        static int totalWinAmount = 0;
        static int totalLoseAmount = 0;

        // ========== 強欲の指輪関連 ==========
        static bool hasGreedRing = false;
        static bool greedRingEquipped = false;
        static int greedRingLoseCount = 0;
        static int totalLuckyCoinsPurchased = 0;

        // ========== VIPルーム関連 ==========
        static bool vipRoomUnlocked = false;
        static bool isInVIPRoom = false;
        static int vipConsecutiveLoses = 0;
        static int vip777Count = 0;
        static bool vip5000BetWin = false;
        static int vipTotalVisits = 0;
        static int vipTotalWins = 0;
        static int vipTotalSpins = 0;
        static bool hasSeenVIPDealer = false;
        static string vipDealerName = "ミス・フォーチュン";

        // ========== 地下カジノ関連 ==========
        static bool undergroundUnlocked = false;
        static bool isInUnderground = false;
        static int undergroundVisits = 0;
        static int undergroundWins = 0;
        static bool undergroundAllInWin = false;
        static string undergroundDealerName = "ダークロード";
        static bool hasSeenUndergroundDealer = false;

        // ========== 地下カジノ追加変数 ==========
        static int undergroundConsecutiveLoses = 0;
        static int undergroundTotalSpins = 0;
        static bool undergroundCursedMode = false;

        // ========== 悪魔契約関連 ==========
        static bool devilContractOffered = false;
        static int devilContractType = 0;
        static bool devilContractActive = false;
        static int devilContractTurns = 0;
        static DateTime contractStartTime;
        static bool contract1Complete = false;
        static bool devilContractSuccess = false;
        static int contract1WinCount = 0;           // 契約1勝利回数
        static DateTime contract2Deadline;          // 契約2期限
        static int contract2OriginalDebt = 0;       // 契約2開始時借金額

        // ========== 中毒システム関連 ==========
        static int addictionLevel = 0;
        static bool isAddicted = false;
        static int addictionWarningCount = 0;
        static bool hasUsedRehab = false;

        // ========== 呪いアイテム関連 ==========
        static int cursedItemCount = 0;
        static bool hasDevilCoin = false;
        static int devilCoinCurse = 0;
        static bool devilCoinWin = false;
        static bool hasBloodAmulet = false;
        static int bloodAmuletLoses = 0;
        static int bloodAmulet5Wins = 0;
        static bool hasDeathRing = false;
        static int deathRing10Wins = 0;
        static bool hasTimeClock = false;
        static bool hasOracleBall = false;
        static int oracleBallPrediction = -1;

        // ========== 呪いアイテム追加変数 ==========
        static bool devilCoinActive = false;
        static bool bloodAmuletEquipped = false;
        static bool deathRingEquipped = false;
        static bool timeClockEquipped = false;

        // ========== メタ演出関連 ==========
        static int metaEventCount = 0;

        // ========== 特殊フラグ ==========
        static bool trueEndingUnlocked = false;
        static bool godModePermanent = false;
        static int maxDebt = 0;

        // ベル関連
        static int shopVisitCount = 0;
        static int shopCloseWithoutBuyCount = 0;
        static bool bellMetFirst = false;

        // 隠しミッション関連
        static int missionOpenCount = 0;

        // ========== チャプター・ストーリー関連 ==========
        static bool chapter1Seen = false;
        static bool memoryFragmentsCleared = false;
        static bool blackSuitIntroduced = false;

        // ========== 廃娯楽施設 ==========
        static bool abandonedCasinoUnlocked = false;
        static bool abandonedCasinoEntered = false;
        static bool vanityKeyPurchased = false;
        static bool[][] roomsOpened = new bool[][]
        {
            new bool[5],  // 1階 部屋0〜4
            new bool[5],  // 2階
            new bool[5],  // 3階
            new bool[4],  // 地下
        };

        // ========== 新アイテム ==========
        static bool hasInnocentGem = false;
        static bool hasJewelRing = false;
        static bool hasExchangedMoney = false;
        static bool hasUnknownCoin = false;
        static int unknownCoinFlipCount = 0;

        // ========== 新エンディングフラグ ==========
        static bool bellRouteACompleted = false;
        static bool bellRouteBCompleted = false;

        // ========== TRUEエンディング条件チェック ==========
        static bool CheckTrueEndCondition()
        {
            return dreamLayerCleared >= 5      // 夢カジノ全層クリア
                && hasEverBorrowedMoney        // 借金経験あり
                && debt == 0                   // 現在借金なし
                && total777Count >= 3          // 777を3回以上
                && hasUsedRehab                // リハビリ経験あり
                && addictionLevel <= 50        // 現在中毒度50以下
                && totalSpins >= 200;          // 総回転数200回以上
        }

        // ========== オートセーブ ==========
        static int autoSaveTurns = 0;
        const int AUTO_SAVE_INTERVAL = 20;

        // 夢カジノ関連
        static bool dreamCasinoUnlocked = false;    // コイン10個で解放
        static int dreamLayerCleared = 0;           // クリア済みの層数
        static bool mushroomManMet = false;         // キノコ男初回済み
        static int luckyCoinsTotal = 0;             // 幸運のコイン累計購入数

        // ========== 設定示唆演出 ==========
        static void ShowSettingSuggestion()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         今日の台の調子は...");
            Console.WriteLine("    ================================");
            Thread.Sleep(1500);

            string[] suggestions = {
        "起動音が普通だ...",
        "起動音が少し高い...",
        "起動音がやや高い！",
        "起動音が高い！！",
        "起動音がかなり高い！！！",
        "起動音が異常に高い！！！！"
    };

            string[] hints = {
        "今日は渋そうだ...",
        "まあまあかな",
        "少し期待できるかも",
        "今日はいけるかもしれない！",
        "かなり良さそうだ！！",
        "これは...高設定の予感！？"
    };

            Console.ForegroundColor = ConsoleColor.Yellow;
            if (setting < 1 || setting > 6) return; // 安全ガード
            Console.WriteLine($"\n    {suggestions[setting - 1]}");
            Thread.Sleep(1500);

            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine($"\n    {hints[setting - 1]}");
            Thread.Sleep(1500);

            if (setting == 6)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n\n    （これは...高設定の予感！？）");
                Console.ResetColor();
                Thread.Sleep(2000);

                if (!unlockedEvents.Contains("設定6解放"))
                    unlockedEvents.Add("設定6解放");
            }

            Console.ResetColor();
            Thread.Sleep(1000);
        }

        // ========== クラス定義 ==========
        [Serializable]
        class SaveData
        {
            public bool OverflowCleared { get; set; }
            public bool RtaCleared { get; set; }
            public DateTime GameStartTime { get; set; }
            public string PlayerName { get; set; } = string.Empty;
            public DateTime SaveDate { get; set; }
            public TimeSpan PlayTime { get; set; }
            public int SaveSlot { get; set; }

            public int Money { get; set; }
            public int Debt { get; set; }
            public int MaxMoney { get; set; }
            public int MaxDebt { get; set; }
            public int GodModeActivateCount { get; set; }
            public int ConsecutiveLosses { get; set; }
            public int TotalSpins { get; set; }
            public int Total777Count { get; set; }
            public int ConsecutiveWins { get; set; }
            public int MaxConsecutiveWins { get; set; }
            public int TotalWinAmount { get; set; }
            public int TotalLoseAmount { get; set; }
            public int TotalLoses { get; set; }
            public int BigWinCount { get; set; }

            public int Setting { get; set; }
            public int DebtTurnsRemaining { get; set; }
            public bool HasEverBorrowedMoney { get; set; }

            public bool GodMode { get; set; }
            public int GodModeRemaining { get; set; }
            public int ConsecutiveHundredPlays { get; set; }

            public bool LuckyTimeActive { get; set; }
            public int LuckyTimeRemaining { get; set; }

            public bool HasSeenConversation { get; set; }
            public bool HasSeenMysteriousWoman { get; set; }

            public int UndergroundConsecutiveLoses { get; set; }
            public int UndergroundTotalSpins { get; set; }
            public bool UndergroundCursedMode { get; set; }
            public Dictionary<string, int> ItemInventory { get; set; } = new Dictionary<string, int>();
            public int TotalLuckyCoinsPurchased { get; set; }

            public bool HasGreedRing { get; set; }
            public bool GreedRingEquipped { get; set; }
            public int GreedRingLoseCount { get; set; }

            public bool VipRoomUnlocked { get; set; }
            public bool IsInVIPRoom { get; set; }
            public int VipConsecutiveLoses { get; set; }
            public int Vip777Count { get; set; }
            public bool Vip5000BetWin { get; set; }
            public int VipTotalVisits { get; set; }
            public int VipTotalWins { get; set; }
            public int VipTotalSpins { get; set; }
            public bool HasSeenVIPDealer { get; set; }

            public bool UndergroundUnlocked { get; set; }
            public bool IsInUnderground { get; set; }
            public int UndergroundVisits { get; set; }
            public int UndergroundWins { get; set; }
            public bool UndergroundAllInWin { get; set; }
            public bool HasSeenUndergroundDealer { get; set; }

            public bool DevilContractOffered { get; set; }
            public int DevilContractType { get; set; }
            public bool DevilContractActive { get; set; }
            public int DevilContractTurns { get; set; }
            public DateTime ContractStartTime { get; set; }
            public bool Contract1Complete { get; set; }
            public bool DevilContractSuccess { get; set; }

            public int AddictionLevel { get; set; }
            public bool IsAddicted { get; set; }
            public int AddictionWarningCount { get; set; }
            public bool HasUsedRehab { get; set; }

            public int CursedItemCount { get; set; }
            public bool HasDevilCoin { get; set; }
            public int DevilCoinCurse { get; set; }
            public bool DevilCoinWin { get; set; }
            public bool HasBloodAmulet { get; set; }
            public int BloodAmuletLoses { get; set; }
            public int BloodAmulet5Wins { get; set; }
            public bool HasDeathRing { get; set; }
            public int DeathRing10Wins { get; set; }
            public bool HasTimeClock { get; set; }
            public bool HasOracleBall { get; set; }
            public int OracleBallPrediction { get; set; }
            public bool DevilCoinActive { get; set; }
            public bool BloodAmuletEquipped { get; set; }
            public bool DeathRingEquipped { get; set; }
            public bool TimeClockEquipped { get; set; }

            public int MetaEventCount { get; set; }

            public List<string> UnlockedSymbols { get; set; } = new List<string>();
            public List<string> UnlockedEvents { get; set; } = new List<string>();

            public List<MissionSaveData> Missions { get; set; } = new List<MissionSaveData>();

            public List<HighScore> Rankings { get; set; } = new List<HighScore>();

            public bool TrueEndingUnlocked { get; set; }
            public bool GodModePermanent { get; set; }
            public int Contract1WinCount { get; set; }
            public DateTime Contract2Deadline { get; set; }
            public int Contract2OriginalDebt { get; set; }
            public int ShopVisitCount { get; set; }
            public int ShopCloseWithoutBuyCount { get; set; }
            public bool BellMetFirst { get; set; }
            public int MissionOpenCount { get; set; }
            public bool DreamCasinoUnlocked { get; set; }
            public int DreamLayerCleared { get; set; }
            public bool MushroomManMet { get; set; }
            public int LuckyCoinsTotal { get; set; }

            // チャプター・ストーリー
            public bool Chapter1Seen { get; set; }
            public bool MemoryFragmentsCleared { get; set; }
            public bool BlackSuitIntroduced { get; set; }

            // 廃娯楽施設
            public bool AbandonedCasinoUnlocked { get; set; }
            public bool AbandonedCasinoEntered { get; set; }
            public bool VanityKeyPurchased { get; set; }
            public bool[][] RoomsOpened { get; set; } = new bool[4][];

            // 新アイテム
            public bool HasInnocentGem { get; set; }
            public bool HasJewelRing { get; set; }
            public bool HasExchangedMoney { get; set; }
            public bool HasUnknownCoin { get; set; }
            public int UnknownCoinFlipCount { get; set; }

            // 新エンディング
            public bool BellRouteACompleted { get; set; }
            public bool BellRouteBCompleted { get; set; }
        }

        [Serializable]
        class MissionSaveData
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public int Reward { get; set; }
            public bool Completed { get; set; }
        }

        class HighScore
        {
            public string Name { get; set; } = string.Empty;
            public int Money { get; set; }
            public int Spins { get; set; }
            public DateTime Date { get; set; }
        }

        class Mission
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public Func<bool> CheckComplete { get; set; }
            public int Reward { get; set; }
            public bool Completed { get; set; }

            public Mission(string name, string desc, Func<bool> check, int reward)
            {
                Name = name;
                Description = desc;
                CheckComplete = check;
                Reward = reward;
                Completed = false;
            }
        }

        // ========== メイン関数 ==========
        static bool overflowCleared = false;
        static bool rtaCleared = false;
        static DateTime gameStartTime;

        // ========== FormatTimeSpan ヘルパー関数（メソッド末尾に追加） ==========
        static string FormatTimeSpan(TimeSpan ts)
        {
            if (ts.TotalMinutes < 1)
                return $"{ts.Seconds}秒";
            else if (ts.TotalHours < 1)
                return $"{ts.Minutes}分{ts.Seconds}秒";
            else
                return $"{ts.Hours}時間{ts.Minutes}分{ts.Seconds}秒";
        }

        static string GetAddictionBar(int level)
        {
            int filled = level / 5;

            ConsoleColor color = level < 40 ? ConsoleColor.Green
                               : level < 70 ? ConsoleColor.Yellow
                                            : ConsoleColor.Red;

            Console.ForegroundColor = color;
            string bar = $"[{"█".PadLeft(filled, '█').PadRight(20, '░')}] {level}%";
            Console.ResetColor();
            return bar;
        }

        static void Main(string[] args)
        {
            try
            {
                Console.OutputEncoding = System.Text.Encoding.UTF8;
            }
            catch
            {
                // UTF-8が使えない環境でもエラーにならないように
            }

            Console.CursorVisible = false;

            itemInventory["お守り"] = 0;
            itemInventory["幸運のコイン"] = 0;
            itemInventory["返済猶予券"] = 0;

            LoadRankings();

            while (true)
            {
                // ===== ゲーム変数リセット（タイトルに戻るたびに初期化） =====
                money = 1000; debt = 0; debtTurnsRemaining = 0;
                addictionLevel = 0; isAddicted = false; addictionWarningCount = 0;
                setting = 0;
                godMode = false; godModePermanent = false; godModeRemaining = 0;
                luckyTimeActive = false; luckyTimeRemaining = 0;
                consecutiveWins = 0; consecutiveLosses = 0;
                consecutiveHundredPlays = 0;
                totalSpins = 0; totalWinAmount = 0; totalLoseAmount = 0;
                totalLoses = 0; bigWinCount = 0;
                total777Count = 0; maxConsecutiveWins = 0; maxMoney = 1000; maxDebt = 0;
                hasSeenConversation = false; hasSeenMysteriousWoman = false;
                vipRoomUnlocked = false; isInVIPRoom = false;
                vipConsecutiveLoses = 0; vip777Count = 0; vip5000BetWin = false;
                vipTotalVisits = 0; vipTotalWins = 0; vipTotalSpins = 0; hasSeenVIPDealer = false;
                undergroundUnlocked = false; isInUnderground = false;
                undergroundVisits = 0; undergroundWins = 0; undergroundAllInWin = false;
                undergroundConsecutiveLoses = 0; undergroundTotalSpins = 0;
                undergroundCursedMode = false; hasSeenUndergroundDealer = false;
                dreamCasinoUnlocked = false; dreamLayerCleared = 0; mushroomManMet = false;
                luckyCoinsTotal = 0;
                devilContractOffered = false; devilContractActive = false;
                devilContractType = 0; devilContractTurns = 0;
                devilContractSuccess = false; contract1Complete = false;
                contract1WinCount = 0;
                hasGreedRing = false; greedRingEquipped = false; greedRingLoseCount = 0;
                totalLuckyCoinsPurchased = 0;
                hasDevilCoin = false; devilCoinCurse = 0; devilCoinWin = false; devilCoinActive = false;
                hasBloodAmulet = false; bloodAmuletLoses = 0; bloodAmulet5Wins = 0; bloodAmuletEquipped = false;
                hasDeathRing = false; deathRing10Wins = 0; deathRingEquipped = false;
                hasTimeClock = false; timeClockEquipped = false;
                hasOracleBall = false; oracleBallPrediction = -1;
                cursedItemCount = 0;
                metaEventCount = 0;
                trueEndingUnlocked = false;
                hasEverBorrowedMoney = false; hasUsedRehab = false;
                shopVisitCount = 0; shopCloseWithoutBuyCount = 0; bellMetFirst = false;
                missionOpenCount = 0; autoSaveTurns = 0;
                overflowCleared = false; rtaCleared = false;
                playerName = "プレイヤー";
                itemInventory["お守り"] = 0;
                itemInventory["幸運のコイン"] = 0;
                itemInventory["返済猶予券"] = 0;
                unlockedSymbols.Clear();
                unlockedSymbols.Add("スライム");
                unlockedSymbols.Add("ゴーレム");
                unlockedEvents.Clear();
                missions.Clear();
                rankings.Clear();
                LoadRankings();

                ShowTitleScreen();

                // ロードされていない場合のみ名前入力
                if (playerName == "プレイヤー")
                {
                    InputPlayerName();
                }

                startTime = DateTime.Now;
                gameStartTime = DateTime.Now;

                // 新規ゲームの場合のみ
                if (setting == 0)
                {
                    ShowLoadingScreen();
                    setting = rand.Next(1, 7);
                    ShowSettingSuggestion();
                    InitializeMissions();
                }

                GameLoop();
                ShowEnding();
                // ShowEnding が終わったらループ先頭に戻り、タイトルへ
            }
        }

        static string GetBellGreeting()
        {
            int hour = DateTime.Now.Hour;

            // 初回
            if (!bellMetFirst)
            {
                bellMetFirst = true;
                return "あら、いらっしゃい♪\n    待ってたわよ？ここには素敵なものが揃ってるから、ゆっくり見ていってね";
            }

            // 中毒度MAX — 素が出る
            if (addictionLevel >= 90)
            {
                string[] maxAddicted = {
                    "…また来たの。\n    …もう、止めてって言っても聞かないわよね。わかってる♪",
                    "顔…ひどいわよ？\n    …でも、来てくれるのは嬉しい。複雑だわ♪",
                    "あなたのこと…心配してるわけじゃないけど\n    …心配してる。うん、してる♪",
                    "…お金なくなっても、来ていいのよ？\n    …ここにいると、安心でしょ？",
                    "…あなたが来ないと、なんか…落ち着かないの\n    …変よね♪ 私",
                    "また来たのね♪\n    …来るって、わかってた。ずっと待ってたから",
                };
                return maxAddicted[rand.Next(maxAddicted.Length)];
            }

            // 中毒度高め
            if (addictionLevel >= 50)
            {
                string[] addicted = {
                    "…また来たの\n    …いつ寝てるの？♪",
                    "顔色…大丈夫？\n    まあ、来てくれるのは嬉しいけど♪",
                    "少し休んだら？\n    …なんて、言っても無駄よね♪",
                    "…リハビリ、考えてみる？\n    …本気で言ってるの。ふざけてないわよ",
                };
                return addicted[rand.Next(addicted.Length)];
            }

            // 悪魔契約中
            if (devilContractActive)
            {
                string[] contract = {
                    "…なんか、空気が重い気がするわ\n    気のせいかしら♪",
                    "…あなた、何かした？\n    聞かなくてもわかるけど♪",
                    "最近ツいてるじゃない♪\n    …でも、なんか怖いわね",
                };
                return contract[rand.Next(contract.Length)];
            }

            // 借金が高額
            if (debt >= 10000)
            {
                string[] bigDebt = {
                    "…借金、増えてるじゃない\n    …大丈夫なの？本当に？",
                    "顔色悪いわよ。ここに来てる場合じゃないんじゃない？\n    …まあ、来てくれたけど♪",
                    "…ねえ、少しだけ話せる？\n    …なんでもないわ、いらっしゃい♪",
                };
                return bigDebt[rand.Next(bigDebt.Length)];
            }

            // 地下カジノ解放後（2回に1回）
            if (undergroundUnlocked && rand.Next(2) == 0)
            {
                string[] underground = {
                    "…地下にも行ってるの？\n    気をつけてね♪ …本当に",
                    "あっちには近づかない方がいいと思うけど\n    …まあ、止めないわ♪",
                    "帰ってきたのね♪\n    …無事でよかった。本当に",
                    "…あそこの人たち、目が怖いわよね\n    あなたはまだ大丈夫そうだけど♪",
                };
                return underground[rand.Next(underground.Length)];
            }

            // VIPルーム解放後（3回に1回）
            if (vipRoomUnlocked && rand.Next(3) == 0)
            {
                string[] vip = {
                    "VIPルームにも行くのね♪\n    …どっちが好き？",
                    "最近羽振りがいいじゃない♪\n    …うらやましいわ",
                    "VIPの常連さんになったの？\n    …私のことも忘れないでね♪",
                    "向こうのディーラー、綺麗よね♪\n    …なんでもない。いらっしゃい",
                };
                return vip[rand.Next(vip.Length)];
            }

            // 777を複数回
            if (total777Count >= 5)
            {
                string[] veryLucky = {
                    "777、また揃えたの？\n    …もうあなた、普通じゃないわよ♪",
                    "神様に愛されてるのかしら\n    …それとも悪魔に？♪",
                };
                if (rand.Next(2) == 0) return veryLucky[rand.Next(veryLucky.Length)];
            }
            if (total777Count >= 3)
            {
                string[] lucky = {
                    "777、また揃えたの？\n    …化け物ね♪",
                    "運がいいのね♪\n    …それとも、何か持ってる？",
                    "三度目の777…\n    …本物のギャンブラーね♪",
                };
                if (rand.Next(2) == 0) return lucky[rand.Next(lucky.Length)];
            }

            // 連敗中
            if (consecutiveLosses >= 10)
            {
                string[] bigLosing = {
                    "…10連敗…？\n    …少し、休もっか♪",
                    "顔が死んでるわよ？\n    …まあ、ここに来てくれる分にはいいけど♪",
                    "ねえ、少し笑って？\n    …ダメ？ そうよね♪",
                };
                return bigLosing[rand.Next(bigLosing.Length)];
            }
            if (consecutiveWins == 0 && totalLoses > 0 && totalLoses % 5 == 0)
            {
                string[] losing = {
                    "…今日は運が悪いわね\n    明日にしたら？♪",
                    "負けが続いてるじゃない\n    …大丈夫？♪",
                    "ここに来ると少し落ち着く？\n    …それならいいけど♪",
                };
                return losing[rand.Next(losing.Length)];
            }

            // 深夜 × 中毒度高い → 素が出る
            if ((hour >= 22 || hour < 5) && addictionLevel >= 60)
            {
                string[] lateAddicted = {
                    "こんな時間に…\n    …でも来てくれた♪ 嬉しい。本当に",
                    "眠れないの？\n    …ここにいれば、眠くなるまで付き合うわよ♪",
                    "…ねえ、家族とか、友達は？\n    …余計なこと聞いたわね。ごめん♪",
                    "こんな時間まで…\n    …あなた以外、誰もいないのよここ。だから嬉しい♪",
                };
                return lateAddicted[rand.Next(lateAddicted.Length)];
            }

            // 深夜（通常）
            if (hour >= 22 || hour < 5)
            {
                string[] lateNight = {
                    "こんな時間に来るなんて…\n    …大丈夫？ まあ、大丈夫じゃないわよね♪",
                    "眠れないの？\n    …私もよ。だから待ってたけど♪",
                    "こんな時間まで…\n    …まあ、会えたから嬉しいけど♪",
                };
                return lateNight[rand.Next(lateNight.Length)];
            }

            // リッチ
            if (money >= 20000)
            {
                string[] veryRich = {
                    "…すごいわね。ほんとに♪\n    そのお金、夢みたい",
                    "大金持ちのお客様♪\n    …でも、ここに来てくれてるのね",
                };
                if (rand.Next(2) == 0) return veryRich[rand.Next(veryRich.Length)];
            }
            if (money >= 5000)
            {
                string[] rich = {
                    "随分稼いでるじゃない。すごいわね♪\n    …そのお金、大事にしてね？",
                    "また来たのね♪ お金持ちのお客様は大歓迎よ",
                    "調子いいじゃない♪\n    …羨ましいわ、少し",
                };
                return rich[rand.Next(rich.Length)];
            }

            // 借金あり
            if (debt > 0)
            {
                string[] inDebt = {
                    "…顔色悪いわよ？\n    まあ、私には関係ないけど♪",
                    "借金があっても来てくれるのね。…うれしい♪",
                    "…返せそう？\n    …余計なお世話よね。ごめん♪",
                    "大変そうね…\n    …でも、ここに来るのはやめないのね♪",
                };
                return inDebt[rand.Next(inDebt.Length)];
            }

            // よく来るお客様
            if (shopVisitCount >= 20)
            {
                string[] regular = {
                    $"…{shopVisitCount}回目よ、もう♪\n    顔覚えちゃったわ",
                    "また来たわね♪\n    …もう常連さんね。嬉しいわ、本当に",
                    "いつもありがとう♪\n    …なんか、いてくれると安心するわ",
                };
                if (rand.Next(3) == 0) return regular[rand.Next(regular.Length)];
            }

            // 何も買わずに来た回数
            if (shopCloseWithoutBuyCount >= 3)
                return $"また来たのね。{shopCloseWithoutBuyCount}回目よ♪\n    …今日こそ買うの？";

            // 通常
            string[] normal = {
                "また来たのね♪ やっぱり来ると思ってた",
                "いらっしゃい♪ 今日は何にする？",
                "来てくれると思ってたわ♪",
                "あら♪ また会えたわね",
                "待ってたわよ♪\n    …嘘じゃないの",
                "いらっしゃい♪\n    …来るの、わかってたわよ？",
            };
            return normal[rand.Next(normal.Length)];
        }

        static string GetBellPurchaseComment(string itemName)
        {
            if (itemName == "悪魔のコイン" || itemName == "血塗られたお守り" ||
                itemName == "死神の指輪" || itemName == "時を刻む懐中時計" || itemName == "禁断の水晶玉")
            {
                string[] cursed = {
            "…本当にいいの？ まあ、あなたが選んだことだから♪",
            "似合いそう。すごく♪",
            "…止めませんよ。止める権利もないので♪",
        };
                return cursed[rand.Next(cursed.Length)];
            }
            // 悪魔契約中の購入コメント
            if (devilContractActive)
            {
                string[] contractBuy = {
        "…本当にそれが必要？\n    まあ、いいけど♪",
        "急いでるのに、買い物してるの？\n    …余裕あるのね♪",
        "…なんか、見えない何かがいる気がする\n    気にしないで♪",
    };
                return contractBuy[rand.Next(contractBuy.Length)];
            }

            string[] normal = {
        "さすが、目の付け所がいいわね♪",
        "これを選ぶなんて…センスあるじゃない♪",
        "ありがとう♪ また来てね",
    };
            return normal[rand.Next(normal.Length)];
        }

        static string GetBellFarewell()
        {
            // 悪魔契約中
            if (devilContractActive)
            {
                if (devilContractType == 1)
                {
                    string[] contract1 = {
                        "…なんか、雰囲気変わったわね♪\n    気のせいかしら…",
                        "…その指、何か巻いてる？\n    …別に、気にしてないけど♪",
                        "最近ツいてるじゃない♪\n    …でも、なんか怖いわね",
                        "10回…ちゃんと数えてる？\n    …まあ、いいけど♪",
                    };
                    return contract1[rand.Next(contract1.Length)];
                }
                if (devilContractType == 2)
                {
                    string[] contract2 = {
                        "…急いでるの？\n    顔色悪いわよ♪",
                        "時間、大丈夫？\n    …なんとなく聞いてみただけ♪",
                        "…何かに追われてる感じがするわ\n    …私だけ？♪",
                        "…ねえ、間に合うの？\n    …余計なこと言ったわね。行って♪",
                    };
                    return contract2[rand.Next(contract2.Length)];
                }
                if (devilContractType == 3)
                {
                    string[] contract3 = {
                        "…あなた、前に会ったことある？\n    なんか、初めて会った気がしないのよね♪",
                        "なんか…覚えてないことがあるって怖いわよね\n    …ふふ♪",
                        "…私のこと、ちゃんと覚えてる？\n    …覚えててね。お願い♪",
                    };
                    return contract3[rand.Next(contract3.Length)];
                }
            }

            // 中毒度高い
            if (addictionLevel >= 70)
            {
                string[] addicted = {
                    "…また来てね♪\n    …来るって、わかってるけど",
                    "ゆっくり休んでね♪\n    …嘘。来るって信じてるわ",
                    "…次来た時、顔色よくなってたら嬉しいわ♪",
                };
                return addicted[rand.Next(addicted.Length)];
            }

            // 借金高い
            if (debt >= 10000)
            {
                string[] bigDebt = {
                    "…気をつけてね♪\n    …本当に",
                    "また来てね♪\n    …でも、無理しないで",
                    "…待ってるから♪\n    借金、なんとかなるといいわね",
                };
                return bigDebt[rand.Next(bigDebt.Length)];
            }

            // 777達成後
            if (total777Count >= 3 && rand.Next(3) == 0)
            {
                string[] after777 = {
                    "またやっちゃうの？♪\n    …777、もう一回見たいわ",
                    "また来てね♪\n    …次も揃えてみせて？",
                };
                return after777[rand.Next(after777.Length)];
            }

            // 常連（何も買わずに帰る回数）
            shopCloseWithoutBuyCount++;

            if (shopCloseWithoutBuyCount == 5)
                return "ねえ、もしかして私に会いに来てる？\n    …正解♪";

            if (shopCloseWithoutBuyCount == 10)
                return "10回目ね♪\n    …数えてたの。内緒よ？";

            if (shopCloseWithoutBuyCount == 20)
                return "20回目♪\n    …もう、ここが居場所になってるんじゃないの？";

            if (shopCloseWithoutBuyCount == 30)
                return "30回よ♪\n    …あなた、私なしじゃ無理でしょ。わかってる";

            if (shopCloseWithoutBuyCount >= 3)
            {
                string[] repeat = {
                    "…また来てね♪ 待ってるから",
                    "いつでも来てね♪\n    …本当に、待ってるから",
                    "またいつでも♪\n    …来るの、わかってるけど言いたかった",
                    "…行かないで\n    …なんでもない♪ またね",
                    "また来てね♪\n    …来なかったら、探しに行くわよ？",
                    "…帰るの？\n    …そう。また来てね♪ 絶対に",
                };
                return repeat[rand.Next(repeat.Length)];
            }

            string[] normal = {
                "またいつでも来てね♪",
                "待ってるわよ♪",
                "いつでもどうぞ♪",
                "またね♪\n    …来てくれると思ってる",
                "気をつけてね♪",
            };
            return normal[rand.Next(normal.Length)];
        }
        // ========== タイトル画面 ==========
        static void ShowTitleScreen()
        {
            // ========== 電源投入点滅 ==========
            for (int i = 0; i < 4; i++)
            {
                Console.Clear();
                Console.BackgroundColor = ConsoleColor.White;
                Console.ForegroundColor = ConsoleColor.Black;
                Console.WriteLine("\n\n\n\n\n\n\n\n          ■");
                Console.ResetColor();
                Thread.Sleep(80);
                Console.Clear();
                Thread.Sleep(60);
            }

            // ========== 全色フラッシュ ==========
            ConsoleColor[] flashColors = {
                ConsoleColor.Red, ConsoleColor.Yellow, ConsoleColor.White,
                ConsoleColor.Cyan, ConsoleColor.Magenta, ConsoleColor.Green
            };
            foreach (var c in flashColors)
            {
                Console.Clear();
                Console.BackgroundColor = c;
                Console.Write(new string(' ', 200));
                Console.ResetColor();
                Thread.Sleep(80);
                Console.Clear();
                Thread.Sleep(40);
            }

            // ========== ロゴ1行ずつ降臨 ==========
            string[] logoLines = {
                "    ╔════════════════════════════════════════╗",
                "    ║                                        ║",
                "    ║   Future Electric Wonder Jackpot Slot  ║",
                "    ║              - 運命の賭け -            ║",
                "    ║                                        ║",
                "    ║             FINAL  EDITION             ║",
                "    ║                                        ║",
                "    ╚════════════════════════════════════════╝"
            };

            Console.Clear();
            Console.WriteLine("\n\n\n");
            for (int i = 0; i < logoLines.Length; i++)
            {
                Console.ForegroundColor = i == 2 ? ConsoleColor.Yellow
                                        : i == 3 ? ConsoleColor.Cyan
                                        : i == 5 ? ConsoleColor.White
                                        : ConsoleColor.DarkYellow;
                Console.WriteLine(logoLines[i]);
                Thread.Sleep(120);
            }
            Console.ResetColor();
            Thread.Sleep(400);

            // ========== ★ 7 7 7 ★ JACKPOT ★ 点滅 ==========
            string[] jackpotLogo = {
                "    ╔════════════════════════════════════════╗",
                "    ║                                        ║",
                "    ║   Future Electric Wonder Jackpot Slot  ║",
                "    ║              - 運命の賭け -            ║",
                "    ║                                        ║",
                "    ║             FINAL  EDITION             ║",
                "    ║                                        ║",
                "    ╚════════════════════════════════════════╝"
            };

            for (int i = 0; i < 6; i++)
            {
                Console.Clear();
                Console.WriteLine("\n\n\n");

                // ロゴ再描画
                for (int li = 0; li < jackpotLogo.Length; li++)
                {
                    Console.ForegroundColor = li == 2 ? ConsoleColor.Yellow
                                            : li == 3 ? ConsoleColor.Cyan
                                            : li == 5 ? ConsoleColor.White
                                            : ConsoleColor.DarkYellow;
                    Console.WriteLine(jackpotLogo[li]);
                }
                Console.ResetColor();

                Console.WriteLine();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Red : ConsoleColor.Yellow;
                Console.WriteLine("          ★  7  7  7  ★  JACKPOT  ★");
                Console.ResetColor();
                Thread.Sleep(i < 5 ? 280 : 500);
            }

            // ========== メニュー項目タイプライター表示 ==========
            Console.WriteLine();
            string[] menuItems = {
                "\n          [Enter] 新規ゲーム",
                "          [L]     ロード",
                "          [D]     セーブデータ削除",
                "          [Q]     ゲーム終了"
            };
            Console.ForegroundColor = ConsoleColor.Cyan;
            foreach (var item in menuItems)
            {
                foreach (char ch in item)
                {
                    Console.Write(ch);
                    Thread.Sleep(25);
                }
                Console.WriteLine();
            }
            Console.ResetColor();

            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n\n          ©2025~2026 FEWJS Casino Corporation");
            Console.ResetColor();

            var key = Console.ReadKey(true);

            if (key.Key == ConsoleKey.L)
            {
                LoadMenu();
            }
            else if (key.Key == ConsoleKey.D)
            {
                DeleteSaveMenu();
                ShowTitleScreen();
            }
            else if (key.Key == ConsoleKey.Q)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n\n          またいつか...");
                Console.ResetColor();
                Thread.Sleep(1500);
                Environment.Exit(0);
            }
            else if (key.KeyChar == '`' || key.KeyChar == '~')
            {
                // ===== DEV MODE 入口 =====
                DevModeEntry();
                ShowTitleScreen();
            }
        }

        // ========== プレイヤー名入力 ==========
        static void InputPlayerName()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    あなたの名前を教えてください");
            Console.WriteLine("    （10文字以内、Enterで決定）");
            Console.ResetColor();
            Console.Write("\n    名前 > ");
            Console.CursorVisible = true;

            string input = Console.ReadLine() ?? string.Empty;
            playerName = input;

            Console.CursorVisible = false;

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"\n\n    ようこそ、{playerName}さん。");
            Console.WriteLine("    運命の扉が今、開かれる...");
            Console.ResetColor();
            Thread.Sleep(2500);
        }
        // ========== オーバーフロー隠しエンディング（超豪華版） ==========
        static void OverflowHiddenEnding()
        {
            // RTA判定
            TimeSpan elapsed = DateTime.Now - gameStartTime;
            bool isRTA = elapsed.TotalSeconds <= 300;

            overflowCleared = true;
            if (isRTA) rtaCleared = true;

            // ============================================
            // フェーズ0: 予兆演出（新規追加）
            // ============================================
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n\n\n");
            Console.WriteLine($"    所持金: {money:N0}G");
            Thread.Sleep(1000);

            // 画面が少しずつおかしくなる
            for (int i = 0; i < 3; i++)
            {
                Console.WriteLine("\n    .");
                Thread.Sleep(500);
            }

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    ...何かが...おかしい...");
            Thread.Sleep(2000);

            // ============================================
            // フェーズ1: 所持金表示の崩壊
            // ============================================
            Console.Clear();

            for (int i = 0; i < 20; i++)
            {
                Console.Clear();

                // 色がおかしくなる
                Console.ForegroundColor = (ConsoleColor)(rand.Next(1, 16));
                Console.BackgroundColor = i % 4 == 0 ? ConsoleColor.Black : (ConsoleColor)(rand.Next(0, 16));

                Console.WriteLine("\n\n\n");

                // 複数の所持金が同時表示
                long[] glitchValues = {
            money,
            money + rand.Next(-99999999, 99999999),
            -money,
            int.MaxValue,
            int.MinValue,
            rand.Next(0, 999999999)
        };

                foreach (var val in glitchValues.OrderBy(x => rand.Next()))
                {
                    Console.WriteLine($"    所持金: {val:N0}G");
                }

                // ランダムなエラーメッセージ
                if (i > 5)
                {
                    string[] warnings = {
                "WARNING: Value exceeds safe range",
                "CAUTION: Memory corruption detected",
                "ALERT: Integer overflow imminent",
                "ERROR: Boundary check failed",
                "CRITICAL: Stack integrity compromised"
            };
                    Console.WriteLine($"\n    [{warnings[rand.Next(warnings.Length)]}]");
                }

                Thread.Sleep(100 + i * 10);
            }

            // ============================================
            // フェーズ2: システムパニック
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.Red;

            string[] panicMessages = {
        "SYSTEM PANIC",
        "KERNEL PANIC",
        "FATAL ERROR",
        "UNRECOVERABLE ERROR",
        "CATASTROPHIC FAILURE"
    };

            for (int i = 0; i < 10; i++)
            {
                Console.Clear();
                Console.WriteLine("\n\n\n");

                foreach (var msg in panicMessages)
                {
                    Console.ForegroundColor = (ConsoleColor)(rand.Next(9, 16));
                    Console.WriteLine($"    *** {msg} ***");
                }

                Console.WriteLine($"\n\n    OVERFLOW VALUE: {money}");
                Console.WriteLine($"    MAX_INT: {int.MaxValue}");
                Console.WriteLine($"    DIFF: {(long)money - int.MaxValue}");

                Thread.Sleep(150);
            }

            // ============================================
            // フェーズ3: ブルースクリーン風演出
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Blue;
            Console.ForegroundColor = ConsoleColor.White;

            Console.WriteLine("\n\n");
            Console.WriteLine("    :(");
            Console.WriteLine();
            Console.WriteLine("    Your casino has run into a problem and needs to restart.");
            Console.WriteLine("    We're just collecting some error info, and then we'll restart");
            Console.WriteLine("    for you.");
            Thread.Sleep(3000);

            Console.WriteLine("\n    0% complete");
            Thread.Sleep(500);

            for (int i = 0; i <= 100; i += rand.Next(1, 15))
            {
                if (i > 100) i = 100;
                Console.SetCursorPosition(4, Console.CursorTop);
                Console.Write($"    {i}% complete");
                Thread.Sleep(100);
            }

            Thread.Sleep(1000);

            Console.WriteLine("\n\n\n    Technical details:");
            Console.WriteLine($"    Stop code: MONEY_OVERFLOW_EXCEPTION");
            Console.WriteLine($"    Failed component: SlotMachine.Money");
            Console.WriteLine($"    Error value: 0x{money:X}");

            Thread.Sleep(3000);

            // ============================================
            // フェーズ4: マトリックス風データストリーム
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;

            for (int frame = 0; frame < 30; frame++)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;

                for (int row = 0; row < 15; row++)
                {
                    Console.Write("    ");
                    for (int col = 0; col < 50; col++)
                    {
                        if (rand.Next(100) < 30)
                        {
                            char[] chars = "01アイウエオカキクサシスセタチツテナニヌネハヒフヘマミムメヤユヨラリルレワヲン".ToCharArray();
                            Console.Write(chars[rand.Next(chars.Length)]);
                        }
                        else
                        {
                            Console.Write(" ");
                        }
                    }
                    Console.WriteLine();
                }

                Thread.Sleep(100);
            }

            // ============================================
            // フェーズ5: 謎の選択肢（UI完全崩壊版）
            // ============================================

            // 崩壊していくアニメーション
            string[] normalUI = {
        "    ┌────────────────────────────┐",
        "    │                            │",
        "    │         ？？？             │",
        "    │                            │",
        "    └────────────────────────────┘"
    };

            string[][] glitchedUI = {
        new string[] {
            "    ┌─??─────??──────??─────────┐",
            "    │  ??        ??          ??  │",
            "    │      ？？？？？？？？      │",
            "    │  ??        ??          ??  │",
            "    └──??──────??───────??───────┘"
        },
        new string[] {
            "    ╔═??═════??══════??═════════╗",
            "    ║??╔═══╗??╔═══╗??╔═══╗??║",
            "    ║  ║？？║  ║？？║  ║？？║  ║",
            "    ║??╚═══╝??╚═══╝??╚═══╝??║",
            "    ╚══??══════??═══════??═════╝"
        },
        new string[] {
            "    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
            "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓",
            "    ▓░░░░？？？？？？？？░░░░░░▓",
            "    ▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓",
            "    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"
        }
    };

            for (int iteration = 0; iteration < 15; iteration++)
            {
                Console.Clear();
                Console.BackgroundColor = iteration % 3 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                Console.ForegroundColor = (ConsoleColor)(rand.Next(1, 16));

                Console.WriteLine("\n\n\n");

                if (iteration < 5)
                {
                    foreach (var line in normalUI)
                        Console.WriteLine(line);
                }
                else
                {
                    var ui = glitchedUI[rand.Next(glitchedUI.Length)];
                    foreach (var line in ui)
                        Console.WriteLine(line);
                }

                Console.WriteLine("\n\n");
                Console.ForegroundColor = ConsoleColor.Yellow;

                string[] prompts = {
            "         [Enter] ？？？",
            "         [????] ???",
            "         [E̷n̷t̷e̷r̷] ？？？",
            "         [█████] ███",
            "         [UNKNOWN] UNKNOWN"
        };
                Console.WriteLine(prompts[rand.Next(prompts.Length)]);

                Thread.Sleep(200);
            }

            Console.ResetColor();
            Console.ReadKey(true);

            // ============================================
            // フェーズ6: 世界崩壊シーケンス
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;

            string[] destructionMessages = {
        "データベース接続...切断",
        "メモリ整合性...破損",
        "スタックフレーム...崩壊",
        "ヒープ領域...解放失敗",
        "レジスタ値...不正",
        "キャッシュライン...汚染",
        "パイプライン...ストール",
        "分岐予測...失敗",
        "TLB...フラッシュ",
        "ページテーブル...破損"
    };

            foreach (var msg in destructionMessages)
            {
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.Write($"\n    {msg}");
                Thread.Sleep(300);

                for (int i = 0; i < 3; i++)
                {
                    Console.Write(".");
                    Thread.Sleep(200);
                }

                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write(" [FAILED]");
                Thread.Sleep(500);
            }

            Thread.Sleep(2000);

            // ============================================
            // フェーズ7: カウントダウン
            // ============================================
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n\n");
            Console.WriteLine("    システム再起動まで...");
            Thread.Sleep(1500);

            for (int countdown = 10; countdown >= 0; countdown--)
            {
                Console.Clear();

                // カウントダウンのサイズと色を変化
                ConsoleColor[] colors = {
            ConsoleColor.Red, ConsoleColor.DarkRed, ConsoleColor.Yellow,
            ConsoleColor.DarkYellow, ConsoleColor.Magenta
        };
                Console.ForegroundColor = colors[countdown % colors.Length];

                Console.WriteLine("\n\n\n\n");

                // 大きな数字をASCIIアートで表示
                string[] digits = GetBigNumber(countdown);
                foreach (var line in digits)
                {
                    Console.WriteLine("         " + line);
                }

                Thread.Sleep(countdown <= 3 ? 500 : 800);
            }

            // ============================================
            // フェーズ8: ホワイトアウト
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.White;
            Console.ForegroundColor = ConsoleColor.White;

            for (int i = 0; i < 30; i++)
            {
                Console.WriteLine();
            }
            Thread.Sleep(2000);

            // ============================================
            // フェーズ9: 再起動（ゆっくり復帰）
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkGray;

            Console.WriteLine("\n\n\n\n\n\n\n");
            Thread.Sleep(2000);

            Console.Write("    .");
            Thread.Sleep(1000);
            Console.Write(".");
            Thread.Sleep(1000);
            Console.Write(".");
            Thread.Sleep(1500);

            Console.Clear();
            Console.WriteLine("\n\n\n\n\n");
            Console.WriteLine("    起動中...");
            Thread.Sleep(2000);

            // ============================================
            // フェーズ10: システムメッセージ
            // ============================================
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;

            string[] bootMessages = {
        "BIOS Version 2.0.26.42",
        "Memory Test: OK",
        "CPU: Quantum Processor x64",
        "Loading Kernel...",
        "Initializing Casino System...",
        "Checking Integrity...",
        "Loading Player Data...",
        $"Player: {playerName}",
        "Anomaly Detected.",
        "Running Diagnostic..."
    };

            Console.WriteLine("\n\n");
            foreach (var msg in bootMessages)
            {
                Console.WriteLine($"    {msg}");
                Thread.Sleep(400);
            }

            Thread.Sleep(1500);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n    DIAGNOSTIC RESULT:");
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"    >>> OVERFLOW DETECTED: {money:N0}G <<<");
            Thread.Sleep(2000);

            // ============================================
            // フェーズ11: メタメッセージ
            // ============================================
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n\n\n");

            TypewriterEffect("    想定外の富は、世界を壊した。", 50);
            Thread.Sleep(2000);

            Console.WriteLine("\n");
            TypewriterEffect("    ――責任は取らない。", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Console.WriteLine("\n\n\n\n");
            TypewriterEffect("    だが、君は成し遂げた。", 50);
            Thread.Sleep(2000);

            Console.WriteLine("\n");
            TypewriterEffect("    誰も到達しないと思われた領域に。", 50);
            Thread.Sleep(2500);

            Console.WriteLine("\n");
            TypewriterEffect("    整数の限界を超えて。", 50);
            Thread.Sleep(2500);

            Console.WriteLine("\n");
            TypewriterEffect("    システムの壁を突き破って。", 50);
            Thread.Sleep(3000);

            // ============================================
            // フェーズ12: クエスト達成（超豪華演出）
            // ============================================
            Console.Clear();

            // パーティクル風演出
            for (int frame = 0; frame < 20; frame++)
            {
                Console.Clear();
                Console.BackgroundColor = ConsoleColor.Black;

                // ランダムに星を散りばめる
                for (int i = 0; i < 50; i++)
                {
                    int x = rand.Next(0, 50);
                    int y = rand.Next(0, 20);

                    Console.SetCursorPosition(x, y);
                    Console.ForegroundColor = (ConsoleColor)(rand.Next(9, 16));

                    char[] particles = { '*', '✦', '✧', '◆', '◇', '○', '●' };
                    Console.Write(particles[rand.Next(particles.Length)]);
                }

                Thread.Sleep(100);
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;

            // メインタイトル表示
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;

                Console.WriteLine("\n\n");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("    ━━                                      ━━");
                Console.WriteLine("    ━━      隠しクエスト達成！！！        ━━");
                Console.WriteLine("    ━━                                      ━━");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

                Thread.Sleep(300);
            }

            Thread.Sleep(1000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ╔═══════════════════════════════════════════════════╗");
            Console.WriteLine("    ║                                                   ║");
            Console.WriteLine("    ║   🏆 「あぁーあ、開発者が見たら泣くぞ。       ║");
            Console.WriteLine("    ║              by開発者」                           ║");
            Console.WriteLine("    ║                                                   ║");
            Console.WriteLine("    ╚═══════════════════════════════════════════════════╝");

            Thread.Sleep(2000);

            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("    達成情報:");
            Console.WriteLine($"    ├─ 到達所持金: {money:N0}G");
            Console.WriteLine($"    ├─ 到達時間: {FormatTimeSpan(elapsed)}");
            Console.WriteLine($"    ├─ 総回転数: {totalSpins}回");
            Console.WriteLine($"    └─ 設定: {setting}");

            Thread.Sleep(3000);

            // ============================================
            // フェーズ13: RTA判定（超特別演出）
            // ============================================
            if (isRTA)
            {
                Thread.Sleep(1000);

                // 画面フラッシュ
                for (int i = 0; i < 10; i++)
                {
                    Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.Magenta : ConsoleColor.Black;
                    Console.Clear();
                    Thread.Sleep(100);
                }

                Console.Clear();
                Console.BackgroundColor = ConsoleColor.Black;

                // 特別なアニメーション
                string[] rtaArt = {
            "    ██████╗ ████████╗ █████╗ ",
            "    ██╔══██╗╚══██╔══╝██╔══██╗",
            "    ██████╔╝   ██║   ███████║",
            "    ██╔══██╗   ██║   ██╔══██║",
            "    ██║  ██║   ██║   ██║  ██║",
            "    ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝"
        };

                for (int frame = 0; frame < 8; frame++)
                {
                    Console.Clear();
                    Console.ForegroundColor = (ConsoleColor)(9 + (frame % 7));

                    Console.WriteLine("\n\n");
                    foreach (var line in rtaArt)
                    {
                        Console.WriteLine(line);
                    }

                    Thread.Sleep(200);
                }

                Thread.Sleep(1000);

                // 虹色グラデーション演出
                Console.Clear();
                ConsoleColor[] rainbow = {
            ConsoleColor.Red, ConsoleColor.DarkYellow, ConsoleColor.Yellow,
            ConsoleColor.Green, ConsoleColor.Cyan, ConsoleColor.Blue, ConsoleColor.Magenta
        };

                for (int i = 0; i < 3; i++)
                {
                    for (int c = 0; c < rainbow.Length; c++)
                    {
                        Console.Clear();
                        Console.ForegroundColor = rainbow[c];

                        Console.WriteLine("\n\n");
                        Console.WriteLine("    ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★");
                        Console.WriteLine("    ★                                              ★");
                        Console.WriteLine("    ★            RTA 達成！！！！！               ★");
                        Console.WriteLine("    ★         5分以内到達成功！！！               ★");
                        Console.WriteLine("    ★                                              ★");
                        Console.WriteLine("    ★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★");

                        Thread.Sleep(150);
                    }
                }

                Console.Clear();
                Console.BackgroundColor = ConsoleColor.DarkMagenta;
                Console.ForegroundColor = ConsoleColor.White;

                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ╔═════════════════════════════════════════════════╗");
                Console.WriteLine("    ║                                                 ║");
                Console.WriteLine("    ║        🏆🏆🏆 特別クエスト達成 🏆🏆🏆        ║");
                Console.WriteLine("    ║                                                 ║");
                Console.WriteLine("    ║              「  R  T  A  」                   ║");
                Console.WriteLine("    ║                                                 ║");
                Console.WriteLine("    ╚═════════════════════════════════════════════════╝");

                Console.BackgroundColor = ConsoleColor.Black;
                Thread.Sleep(2000);

                Console.WriteLine("\n\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("    ═══════════════════════════════════════");
                Console.WriteLine($"         記録: {elapsed.Minutes:D2}:{elapsed.Seconds:D2}.{elapsed.Milliseconds:D3}");
                Console.WriteLine("    ═══════════════════════════════════════");

                Thread.Sleep(2000);

                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("    ステータス: 🌟 LEGENDARY 🌟");
                Console.WriteLine("    称号: 「時間の支配者」");
                Console.WriteLine("    ランク: SSS+");

                Thread.Sleep(3000);

                // スペシャルメッセージ
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;

                Console.WriteLine("\n\n\n\n");
                TypewriterEffect("    君は伝説となった。", 50);
                Thread.Sleep(2000);

                Console.WriteLine("\n");
                TypewriterEffect("    開発者の友人と同じ偉業を成し遂げた者として。", 50);
                Thread.Sleep(2500);

                Console.WriteLine("\n");
                TypewriterEffect("    5分でゲームを破壊した者として。", 50);
                Thread.Sleep(2500);

                Console.WriteLine("\n");
                TypewriterEffect("    その名は永遠に刻まれる。", 50);
                Thread.Sleep(3000);

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("              開発者からのメッセージ");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                Thread.Sleep(2000);

                Console.WriteLine("\n\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                TypewriterEffect("    「まさか本当に5分で到達する人が", 40);
                Console.WriteLine();
                TypewriterEffect("     現れるとは思わなかった...」", 40);
                Thread.Sleep(2500);

                Console.WriteLine("\n");
                TypewriterEffect("    「友達がやった時は笑ってたけど、", 40);
                Console.WriteLine();
                TypewriterEffect("     君も同じことやるとは...」", 40);
                Thread.Sleep(2500);

                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Magenta;
                TypewriterEffect("    「おめでとう。君は本物だ。」", 40);
                Thread.Sleep(3000);
            }

            // ============================================
            // フェーズ14: 最終エンディング表示
            // ============================================
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;

            // 星空演出
            for (int frame = 0; frame < 30; frame++)
            {
                if (frame % 3 == 0)
                {
                    for (int i = 0; i < 20; i++)
                    {
                        Console.SetCursorPosition(rand.Next(0, 60), rand.Next(0, 20));
                        Console.ForegroundColor = ConsoleColor.White;
                        Console.Write("·");
                    }
                }
                Thread.Sleep(100);
            }

            Console.Clear();

            // エンディングタイトル
            string[] endingTitle = {
        "    ═══════════════════════════════════════════",
        "                                               ",
        "              H I D D E N   E N D              ",
        "                                               ",
        "           - OVERFLOW ACHIEVED -               ",
        "                                               ",
        "    ═══════════════════════════════════════════"
    };

            foreach (var line in endingTitle)
            {
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine(line);
                Thread.Sleep(200);
            }

            Thread.Sleep(2000);

            Console.WriteLine("\n\n");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("    ═══════════════════════════════════════════");
            Console.WriteLine("                 達成記録                    ");
            Console.WriteLine("    ═══════════════════════════════════════════");
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"    プレイヤー名: {playerName}");
            Console.WriteLine($"    最終所持金: {money:N0}G");
            Console.WriteLine($"    到達時間: {FormatTimeSpan(elapsed)}");
            Console.WriteLine($"    総回転数: {totalSpins}回");
            Console.WriteLine($"    777回数: {total777Count}回");
            Console.WriteLine($"    最大連勝: {maxConsecutiveWins}回");

            if (isRTA)
            {
                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine($"    ★ RTA記録: {elapsed.Minutes:D2}:{elapsed.Seconds:D2}.{elapsed.Milliseconds:D3} ★");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━━━━");
            }

            Console.ResetColor();
            Thread.Sleep(5000);

            // ============================================
            // フェーズ15: 哲学的メッセージ
            // ============================================
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Gray;

            Console.WriteLine("\n\n\n\n");
            TypewriterEffect("    システムには限界がある。", 40);
            Thread.Sleep(2000);

            Console.WriteLine("\n");
            TypewriterEffect("    だが、人の欲望には限界がない。", 40);
            Thread.Sleep(2500);

            Console.WriteLine("\n");
            TypewriterEffect("    君はそれを証明した。", 40);
            Thread.Sleep(2500);

            Console.WriteLine("\n");
            TypewriterEffect("    たとえ世界が壊れようとも。", 40);
            Thread.Sleep(3000);

            Thread.Sleep(2000);

            // イベント登録
            if (!unlockedEvents.Contains("OVERFLOW END"))
                unlockedEvents.Add("OVERFLOW END");

            if (isRTA && !unlockedEvents.Contains("RTA達成"))
                unlockedEvents.Add("RTA達成");

            metaEventCount = Math.Max(metaEventCount, 10);

            Thread.Sleep(3000);
        }

        // ========== タイプライター効果 ==========
        static void TypewriterEffect(string text, int delayMs = 50)
        {
            foreach (char c in text)
            {
                Console.Write(c);
                Thread.Sleep(delayMs);
            }
        }

        // ========== 大きな数字のASCIIアート ==========
        static string[] GetBigNumber(int num)
        {
            Dictionary<int, string[]> bigDigits = new Dictionary<int, string[]>
    {
        {0, new string[] {
            " ██████╗ ",
            "██╔═████╗",
            "██║██╔██║",
            "████╔╝██║",
            "╚██████╔╝",
            " ╚═════╝ "
        }},
        {1, new string[] {
            " ██╗",
            "███║",
            "╚██║",
            " ██║",
            " ██║",
            " ╚═╝"
        }},
        {2, new string[] {
            "██████╗ ",
            "╚════██╗",
            " █████╔╝",
            "██╔═══╝ ",
            "███████╗",
            "╚══════╝"
        }},
        {3, new string[] {
            "██████╗ ",
            "╚════██╗",
            " █████╔╝",
            " ╚═══██╗",
            "██████╔╝",
            "╚═════╝ "
        }},
        {4, new string[] {
            "██╗  ██╗",
            "██║  ██║",
            "███████║",
            "╚════██║",
            "     ██║",
            "     ╚═╝"
        }},
        {5, new string[] {
            "███████╗",
            "██╔════╝",
            "███████╗",
            "╚════██║",
            "███████║",
            "╚══════╝"
        }},
        {6, new string[] {
            " ██████╗ ",
            "██╔════╝ ",
            "███████╗ ",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚═════╝ "
        }},
        {7, new string[] {
            "███████╗",
            "╚════██║",
            "    ██╔╝",
            "   ██╔╝ ",
            "   ██║  ",
            "   ╚═╝  "
        }},
        {8, new string[] {
            " ██████╗ ",
            "██╔═══██╗",
            "╚█████╔╝",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚═════╝ "
        }},
        {9, new string[] {
            " ██████╗ ",
            "██╔═══██╗",
            "╚██████╔╝",
            " ╚═══██║ ",
            " █████╔╝ ",
            " ╚════╝  "
        }},
        {10, new string[] {
            " ██╗ ██████╗ ",
            "███║██╔═████╗",
            "╚██║██║██╔██║",
            " ██║████╔╝██║",
            " ██║╚██████╔╝",
            " ╚═╝ ╚═════╝ "
        }}
    };

            return bigDigits.ContainsKey(num) ? bigDigits[num] : bigDigits[0];
        }

        // ========== ローディング画面 ==========
        static void ShowLoadingScreen()
        {
            string[] reelSymbols = { " 7 ", " ★ ", " ♦ ", " ♣ ", " ♠ ", " ♥ ", "BAR", " $ " };

            // ========== リール回転演出（毎フレームClear再描画） ==========
            int spinFrames = 32;
            for (int frame = 0; frame < spinFrames; frame++)
            {
                int r1 = frame % reelSymbols.Length;
                int r2 = (frame + 2) % reelSymbols.Length;
                int r3 = (frame + 4) % reelSymbols.Length;

                // 後半から順番に止まる
                if (frame >= spinFrames - 8) r1 = 0;
                if (frame >= spinFrames - 4) r2 = 0;
                if (frame >= spinFrames - 1) r3 = 0;

                ConsoleColor c1 = r1 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;
                ConsoleColor c2 = r2 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;
                ConsoleColor c3 = r3 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;

                Console.Clear();
                Console.WriteLine("\n\n\n");
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("    ╔═══════════════════════════════════╗");
                Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║");
                Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣");

                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.Write("    ║    ");
                Console.ForegroundColor = c1; Console.Write(reelSymbols[r1]);
                Console.ForegroundColor = ConsoleColor.Cyan; Console.Write("    ║    ");
                Console.ForegroundColor = c2; Console.Write(reelSymbols[r2]);
                Console.ForegroundColor = ConsoleColor.Cyan; Console.Write("    ║    ");
                Console.ForegroundColor = c3; Console.Write(reelSymbols[r3]);
                Console.ForegroundColor = ConsoleColor.Cyan; Console.WriteLine("    ║");

                Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝");
                Console.ResetColor();

                Thread.Sleep(frame < 15 ? 55 : frame < 25 ? 110 : 190);
            }

            // ========== 7 7 7 ピタ止め点滅 ==========
            for (int blink = 0; blink < 7; blink++)
            {
                Console.Clear();
                Console.WriteLine("\n\n\n");
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("    ╔═══════════════════════════════════╗");
                Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║");
                Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣");

                Console.ForegroundColor = blink % 2 == 0 ? ConsoleColor.Red : ConsoleColor.Yellow;
                Console.WriteLine("    ║     7     ║     7     ║     7     ║");

                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝");
                Console.ResetColor();
                Thread.Sleep(240);
            }

            // ========== JACKPOT 確定表示 ==========
            Console.Clear();
            Console.WriteLine("\n\n\n");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("    ╔═══════════════════════════════════╗");
            Console.WriteLine("    ║         S  P  I  N  N  I  N  G   ║");
            Console.WriteLine("    ╠═══════════╦═══════════╦═══════════╣");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("    ║     7     ║     7     ║     7     ║");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("    ╚═══════════╩═══════════╩═══════════╝");
            Console.ResetColor();
            Thread.Sleep(400);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n      ★★★  J A C K P O T  ★★★");
            Console.ResetColor();
            Thread.Sleep(800);

            // ========== プログレスバー ==========
            Console.WriteLine();
            int barWidth = 30;
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write("    [");
            Console.ResetColor();
            for (int i = 0; i < barWidth; i++)
            {
                Console.ForegroundColor = i < barWidth * 0.5 ? ConsoleColor.Green
                                        : i < barWidth * 0.8 ? ConsoleColor.Yellow
                                        : ConsoleColor.Cyan;
                Console.Write("█");
                Thread.Sleep(38);
            }
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write("]");
            Console.ResetColor();

            // ========== カジノへようこそ ==========
            Console.WriteLine("\n");
            foreach (char c in "    カジノへようこそ。")
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.Write(c);
                Thread.Sleep(80);
            }
            Console.ResetColor();
            Thread.Sleep(1500);
        }

        // ========== 設定示唆 ==========
        static void ChangeMachine()
        {
            if (money < 2000)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n所持金が足りません... (2000G必要)");
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n台を変えますか？ (2000G) [Y/N]");
            Console.ResetColor();

            var confirm = Console.ReadKey(true);
            if (confirm.Key != ConsoleKey.Y) return;

            money -= 2000;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n    台を移動する...");
            Thread.Sleep(1500);

            // 設定6だけ少し優遇
            int[] settingPool = { 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6 };
            setting = settingPool[rand.Next(settingPool.Length)];

            // 起動音演出
            string[] suggestions = {
        "起動音が普通だ...",
        "起動音が少し高い...",
        "起動音がやや高い！",
        "起動音が高い！！",
        "起動音がかなり高い！！！",
        "起動音が異常に高い！！！！"
    };

            Console.WriteLine($"\n    {suggestions[setting - 1]}");
            Thread.Sleep(1500);

            if (setting == 6)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n    （これは...高設定の予感！？）");
                Console.ResetColor();
                Thread.Sleep(2000);

                if (!unlockedEvents.Contains("設定6解放"))
                    unlockedEvents.Add("設定6解放");
            }

            Thread.Sleep(1500);
        }

        // ========== ミッション初期化 ==========
        static void InitializeMissions()
        {
            // 既存ミッション（1-11）
            missions.Add(new Mission("初心者", "50G以下で1回勝利", () => consecutiveWins >= 1 && money <= 1050, 100));
            missions.Add(new Mission("連勝の始まり", "3連勝を達成", () => consecutiveWins >= 3, 200));
            missions.Add(new Mission("連勝マスター", "5連勝を達成", () => consecutiveWins >= 5, 500));
            missions.Add(new Mission("無借金主義", "借金せずに所持金2000G達成", () => money >= 2000 && debt == 0, 300));
            missions.Add(new Mission("777ハンター", "777を1回揃える", () => total777Count >= 1, 1000));
            missions.Add(new Mission("借金返済の達人", "借金を完済する", () => debt == 0 && hasEverBorrowedMoney, 300));
            missions.Add(new Mission("GODへの道", "100G連続10回プレイ", () => consecutiveHundredPlays >= 10, 200));
            missions.Add(new Mission("粘り強さ", "20回転連続でプレイ", () => totalSpins >= 20, 150));
            missions.Add(new Mission("強運の持ち主", "設定6を引き当てる", () => setting == 6, 500));
            missions.Add(new Mission("ギャンブラー", "総回転数100回達成", () => totalSpins >= 100, 1000));
            missions.Add(new Mission("強欲", "幸運のコインを10個購入", () => totalLuckyCoinsPurchased >= 10, 0));
            missions.Add(new Mission("破滅への道", "強欲の指輪装備中に借金5000G到達", () => greedRingEquipped && debt >= 5000, 0));

            // VIPルーム関連（12-15）
            missions.Add(new Mission("セレブへの道", "所持金10000G到達してVIPルーム解放", () => money >= 10000 && vipRoomUnlocked, 0));
            missions.Add(new Mission("VIPの洗礼", "VIPルームで初勝利", () => vipTotalWins >= 1, 1000));
            missions.Add(new Mission("ハイローラー", "VIPルームで5000Gベットで勝利", () => vip5000BetWin, 3000));
            missions.Add(new Mission("VIPマスター", "VIPルームで777を揃える", () => vip777Count >= 1, 5000));

            // 地下カジノ関連（16-20）
            missions.Add(new Mission("奈落への扉", "地下カジノを解放", () => undergroundUnlocked, 0));
            missions.Add(new Mission("地獄の訪問者", "地下カジノに初めて入る", () => undergroundVisits >= 1, 500));
            missions.Add(new Mission("奈落の生還者", "地下カジノで1回勝利", () => undergroundWins >= 1, 0));
            missions.Add(new Mission("闇の常連客", "地下カジノを5回訪問", () => undergroundVisits >= 5, 2000));
            missions.Add(new Mission("奈落の覇者", "地下カジノで全財産ベットして勝利", () => undergroundAllInWin, 10000));

            // 悪魔契約関連（21-24）
            missions.Add(new Mission("悪魔の誘惑", "悪魔から契約を提示される", () => devilContractOffered, 0));
            missions.Add(new Mission("契約者", "悪魔と契約する（種類問わず）", () => devilContractActive, 1500));
            missions.Add(new Mission("魂の代償", "契約1「魂の担保」で10連勝達成", () => contract1Complete, 5000));
            missions.Add(new Mission("悪魔を欺く者", "いずれかの契約を成功させる", () => devilContractSuccess, 0));

            // 中毒システム関連（25-29）
            missions.Add(new Mission("止まらない", "中毒度20到達", () => addictionLevel >= 20, 300));
            missions.Add(new Mission("依存症", "中毒度50到達", () => addictionLevel >= 50, 800));
            missions.Add(new Mission("末期症状", "中毒度80到達", () => addictionLevel >= 80, 0));
            missions.Add(new Mission("制御不能", "中毒度100到達", () => addictionLevel >= 100, 0));
            missions.Add(new Mission("更生の道", "リハビリ券で中毒度を50以下に下げる", () => hasUsedRehab && addictionLevel <= 50, 3000));

            // 呪いアイテム関連（30-35）
            missions.Add(new Mission("禁断の力", "呪いのアイテムを1つ入手", () => cursedItemCount >= 1, 500));
            missions.Add(new Mission("コレクター", "呪いのアイテムを3種類入手", () => cursedItemCount >= 3, 1500));
            missions.Add(new Mission("呪われし者", "呪いのアイテムを全種類入手", () => cursedItemCount >= 5, 0));
            missions.Add(new Mission("悪魔のささやき", "悪魔のコインで勝利", () => devilCoinWin, 1000));
            missions.Add(new Mission("血の契約", "血塗られたお守りを装備して5連勝", () => bloodAmulet5Wins >= 5, 2000));
            missions.Add(new Mission("死神との賭け", "死神の指輪で10回勝利", () => deathRing10Wins >= 10, 5000));

            // メタ・その他関連（36-40）
            missions.Add(new Mission("第四の壁", "メタ演出を3種類以上体験", () => metaEventCount >= 3, 2000));
            missions.Add(new Mission("真実を知る者", "全てのイベントを閲覧", () => unlockedEvents.Count >= 20, 3000));
            missions.Add(new Mission("完全主義者", "全ての絵柄を解放", () => unlockedSymbols.Count >= 8, 2000));
            missions.Add(new Mission("生存者", "借金20000G以上から完済", () => maxDebt >= 20000 && debt == 0, 10000));
            missions.Add(new Mission("伝説のギャンブラー", "全ミッション達成", () => missions.Count(m => m.Completed) >= 40, 0));

            // 隠しミッション（41-46）
            missions.Add(new Mission("???", "???", () => totalLoses >= 100, 5000));
            missions.Add(new Mission("???", "???", () => consecutiveWins >= 20, 0));
            missions.Add(new Mission("???", "???", () => money == 6666, 0));
            missions.Add(new Mission("???", "???", () => totalSpins == 777, 0));
            missions.Add(new Mission("???", "???", () => missions.Count(m => m.Completed) >= 44, 0));
            missions.Add(new Mission("???", "???", () => money >= 10000 && total777Count >= 3, 0));
        }

        // ========== 中毒システム追加変数 ==========
        static List<string> addictionMessages = new List<string>
{
    "もう1回だけ...",
    "次で取り戻せる...",
    "やめられない...",
    "あと少しで大当たり...",
    "画面が...歪んで見える...",
    "これは...夢か...？",
    "声が...聞こえる...",
    "誰かが...呼んでいる..."
};

        // ========== メインゲームループ ==========
        // ========== GameLoop内、冒頭部分を修正 ==========
        static void GameLoop()
        {
            while (true)
            {
                // 🆕 オーバーフローチェック（マイナス表示検出）
                // int型の限界を超えてマイナスになった場合
                // より確実なオーバーフロー検出
                if (money < 0 || money >= int.MaxValue - 10000)
                {
                    OverflowHiddenEnding();
                    break;
                }

                // godModePermanent有効時は常にGOD MODE維持
                if (godModePermanent && !godMode)
                {
                    godMode = true;
                    godModeRemaining = 10;
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n★ 永続GOD MODE 再発動！ ★");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }

                // または、1億以上でも発動（安全装置）
                if (money >= 100000000)
                {
                    OverflowHiddenEnding();
                    break;
                }

                // VIPルーム解放チェック
                if (!vipRoomUnlocked && money >= 10000)
                {
                    VIPRoomUnlockEvent();
                    vipRoomUnlocked = true;
                    if (!unlockedEvents.Contains("VIPルーム解放"))
                        unlockedEvents.Add("VIPルーム解放");
                }
                // GameLoop内に追加（VIP解放チェックの下）
                // 借金5000G以上で地下解放
                if (!undergroundUnlocked && debt >= 5000)
                {
                    UndergroundUnlockByDebt();
                    undergroundUnlocked = true;
                    if (!unlockedEvents.Contains("地下カジノ解放"))
                        unlockedEvents.Add("地下カジノ解放");
                }
                // GameLoop内、イベントチェック部分に追加

                // メタ演出1: セーブ削除の脅し
                if (metaEventCount < 1 && totalSpins > 30 && rand.Next(500) == 0)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    ⚠⚠⚠ 警告 ⚠⚠⚠");
                    Console.WriteLine("\n    セーブデータを削除しますか？");
                    Console.WriteLine("\n    [Y] 削除する");
                    Console.WriteLine("    [N] キャンセル");
                    Console.ResetColor();

                    var metaKey = Console.ReadKey(true);

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n\n\n    ...冗談だよ");
                    Console.WriteLine("\n    でも次は本当かもしれない");
                    Console.ResetColor();
                    Thread.Sleep(3000);

                    metaEventCount++;
                    if (!unlockedEvents.Contains("メタ演出1"))
                        unlockedEvents.Add("メタ演出1");
                }

                // GameLoop内にこれがない
                if (addictionLevel >= 100)
                {
                    AddictionBadEnding();
                    break;
                }

                // メタ演出2: フェイクエラー画面
                if (metaEventCount >= 1 && metaEventCount < 2 && totalSpins > 50 && rand.Next(500) == 0)
                {
                    Console.Clear();
                    Console.BackgroundColor = ConsoleColor.Blue;
                    Console.ForegroundColor = ConsoleColor.White;
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    :(");
                    Console.WriteLine("\n    FEWJS_CASINO_CRITICAL_ERROR");
                    Console.WriteLine("\n    問題が発生したため、ゲームを再起動します。");
                    Console.WriteLine("    セーブデータは...保護されています。多分。");
                    Thread.Sleep(3000);

                    Console.WriteLine("\n\n    0% 回復中...");
                    for (int i = 0; i <= 100; i += rand.Next(3, 15))
                    {
                        if (i > 100) i = 100;
                        Console.SetCursorPosition(4, Console.CursorTop);
                        Console.Write($"    {i}% 回復中...");
                        Thread.Sleep(80);
                    }

                    Thread.Sleep(1000);
                    Console.BackgroundColor = ConsoleColor.Black;
                    Console.ResetColor();
                    Console.Clear();
                    Console.WriteLine("\n\n    ...再起動完了");
                    Console.WriteLine("\n    やっぱり冗談だよ");
                    Thread.Sleep(2000);

                    metaEventCount++;
                    if (!unlockedEvents.Contains("メタ演出2"))
                        unlockedEvents.Add("メタ演出2");
                }

                // メタ演出3: 実名呼び出し
                if (metaEventCount >= 2 && metaEventCount < 3 && totalSpins > 70 && rand.Next(500) == 0)
                {
                    string realName = Environment.UserName;

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    ...ねえ");
                    Thread.Sleep(2000);

                    Console.WriteLine($"\n    {realName}さん");
                    Thread.Sleep(2000);

                    Console.WriteLine("\n    まだやめないの？");
                    Thread.Sleep(2000);

                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n\n    （あなたのPCのユーザー名から取得しました）");
                    Console.ResetColor();
                    Thread.Sleep(3000);

                    metaEventCount++;
                    if (!unlockedEvents.Contains("メタ演出3"))
                        unlockedEvents.Add("メタ演出3");
                }

                // メタ演出4: カーソル異常
                if (metaEventCount >= 3 && metaEventCount < 4 && totalSpins > 90 && rand.Next(500) == 0)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.White;
                    Console.WriteLine("\n\n\n    何かがおかしい...");
                    Thread.Sleep(1500);

                    // カーソルが暴れる
                    Console.CursorVisible = true;
                    for (int i = 0; i < 20; i++)
                    {
                        int x = rand.Next(0, Console.WindowWidth - 1);
                        int y = rand.Next(0, Console.WindowHeight - 1);
                        try { Console.SetCursorPosition(x, y); } catch { }
                        Thread.Sleep(100);
                    }

                    // カーソルが消える
                    Console.CursorVisible = false;
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.SetCursorPosition(0, 0);
                    Console.WriteLine("\n\n\n    カーソルが...言うことを聞かない...");
                    Thread.Sleep(2000);
                    Console.WriteLine("\n    ...落ち着いた");
                    Thread.Sleep(2000);
                    Console.ResetColor();

                    metaEventCount++;
                    if (!unlockedEvents.Contains("メタ演出4"))
                        unlockedEvents.Add("メタ演出4");
                }

                // メタ演出5: 時間逆行演出
                if (metaEventCount >= 4 && metaEventCount < 5 && totalSpins > 110 && rand.Next(500) == 0)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine("\n\n\n    時間が...");
                    Thread.Sleep(1500);
                    Console.WriteLine("\n    逆流している...");
                    Thread.Sleep(1500);

                    // 回転数が戻っていくように見せる
                    for (int i = totalSpins; i >= totalSpins - 10; i--)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        Console.WriteLine("\n\n\n");
                        Console.WriteLine($"    総回転数: {i}回");
                        Console.WriteLine("\n    時間が巻き戻っている...");
                        Thread.Sleep(200);
                    }

                    Thread.Sleep(500);
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.White;
                    Console.WriteLine("\n\n\n    ...元に戻った");
                    Console.WriteLine($"\n    総回転数: {totalSpins}回");
                    Console.WriteLine("\n    （回転数は実際には減っていません）");
                    Console.ResetColor();
                    Thread.Sleep(3000);

                    metaEventCount++;
                    if (!unlockedEvents.Contains("メタ演出5"))
                        unlockedEvents.Add("メタ演出5");
                }



                // 中毒幻覚
                if (addictionLevel >= 61 && rand.Next(100) < 10)
                {
                    AddictionHallucinationEffect();
                }

                // 中毒メッセージ
                if (addictionLevel >= 21 && rand.Next(100) < 15)
                {
                    ShowAddictionMessage();
                }
                // 中毒度100でBAD END
                if (addictionLevel >= 100)
                {
                    AddictionBadEnding();
                    break;
                }
                // 悪魔契約発動条件チェック
                if (!devilContractOffered && !devilContractActive)
                {
                    if (debt >= 10000 || totalLoses >= 50 || (undergroundTotalSpins > 0 && undergroundConsecutiveLoses >= 10))
                    {
                        DevilContractOfferEvent();
                        devilContractOffered = true;
                        if (!unlockedEvents.Contains("悪魔の誘惑"))
                            unlockedEvents.Add("悪魔の誘惑");
                    }
                }

                // 契約1（魂の担保）処理
                if (devilContractActive && devilContractType == 1)
                {
                    if (contract1Complete)
                    {
                        // 10連勝達成 → 成功演出
                        DevilContract1Success();
                        devilContractActive = false;
                        devilContractSuccess = true;
                        if (!unlockedEvents.Contains("悪魔契約成功"))
                            unlockedEvents.Add("悪魔契約成功");
                    }
                    else if (consecutiveLosses >= 1 && contract1WinCount > 0)
                    {
                        // 連勝が途切れた → BAD END
                        DevilContract1BadEnding();
                        break;
                    }
                }

                // 契約2（時間との取引）処理
                if (devilContractActive && devilContractType == 2)
                {
                    TimeSpan remaining = contract2Deadline - DateTime.Now;
                    if (remaining.TotalSeconds <= 0)
                    {
                        DevilContract2TimeUpEnding();
                        break;
                    }

                    // 完済チェック
                    if (debt == 0)
                    {
                        DevilContract2Success();
                        devilContractActive = false;
                        devilContractSuccess = true;
                    }
                }

                // 強欲の指輪装備中で借金5000G以上
                if (greedRingEquipped && debt >= 5000)
                {
                    GreedRingBadEnding();
                    break;
                }

                // TRUEエンディングチェック
                if (!trueEndingUnlocked && CheckTrueEndCondition())
                {
                    trueEndingUnlocked = true;
                    TrueEnding();
                    break;
                }

                // チャプター1：夢カジノ1層クリア後に解放
                if (dreamLayerCleared >= 1 && !chapter1Seen)
                {
                    Chapter1_FirstConversation();
                    chapter1Seen = true;
                }

                // 廃娯楽施設：チャプター1クリア後にショップ隠しページ解放通知（初回のみ）
                if (chapter1Seen && !vanityKeyPurchased && !abandonedCasinoUnlocked
                    && totalSpins > 0 && totalSpins % 10 == 0 && rand.Next(3) == 0)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    TypewriterEffect("\n\n    ベルのショップに　何か新しいページが...", 40);
                    Console.ResetColor();
                    Thread.Sleep(2000);
                }

                if (money <= 0 && debt > 0)
                {
                    DebtCollectionEvent();
                    break;
                }

                if (debt > 0 && debtTurnsRemaining > 0)
                {
                    debtTurnsRemaining--;
                    if (debtTurnsRemaining == 0)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\n借金の期限が切れた...");
                        Thread.Sleep(2000);
                        Console.ResetColor();
                        DebtCollectionEvent();
                        break;
                    }
                }


                // 借金最大値記録
                if (debt > maxDebt) maxDebt = debt;

                if (!hasSeenConversation && rand.Next(100) < 8)
                {
                    RandomConversationEvent();
                    hasSeenConversation = true;
                    if (!unlockedEvents.Contains("謎のおじさん"))
                        unlockedEvents.Add("謎のおじさん");
                }

                if (!hasSeenMysteriousWoman && rand.Next(100) < 10 && totalSpins > 10)
                {
                    MysteriousWomanEvent();
                    hasSeenMysteriousWoman = true;
                    if (!unlockedEvents.Contains("ミステリアスなお姉さん"))
                        unlockedEvents.Add("ミステリアスなお姉さん");
                }

                if (rand.Next(2000) == 0 && totalSpins > 5 && !greedRingEquipped)
                {
                    Devilmonster();
                    if (!unlockedEvents.Contains("悪魔の怪物"))
                        unlockedEvents.Add("悪魔の怪物");
                }

                if (bigWinCount >= 3 && rand.Next(100) < 30 && !greedRingEquipped)
                {
                    BlackSuitWarningEvent();
                    bigWinCount = 0;
                    if (!unlockedEvents.Contains("黒服の警告"))
                        unlockedEvents.Add("黒服の警告");
                }

                if (greedRingEquipped && rand.Next(100) < 15)
                {
                    GreedWhisperEvent();
                }

                Console.Clear();

                if (greedRingEquipped)
                {
                    Console.BackgroundColor = ConsoleColor.DarkRed;
                    Console.ForegroundColor = ConsoleColor.Black;
                }

                DrawTitle();

                if (greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.BackgroundColor = ConsoleColor.Black;
                    Console.WriteLine($"\n💀💀💀 強欲のオーラ 発動中 💀💀💀");
                    Console.WriteLine($"負け: -500G | 勝ち: ×5倍");
                    Console.ResetColor();
                }

                if (godMode && godModeRemaining > 0 && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                    Console.ResetColor();
                }

                if (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"\n☆☆☆ ラッキータイム！残り{luckyTimeRemaining}回 ☆☆☆");
                    Console.ResetColor();
                }

                if (addictionLevel >= 1)
                {
                    Console.Write("\n⚠ 中毒度: ");
                    Console.Write(GetAddictionBar(addictionLevel));
                    Console.ResetColor();
                    Console.WriteLine(" ⚠");
                }

                if (hasTimeClock)
                {
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine($"\n🕐 現在時刻: {DateTime.Now:HH:mm}");
                    Console.ResetColor();
                }

                Console.WriteLine($"\nプレイヤー: {playerName}");
                Console.WriteLine($"所持金: {money}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    if (debtTurnsRemaining > 0)
                    {
                        Console.WriteLine($"返済期限: あと{debtTurnsRemaining}回転");
                    }
                    Console.ResetColor();
                }

                if (consecutiveHundredPlays > 0 && !godMode && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"100G連続プレイ: {consecutiveHundredPlays}/20回");
                    Console.ResetColor();
                }

                ShowUncompletedMissions();

                Console.WriteLine("\n┌────────────────────────────┐");
                Console.WriteLine("│  [1] 50G でプレイ         │");
                Console.WriteLine("│  [2] 100G でプレイ        │");
                if (money < 50)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("│  [3] 借金する (500G)      │");
                    Console.ResetColor();
                }
                if (vipRoomUnlocked)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("│  [V] VIPルームへ          │");
                    Console.ResetColor();
                }
                if (undergroundUnlocked)
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("│  [U] 地下カジノへ         │");
                    Console.ResetColor();
                }
                // 🆕 悪魔契約メニュー追加
                if (devilContractOffered && !devilContractActive)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("│  [D] 悪魔との契約...      │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [M] ミッション確認       │");
                Console.WriteLine("│  [S] ショップ             │");
                if (abandonedCasinoUnlocked)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("│  [A] 廃娯楽施設           │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [E] 装備管理             │");
                Console.WriteLine("│  [R] ランキング           │");
                Console.WriteLine("│  [C] コレクション         │");
                Console.WriteLine("│  [T] 台を変える (2000G)   │");
                Console.WriteLine("│  [F5] セーブ              │");
                Console.WriteLine("│  [F9] ロード              │");
                Console.WriteLine("│  [0] 終了                 │");
                Console.WriteLine("└────────────────────────────┘");

                // メニューグリッチ（中毒度80%以上で低確率発動）
                MenuGlitch();

                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);
                int bet = 0;

                if (key.KeyChar == 's' || key.KeyChar == 'S')
                {
                    ShopMenu();
                    continue;
                }

                if ((key.KeyChar == 'a' || key.KeyChar == 'A') && abandonedCasinoUnlocked)
                {
                    EnterAbandonedCasino();
                    continue;
                }

                if (key.KeyChar == 'e' || key.KeyChar == 'E')
                {
                    EquipmentMenu();
                    continue;
                }
                if ((key.KeyChar == 'd' || key.KeyChar == 'D') && devilContractOffered && !devilContractActive)
                {
                    DevilContractMenu();
                    continue;
                }

                if (key.KeyChar == 'r' || key.KeyChar == 'R')
                {
                    ShowRankings();
                    continue;
                }

                if (key.KeyChar == 'c' || key.KeyChar == 'C')
                {
                    ShowCollection();
                    continue;
                }

                if (key.KeyChar == 'm' || key.KeyChar == 'M')
                {
                    ShowAllMissions();
                    continue;
                }

                if (key.Key == ConsoleKey.F5)
                {
                    SaveMenu();
                    continue;
                }

                if (key.Key == ConsoleKey.F9)
                {
                    LoadMenu();
                    continue;
                }

                if ((key.KeyChar == 'v' || key.KeyChar == 'V') && vipRoomUnlocked)
                {
                    VIPRoomLoop();
                    continue;
                }

                if ((key.KeyChar == 'u' || key.KeyChar == 'U') && undergroundUnlocked)
                {
                    UndergroundLoop();
                    continue;
                }

                if (key.KeyChar == 't' || key.KeyChar == 'T')
                {
                    ChangeMachine();
                    continue;
                }

                if (key.KeyChar == '0')
                {
                    // メタ演出6: 終了拒否強化
                    if (metaEventCount >= 5 && rand.Next(3) == 0)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine("\n\n\n    終了？");
                        Thread.Sleep(1500);
                        Console.WriteLine("\n    ...できないよ");
                        Thread.Sleep(1500);

                        // フェイク終了処理
                        Console.WriteLine("\n\n    終了中...");
                        for (int i = 0; i <= 100; i += rand.Next(5, 20))
                        {
                            if (i > 100) i = 100;
                            Console.Write($"\r    [{i}%]");
                            Thread.Sleep(100);
                        }

                        Thread.Sleep(500);
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("\n\n\n    ...やっぱりまだ終われない");
                        Console.WriteLine("\n    もう1回だけ");
                        Console.ResetColor();
                        Thread.Sleep(2000);

                        if (!unlockedEvents.Contains("メタ演出6"))
                            unlockedEvents.Add("メタ演出6");
                        continue;
                    }

                    // 中毒度61以上で終了拒否（既存コード）
                    if (addictionLevel >= 61)
                    {
                        int confirmCount = addictionLevel >= 81 ? 5 : 3;
                        for (int i = 0; i < confirmCount; i++)
                        {
                            Console.Clear();
                            Console.ForegroundColor = ConsoleColor.DarkRed;
                            Console.WriteLine("\n\n本当にやめますか？ [Y/N]");
                            if (addictionLevel >= 81)
                            {
                                Console.WriteLine("\n...やめられない...");
                                Console.WriteLine("...もう1回...");
                            }
                            Console.ResetColor();
                            var confirm = Console.ReadKey(true);
                            if (confirm.Key == ConsoleKey.Y)
                            {
                                if (i == confirmCount - 1)
                                    break;
                            }
                            else { continue; }
                        }
                        if (addictionLevel >= 81)
                        {
                            Console.Clear();
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\n...もう1回だけ...");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                            continue;
                        }
                    }
                    break;
                }
                else if (key.KeyChar == '1')
                {
                    // 中毒度41以上で50Gベット不可
                    if (addictionLevel >= 41 && addictionLevel < 81)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine("\n\n50Gじゃ...足りない...");
                        Console.WriteLine("もっと...もっと賭けたい...");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                        continue;
                    }

                    bet = 50;
                    if (!godMode && !greedRingEquipped)
                    {
                        consecutiveHundredPlays = 0;
                    }
                }
                else if (key.KeyChar == '2')
                {
                    // 中毒度81以上で自動的に100Gに変更
                    if (addictionLevel >= 81)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\n制御できない...");
                        Console.WriteLine("100Gを賭けてしまう...");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                    }

                    bet = 100;
                    if (!godMode && !greedRingEquipped)
                    {
                        consecutiveHundredPlays++;

                        if (consecutiveHundredPlays >= 20)
                        {
                            GodModeActivation();
                            consecutiveHundredPlays = 0;
                        }
                    }
                }

                else if (key.KeyChar == '3' && money < 50)
                {
                    BlackSuitArrival();
                    money += 500;
                    debt += 500;
                    hasEverBorrowedMoney = true;
                    debtTurnsRemaining = 20;
                    if (!godMode && !greedRingEquipped)
                    {
                        consecutiveHundredPlays = 0;
                    }
                    if (!unlockedEvents.Contains("黒服登場"))
                        unlockedEvents.Add("黒服登場");
                    continue;
                }
                else
                {
                    Console.WriteLine("\n正しい選択をしてください");
                    Thread.Sleep(1000);
                    continue;
                }

                if (bet > money)
                {
                    Console.WriteLine("\n所持金不足！借金しますか？");
                    Thread.Sleep(1500);
                    continue;
                }


                money -= bet;
                totalSpins++;

                // オートセーブ
                autoSaveTurns++;
                if (autoSaveTurns >= AUTO_SAVE_INTERVAL)
                {
                    try
                    {
                        SaveGame(0);
                        autoSaveTurns = 0;
                    }
                    catch { }
                }

                if (!luckyTimeActive && rand.Next(1000) < 5 && !greedRingEquipped)
                {
                    LuckyTimeActivation();
                }

                // 通常スピン処理（既存コードと同じ）
                NormalSpin(bet);

                Console.WriteLine("\n\n何かキーを押して続ける...");
                Console.ReadKey(true);
            }
        }

        // ========== 通常スピン処理（既存コードから抽出）==========
        static void NormalSpin(int bet)
        {
            DateTime spinStartTime = DateTime.Now;

            Console.Clear();

            if (greedRingEquipped)
            {
                Console.BackgroundColor = ConsoleColor.DarkRed;
                Console.ForegroundColor = ConsoleColor.Black;
            }

            DrawTitle();

            if (greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.BackgroundColor = ConsoleColor.Black;
                Console.WriteLine($"\n💀💀💀 強欲のオーラ 発動中 💀💀💀");
                Console.ResetColor();
            }

            if (godMode && godModeRemaining > 0 && !greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                Console.ResetColor();
            }

            if (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"\n☆☆☆ ラッキータイム！残り{luckyTimeRemaining}回 ☆☆☆");
                Console.ResetColor();
            }

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(new int[] { 0, 1, 2 });
            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("        ▼ 回転開始！ ▼");
            Console.ResetColor();
            Thread.Sleep(800);

            bool freezeEffect = false;
            bool premiumEffect = false;

            if (!greedRingEquipped)
            {
                freezeEffect = rand.Next(1000) < 1;
                if (freezeEffect)
                {
                    FreezeEffect();
                    if (!unlockedEvents.Contains("フリーズ演出"))
                        unlockedEvents.Add("フリーズ演出");
                }

                premiumEffect = rand.Next(1000) < 5;

                if (premiumEffect)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n        ！！！画面フラッシュ！！！");
                    Console.ResetColor();
                    Thread.Sleep(300);
                    Console.Clear();
                    DrawTitle();
                    Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
                    if (debt > 0)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine($"借金: {debt}G");
                        Console.ResetColor();
                    }
                    Console.WriteLine("\n");
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("           ★★★★★★★★★★★★★★★★★★★");
                    Console.WriteLine("         ★                                　★");
                    Console.WriteLine("       ★      　プレミア演出発生！       ★");
                    Console.WriteLine("     ★                                ★");
                    Console.WriteLine("    ★★★★★★★★★★★★★★★★★");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                }
            }

            for (int t = 0; t < 25; t++)
            {
                int[] reels = { rand.Next(symbols.Length), rand.Next(symbols.Length), rand.Next(symbols.Length) };
                Console.Clear();

                // スピン中グリッチ（中毒度/悪魔契約で発動）
                if (t == 12) SpinGlitch();

                if (greedRingEquipped)
                {
                    Console.BackgroundColor = ConsoleColor.DarkRed;
                    Console.ForegroundColor = ConsoleColor.Black;
                }

                DrawTitle();

                if (greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.BackgroundColor = ConsoleColor.Black;
                    Console.WriteLine($"\n💀💀💀 強欲のオーラ 発動中 💀💀💀");
                    Console.ResetColor();
                }

                if (godMode && godModeRemaining > 0 && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                    Console.ResetColor();
                }

                if (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"\n☆☆☆ ラッキータイム！残り{luckyTimeRemaining}回 ☆☆☆");
                    Console.ResetColor();
                }

                Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    Console.ResetColor();
                }
                Console.WriteLine("\n");

                if (premiumEffect && t % 2 == 0 && !greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                }

                DrawReels(reels);
                Console.ResetColor();

                int delay = t < 15 ? 60 : 60 + (t - 15) * 20;
                Thread.Sleep(delay);
            } // ← このカッコの直後に挿入

            // 🆕 時計装備時の制限時間チェック
            if (timeClockEquipped)
            {
                TimeSpan elapsed = DateTime.Now - spinStartTime;

                if (elapsed.TotalSeconds > 3)
                {
                    // 3秒超過 → 強制負け
                    Console.Clear();

                    Console.BackgroundColor = ConsoleColor.Black;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    ⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰");
                    Console.WriteLine("    ⏰                          　　⏰");
                    Console.WriteLine("    ⏰        時間切れ！！！        ⏰");
                    Console.WriteLine("    ⏰                              ⏰");
                    Console.WriteLine("    ⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰⏰");
                    Thread.Sleep(1500);

                    Console.Clear();
                    DrawTitle();
                    Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
                    Console.WriteLine("\n");

                    // ランダムなハズレ結果
                    int[] loseResult = {
            rand.Next(5, symbols.Length),
            rand.Next(5, symbols.Length),
            rand.Next(5, symbols.Length)
        };
                    DrawReels(loseResult);

                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("\n           ⏰ 制限時間超過... ⏰");
                    Console.ResetColor();
                    Thread.Sleep(1500);

                    totalLoseAmount += bet;
                    totalLoses++;
                    consecutiveWins = 0;

                    // 血お守りの処理
                    if (bloodAmuletEquipped)
                    {
                        bloodAmuletLoses++;

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血の呪い: {bloodAmuletLoses}/3回");
                        Console.ResetColor();
                        Thread.Sleep(1500);

                        if (bloodAmuletLoses >= 3)
                        {
                            BloodAmuletBadEnding();
                            return;
                        }
                    }

                    // 死神の指輪ペナルティ
                    if (deathRingEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Magenta;
                        Console.WriteLine("\n💀 死神の呪い: -1000G");
                        Console.ResetColor();
                        Thread.Sleep(1500);

                        if (money >= 1000)
                        {
                            money -= 1000;
                            totalLoseAmount += 1000;
                        }
                        else
                        {
                            int shortage = 1000 - money;
                            totalLoseAmount += money;
                            money = 0;
                            debt += shortage;
                            hasEverBorrowedMoney = true;

                            Console.ForegroundColor = ConsoleColor.DarkRed;
                            Console.WriteLine($"\n所持金不足...{shortage}Gが借金に追加された");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                        }
                    }

                    return; // スピン処理を終了
                }
            }

            // ========== リール結果決定 ==========
            int[] result = new int[3];
            int luckBonus = 0;

            // 🆕 悪魔のコイン: 次回100%勝利
            if (devilCoinActive && !devilCoinWin)
            {
                result[0] = 2;
                result[1] = 2;
                result[2] = 2;
                devilCoinWin = true;

                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n💀 悪魔のコインの力！ 💀");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            // 🆕 悪魔のコイン: 呪い発動中（5回強制負け）
            else if (devilCoinActive && devilCoinWin && devilCoinCurse < 5)
            {
                result[0] = 5;
                result[1] = 6;
                result[2] = 7;
                devilCoinCurse++;

                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine($"\n💀 呪いの代償...({devilCoinCurse}/5) 💀");
                Console.ResetColor();
                Thread.Sleep(1500);

                if (devilCoinCurse >= 5)
                {
                    devilCoinActive = false;
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n呪いが解けた...");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }
            // 🆕 水晶玉予知
            else if (oracleBallPrediction >= 0)
            {
                result[0] = oracleBallPrediction;
                result[1] = oracleBallPrediction;
                result[2] = oracleBallPrediction;
                oracleBallPrediction = -1;

                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n🔮 予知通りの未来...！ 🔮");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            else
            {
                // 通常の確率計算
                if (!greedRingEquipped)
                {
                    if (itemInventory["お守り"] > 0)
                    {
                        luckBonus += 3;
                    }
                    if (itemInventory["幸運のコイン"] > 0)
                    {
                        luckBonus += 8;
                        itemInventory["幸運のコイン"]--;
                    }

                    // 🆕 血塗られたお守り: 確率2倍
                    if (bloodAmuletEquipped)
                    {
                        luckBonus += 15;
                    }
                }

                if (freezeEffect || premiumEffect)
                {
                    result[0] = 2;
                    result[1] = 2;
                    result[2] = 2;
                }
                else
                {
                    int luckyBonus = (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped) ? 10 : 0;
                    int settingBonus = greedRingEquipped ? 0 : setting * 1;

                    if (greedRingEquipped)
                    {
                        for (int i = 0; i < 3; i++)
                        {
                            int rnd = rand.Next(100);
                            if (rnd < 2) result[i] = 2;
                            else if (rnd < 6) result[i] = 0;
                            else if (rnd < 10) result[i] = 1;
                            else if (rnd < 14) result[i] = 4;
                            else result[i] = rand.Next(5, symbols.Length);
                        }
                    }
                    else
                    {
                        for (int i = 0; i < 3; i++)
                        {
                            int rnd = rand.Next(100);
                            int threshold777 = 4 + luckyBonus + settingBonus + luckBonus;
                            int threshold0 = 12 + luckyBonus + settingBonus + luckBonus;
                            int threshold1 = 22 + luckyBonus + settingBonus + luckBonus;
                            int threshold4 = 35 + luckyBonus + settingBonus + luckBonus;

                            if (rnd < threshold777) result[i] = 2;
                            else if (rnd < threshold0) result[i] = 0;
                            else if (rnd < threshold1) result[i] = 1;
                            else if (rnd < threshold4) result[i] = 4;
                            else result[i] = rand.Next(5, symbols.Length);
                        }
                    }
                }
            }






            bool isReach = (result[0] == result[2] && result[0] != result[1]) && rand.Next(100) < 15 && !greedRingEquipped;

            if (isReach)
            {
                ReachEffect(result);
            }

            Console.Clear();

            if (greedRingEquipped)
            {
                Console.BackgroundColor = ConsoleColor.DarkRed;
                Console.ForegroundColor = ConsoleColor.Black;
            }

            DrawTitle();

            if (greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.BackgroundColor = ConsoleColor.Black;
                Console.WriteLine($"\n💀💀💀 強欲のオーラ 発動中 💀💀💀");
                Console.ResetColor();
            }

            if (godMode && godModeRemaining > 0 && !greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                Console.ResetColor();
            }

            if (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"\n☆☆☆ ラッキータイム！残り{luckyTimeRemaining}回 ☆☆☆");
                Console.ResetColor();
            }

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(result);
            Thread.Sleep(600);

            Console.WriteLine("\n");
            int winAmount = 0;
            int multiplier = 1;

            if (godMode && godModeRemaining > 0 && !greedRingEquipped)
                multiplier *= 2;

            // 🆕 死神の指輪: 勝利時×10倍
            if (deathRingEquipped)
                multiplier *= 10;

            bool isWin = false;

            if (result[0] == 2 && result[1] == 2 && result[2] == 2)
            {
                winAmount = bet * 10 * multiplier;
                isWin = true;

                if (greedRingEquipped)
                {
                    winAmount *= 5;
                    GreedRingMegaWinAnimation($"+{winAmount}G");
                }
                else
                {
                    JackpotGlitch();
                    MegaWinAnimation($"+{winAmount}G");
                }

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                bigWinCount++;
                total777Count++;
                totalLoses = 0;
                consecutiveLosses = 0;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;

                    // 🆕 5連勝カウント
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                if (deathRingEquipped)
                {
                    deathRing10Wins++;

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n💀 死神の指輪: {deathRing10Wins}回勝利");
                    Console.ResetColor();
                    Thread.Sleep(1000);
                }

                if (!unlockedEvents.Contains("777大当たり"))
                    unlockedEvents.Add("777大当たり");

                if (!greedRingEquipped)
                    UnlockSymbol();

                if (bet == 5000)
                    vip5000BetWin = true;
            }
            else if (result[0] == result[1] && result[1] == result[2])
            {
                winAmount = bet * 5 * multiplier;
                isWin = true;

                if (greedRingEquipped)
                {
                    winAmount *= 5;
                    GreedRingBigWinAnimation($"+{winAmount}G");
                }
                else
                {
                    BigWinAnimation($"+{winAmount}G");
                }

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                totalLoses = 0;
                consecutiveLosses = 0;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;

                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                if (deathRingEquipped)
                {
                    deathRing10Wins++;

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n💀 死神の指輪: {deathRing10Wins}回勝利");
                    Console.ResetColor();
                    Thread.Sleep(1000);
                }
            }
            else if (result[0] == result[1] || result[1] == result[2] || result[0] == result[2])
            {
                winAmount = bet * 2 * multiplier;
                isWin = true;

                if (greedRingEquipped)
                {
                    winAmount *= 5;
                    GreedRingSmallWinAnimation($"+{winAmount}G");
                }
                else
                {
                    SmallWinAnimation($"+{winAmount}G");
                }

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                totalLoses = 0;
                consecutiveLosses = 0;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;

                    // 🆕 追加
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                if (deathRingEquipped)
                {
                    deathRing10Wins++;

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n💀 死神の指輪: {deathRing10Wins}回勝利");
                    Console.ResetColor();
                    Thread.Sleep(1000);
                }
            }
            else
            {
                if (greedRingEquipped)
                {
                    GreedRingLoseAnimation();
                    greedRingLoseCount++;

                    if (money >= 500)
                    {
                        money -= 500;
                        totalLoseAmount += 500;
                    }
                    else
                    {
                        int shortage = 500 - money;
                        totalLoseAmount += money;
                        money = 0;
                        debt += shortage;
                        hasEverBorrowedMoney = true;

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n所持金不足...{shortage}Gが借金に追加された");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                    }
                }
                else
                {
                    totalLoseAmount += bet;
                    LoseAnimation();

                    // 🆕 血塗られたお守りの呪い処理
                    if (bloodAmuletEquipped)
                    {
                        bloodAmuletLoses++;

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血の呪い: {bloodAmuletLoses}/3回");
                        Console.ResetColor();
                        Thread.Sleep(1500);

                        if (bloodAmuletLoses >= 3)
                        {
                            BloodAmuletBadEnding();
                            return; // スピン処理を中断してメニューに戻る
                        }
                    }
                    if (deathRingEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Magenta;
                        Console.WriteLine("\n💀 死神の呪い: -1000G");
                        Console.ResetColor();
                        Thread.Sleep(1500);

                        if (money >= 1000)
                        {
                            money -= 1000;
                            totalLoseAmount += 1000;
                        }
                        else
                        {
                            // 所持金不足なら借金に
                            int shortage = 1000 - money;
                            totalLoseAmount += money;
                            money = 0;
                            debt += shortage;
                            hasEverBorrowedMoney = true;

                            Console.ForegroundColor = ConsoleColor.DarkRed;
                            Console.WriteLine($"\n所持金不足...{shortage}Gが借金に追加された");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                        }

                        deathRing10Wins++; // 使用回数カウント（ミッション用）
                    }
                }

                consecutiveWins = 0;
                totalLoses++;
                consecutiveLosses++;

            }
            if (devilContractActive && devilContractType == 1 && isWin)
            {
                contract1WinCount++;

                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine($"\n😈 契約勝利: {contract1WinCount}/10回");
                Console.ResetColor();

                if (contract1WinCount >= 10)
                {
                    contract1Complete = true;
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n★ 10回勝利達成！次の回転で... ★");
                    Console.ResetColor();
                }

                Thread.Sleep(1500);
            }

            if (consecutiveWins > maxConsecutiveWins)
                maxConsecutiveWins = consecutiveWins;

            if (money > maxMoney)
                maxMoney = money;

            if (godMode && godModeRemaining > 0 && !greedRingEquipped)
            {
                godModeRemaining--;
                if (godModeRemaining == 0)
                {
                    godMode = false;
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n[GOD MODE 終了...]");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }

            if (luckyTimeActive && luckyTimeRemaining > 0 && !greedRingEquipped)
            {
                luckyTimeRemaining--;
                if (luckyTimeRemaining == 0)
                {
                    luckyTimeActive = false;
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n[ラッキータイム 終了...]");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }

            if (winAmount > 0 && rand.Next(100) < 40 && !greedRingEquipped)
            {
                DoubleUpChallenge(ref winAmount);
            }
            // スピンごとの中毒度上昇
            if (addictionLevel < 100)
            {
                int addIncrease = 1;               // 基本+1
                if (bet >= 100) addIncrease++;     // 100Gベットで+1
                if (!isWin) addIncrease++;        // 負けで+1
                addictionLevel = Math.Min(100, addictionLevel + addIncrease);
            }
            CheckMissions();

            if (debt > 0 && winAmount > 0)
            {
                Thread.Sleep(500);
                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("借金を返済しますか？ [Y/N]");
                Console.ResetColor();
                var repay = Console.ReadKey(true);
                if (repay.Key == ConsoleKey.Y)
                {
                    int repayAmount = Math.Min(money, debt);
                    money -= repayAmount;
                    debt -= repayAmount;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"\n{repayAmount}G返済しました！");
                    Console.ResetColor();
                    if (debt == 0)
                    {
                        debtTurnsRemaining = 0;
                        Console.WriteLine("\n借金完済！黒服たちが去っていった...");
                        if (!unlockedEvents.Contains("借金完済"))
                            unlockedEvents.Add("借金完済");
                    }
                    Thread.Sleep(1500);
                }
            }
        }

        // ========== VIPルーム解放イベント ==========
        static void VIPRoomUnlockEvent()
        {
            Console.Clear();

            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Magenta : ConsoleColor.White;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
                Console.WriteLine("    ♦                           ♦");
                Console.WriteLine("    ♦    VIPルーム 解放！！！   ♦");
                Console.WriteLine("    ♦                           ♦");
                Console.WriteLine("    ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
                Console.ResetColor();
                Thread.Sleep(300);
            }

            Thread.Sleep(1000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    店員が近づいてきた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「お客様...所持金10000Gを突破されましたね」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「特別なお部屋へご案内いたします...」");
            Thread.Sleep(2000);

            Console.Clear();
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    重厚な扉が開かれる...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    そこには豪華絢爛な空間が広がっていた");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n    ★★★ VIPルームが利用可能になりました！ ★★★");
            Console.ResetColor();
            Console.WriteLine("\n    ・通常の3倍の配当");
            Console.WriteLine("    ・高額ベット可能（500G/1000G/5000G）");
            Console.WriteLine("    ・専属ディーラーが対応");

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n    ⚠ ただし...連敗には気をつけて... ⚠");
            Console.ResetColor();

            Thread.Sleep(4000);

            // 中毒度増加
            if (addictionLevel < 100)
            {
                addictionLevel += rand.Next(1, 3);
                if (addictionLevel > 100) addictionLevel = 100;
            }
        }


        // ========== VIPディーラー初対面 ==========
        static void VIPDealerFirstMeeting()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    美しい女性ディーラーが微笑んだ...");
            Thread.Sleep(2000);

            Console.WriteLine($"\n    「初めまして、{playerName}様」");
            Thread.Sleep(2000);

            Console.WriteLine($"\n    「私は{vipDealerName}」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「VIPルーム専属ディーラーです」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「ここでは...大きな幸運も...」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n    「...大きな不幸も訪れます」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n    「どうぞ...お楽しみください」");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("ミス・フォーチュン登場"))
                unlockedEvents.Add("ミス・フォーチュン登場");
        }

        // ========== VIPルーム入退室 ==========
        static void EnterVIPRoom()
        {
            if (!hasSeenVIPDealer)
            {
                VIPDealerFirstMeeting();
                hasSeenVIPDealer = true;
            }

            isInVIPRoom = true;
            vipTotalVisits++;
            vipConsecutiveLoses = 0;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ════════════════════════════════");
            Console.WriteLine("         VIPルームへようこそ");
            Console.WriteLine("    ════════════════════════════════");
            Console.ResetColor();
            Thread.Sleep(2000);
        }

        static void ExitVIPRoom()
        {
            isInVIPRoom = false;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    VIPルームを退室しました");
            Console.ResetColor();
            Thread.Sleep(1500);
        }

        // ========== VIPルームメインループ ==========
        static void VIPRoomLoop()
        {
            EnterVIPRoom();

            while (isInVIPRoom)
            {
                if (greedRingEquipped && debt >= 5000)
                {
                    GreedRingBadEnding();
                    return;
                }

                if (money <= 0 && debt > 0)
                {
                    DebtCollectionEvent();
                    return;
                }

                if (debt > 0 && debtTurnsRemaining > 0)
                {
                    debtTurnsRemaining--;
                    if (debtTurnsRemaining == 0)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\n借金の期限が切れた...");
                        Thread.Sleep(2000);
                        Console.ResetColor();
                        DebtCollectionEvent();
                        return;
                    }
                }

                if (vipConsecutiveLoses >= 3 && !undergroundUnlocked)
                {
                    VIPThreeLossEvent();
                    vipConsecutiveLoses = 0;
                }

                if (rand.Next(100) < 5)
                {
                    VIPRandomEvent();
                }

                Console.Clear();

                Console.BackgroundColor = ConsoleColor.DarkMagenta;
                Console.ForegroundColor = ConsoleColor.White;

                DrawVIPTitle();

                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n♦♦♦ VIPルーム - {vipDealerName}が対応中 ♦♦♦");
                Console.ResetColor();

                if (godMode && godModeRemaining > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                    Console.ResetColor();
                }

                if (luckyTimeActive && luckyTimeRemaining > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"\n☆☆☆ ラッキータイム！残り{luckyTimeRemaining}回 ☆☆☆");
                    Console.ResetColor();
                }

                Console.WriteLine($"\nプレイヤー: {playerName}");
                Console.WriteLine($"所持金: {money}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    if (debtTurnsRemaining > 0)
                    {
                        Console.WriteLine($"返済期限: あと{debtTurnsRemaining}回転");
                    }
                    Console.ResetColor();
                }

                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"\nVIP統計:");
                Console.WriteLine($"  訪問回数: {vipTotalVisits}回");
                Console.WriteLine($"  総回転数: {vipTotalSpins}回");
                Console.WriteLine($"  勝利回数: {vipTotalWins}回");
                if (vipConsecutiveLoses > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  連敗中: {vipConsecutiveLoses}回");
                }
                Console.ResetColor();

                ShowUncompletedMissions();

                Console.WriteLine("\n┌────────────────────────────┐");
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("│  [1] 500G でプレイ        │");
                Console.WriteLine("│  [2] 1000G でプレイ       │");
                Console.WriteLine("│  [3] 5000G でプレイ       │");
                Console.ResetColor();
                if (money < 500)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("│  [4] 借金する (500G)      │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [M] ミッション確認       │");
                Console.WriteLine("│  [S] ショップ             │");
                if (abandonedCasinoUnlocked)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("│  [A] 廃娯楽施設           │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [E] 装備管理             │");
                Console.WriteLine("│  [X] VIP退室              │");
                Console.WriteLine("│  [0] ゲーム終了           │");
                Console.WriteLine("└────────────────────────────┘");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);
                int bet = 0;

                if (key.KeyChar == 's' || key.KeyChar == 'S')
                {
                    ShopMenu();
                    continue;
                }

                if ((key.KeyChar == 'a' || key.KeyChar == 'A') && abandonedCasinoUnlocked)
                {
                    EnterAbandonedCasino();
                    continue;
                }

                if (key.KeyChar == 'e' || key.KeyChar == 'E')
                {
                    EquipmentMenu();
                    continue;
                }

                if (key.KeyChar == 'm' || key.KeyChar == 'M')
                {
                    ShowAllMissions();
                    continue;
                }

                if (key.KeyChar == 'x' || key.KeyChar == 'X')
                {
                    ExitVIPRoom();
                    break;
                }

                if (key.KeyChar == '0')
                {
                    isInVIPRoom = false;
                    return;
                }
                else if (key.KeyChar == '1')
                {
                    bet = 500;
                }
                else if (key.KeyChar == '2')
                {
                    bet = 1000;
                }
                else if (key.KeyChar == '3')
                {
                    bet = 5000;
                }
                else if (key.KeyChar == '4' && money < 500)
                {
                    BlackSuitArrival();
                    money += 500;
                    debt += 500;
                    hasEverBorrowedMoney = true;
                    debtTurnsRemaining = 20;
                    if (!unlockedEvents.Contains("黒服登場"))
                        unlockedEvents.Add("黒服登場");
                    continue;
                }
                else
                {
                    Console.WriteLine("\n正しい選択をしてください");
                    Thread.Sleep(1000);
                    continue;
                }

                if (bet > money)
                {
                    Console.WriteLine("\n所持金不足！");
                    Thread.Sleep(1500);
                    continue;
                }

                VIPSpin(bet);

                Console.WriteLine("\n\n何かキーを押して続ける...");
                Console.ReadKey(true);
            }
        }

        // ========== VIPスピン処理 ==========
        static void VIPSpin(int bet)
        {
            DateTime spinStartTime = DateTime.Now;

            money -= bet;
            totalSpins++;
            vipTotalSpins++;

            Console.Clear();

            Console.BackgroundColor = ConsoleColor.DarkMagenta;
            Console.ForegroundColor = ConsoleColor.White;
            DrawVIPTitle();
            Console.BackgroundColor = ConsoleColor.Black;

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine($"\n♦♦♦ VIPルーム - ベット: {bet}G ♦♦♦");
            Console.ResetColor();

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(new int[] { 0, 1, 2 });
            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine($"        ▼ {vipDealerName}がレバーを引く ▼");
            Console.ResetColor();
            Thread.Sleep(1000);

            for (int t = 0; t < 20; t++)
            {
                int[] reels = { rand.Next(symbols.Length), rand.Next(symbols.Length), rand.Next(symbols.Length) };
                Console.Clear();

                Console.BackgroundColor = ConsoleColor.DarkMagenta;
                Console.ForegroundColor = ConsoleColor.White;
                DrawVIPTitle();
                Console.BackgroundColor = ConsoleColor.Black;

                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n♦♦♦ VIPルーム - ベット: {bet}G ♦♦♦");
                Console.ResetColor();

                Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    Console.ResetColor();
                }
                Console.WriteLine("\n");

                Console.ForegroundColor = t % 2 == 0 ? ConsoleColor.Magenta : ConsoleColor.White;
                DrawReels(reels);
                Console.ResetColor();

                int delay = t < 10 ? 50 : 50 + (t - 10) * 30;
                Thread.Sleep(delay);
            }

            int[] result = new int[3];
            int luckBonus = 0;

            if (itemInventory["お守り"] > 0)
                luckBonus += 3;
            if (itemInventory["幸運のコイン"] > 0)
            {
                luckBonus += 8;
                itemInventory["幸運のコイン"]--;
            }
            // 🆕 水晶玉予知
            if (oracleBallPrediction >= 0)
            {
                result[0] = oracleBallPrediction;
                result[1] = oracleBallPrediction;
                result[2] = oracleBallPrediction;
                oracleBallPrediction = -1;

                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n🔮 予知通りの未来...！ 🔮");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            else
            {


                int luckyBonus = luckyTimeActive && luckyTimeRemaining > 0 ? 10 : 0;
                int settingBonus = setting * 1;
                int vipBonus = 8;

                for (int i = 0; i < 3; i++)
                {
                    int rnd = rand.Next(100);
                    int threshold777 = 6 + luckyBonus + settingBonus + luckBonus + vipBonus;
                    int threshold0 = 18 + luckyBonus + settingBonus + luckBonus + vipBonus;
                    int threshold1 = 30 + luckyBonus + settingBonus + luckBonus + vipBonus;
                    int threshold4 = 45 + luckyBonus + settingBonus + luckBonus + vipBonus;

                    if (rnd < threshold777) result[i] = 2;
                    else if (rnd < threshold0) result[i] = 0;
                    else if (rnd < threshold1) result[i] = 1;
                    else if (rnd < threshold4) result[i] = 4;
                    else result[i] = rand.Next(5, symbols.Length);
                }
            }

            bool isReach = (result[0] == result[2] && result[0] != result[1]) && rand.Next(100) < 20;
            if (isReach)
            {
                VIPReachEffect(result);
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkMagenta;
            Console.ForegroundColor = ConsoleColor.White;
            DrawVIPTitle();
            Console.BackgroundColor = ConsoleColor.Black;

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine($"\n♦♦♦ VIPルーム - 結果 ♦♦♦");
            Console.ResetColor();

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(result);
            Thread.Sleep(800);

            Console.WriteLine("\n");
            int winAmount = 0;
            int multiplier = 3;

            if (godMode && godModeRemaining > 0)
                multiplier *= 2;
            if (deathRingEquipped)
                multiplier *= 10;

            bool isWin = false;

            if (result[0] == 2 && result[1] == 2 && result[2] == 2)
            {
                winAmount = bet * 10 * multiplier;
                isWin = true;
                vip777Count++;

                VIPMegaWinAnimation($"+{winAmount}G");

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                bigWinCount++;
                total777Count++;
                vipTotalWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                vipConsecutiveLoses = 0;
                totalLoses = 0;

                if (!unlockedEvents.Contains("VIP777"))
                    unlockedEvents.Add("VIP777");

                UnlockSymbol();
            }
            else if (result[0] == result[1] && result[1] == result[2])
            {
                winAmount = bet * 5 * multiplier;
                isWin = true;

                VIPBigWinAnimation($"+{winAmount}G");

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                vipTotalWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                vipConsecutiveLoses = 0;
                totalLoses = 0;

                if (bet == 5000)
                    vip5000BetWin = true;
            }
            else if (result[0] == result[1] || result[1] == result[2] || result[0] == result[2])
            {
                winAmount = bet * 2 * multiplier;
                isWin = true;

                VIPSmallWinAnimation($"+{winAmount}G");

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                vipTotalWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                vipConsecutiveLoses = 0;
                totalLoses = 0;
            }
            else
            {
                totalLoseAmount += bet;
                VIPLoseAnimation();
                consecutiveWins = 0;
                totalLoses++;
                vipConsecutiveLoses++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses++;

                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine($"\n🩸 血の呪い: {bloodAmuletLoses}/3回");
                    Console.ResetColor();
                    Thread.Sleep(1500);

                    if (bloodAmuletLoses >= 3)
                    {
                        BloodAmuletBadEnding();
                        return;
                    }
                }
                if (deathRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n💀 死神の呪い: -1000G");
                    Console.ResetColor();
                    Thread.Sleep(1500);

                    if (money >= 1000)
                    {
                        money -= 1000;
                        totalLoseAmount += 1000;
                    }
                    else
                    {
                        int shortage = 1000 - money;
                        totalLoseAmount += money;
                        money = 0;
                        debt += shortage;
                        hasEverBorrowedMoney = true;

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n所持金不足...{shortage}Gが借金に追加された");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                    }
                }
            }
            if (devilContractActive && devilContractType == 1 && isWin)
            {
                contract1WinCount++;

                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine($"\n😈 契約勝利: {contract1WinCount}/10回");
                Console.ResetColor();

                if (contract1WinCount >= 10)
                {
                    contract1Complete = true;
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n★ 10回勝利達成！次の回転で... ★");
                    Console.ResetColor();
                }

                Thread.Sleep(1500);
            }

            if (consecutiveWins > maxConsecutiveWins)
                maxConsecutiveWins = consecutiveWins;

            if (money > maxMoney)
                maxMoney = money;

            if (godMode && godModeRemaining > 0)
            {
                godModeRemaining--;
                if (godModeRemaining == 0)
                {
                    godMode = false;
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n[GOD MODE 終了...]");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }

            if (luckyTimeActive && luckyTimeRemaining > 0)
            {
                luckyTimeRemaining--;
                if (luckyTimeRemaining == 0)
                {
                    luckyTimeActive = false;
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n[ラッキータイム 終了...]");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }

            if (winAmount > 0 && rand.Next(100) < 60)
            {
                VIPDoubleUpChallenge(ref winAmount);
            }
            // スピンごとの中毒度上昇（VIPは多め）
            if (addictionLevel < 100)
            {
                int addIncrease = 2;               // VIP基本+2
                if (bet >= 1000) addIncrease++;   // 高額ベットで+1
                if (!isWin) addIncrease++;        // 負けで+1
                addictionLevel = Math.Min(100, addictionLevel + addIncrease);
            }

            CheckMissions();

            if (debt > 0 && winAmount > 0)
            {
                Thread.Sleep(500);
                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("借金を返済しますか？ [Y/N]");
                Console.ResetColor();
                var repay = Console.ReadKey(true);
                if (repay.Key == ConsoleKey.Y)
                {
                    int repayAmount = Math.Min(money, debt);
                    money -= repayAmount;
                    debt -= repayAmount;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"\n{repayAmount}G返済しました！");
                    Console.ResetColor();
                    if (debt == 0)
                    {
                        debtTurnsRemaining = 0;
                        Console.WriteLine("\n借金完済！黒服たちが去っていった...");
                        if (!unlockedEvents.Contains("借金完済"))
                            unlockedEvents.Add("借金完済");
                    }
                    Thread.Sleep(1500);
                }
            }
        }


        // ========== VIP専用演出 ==========
        static void DrawVIPTitle()
        {
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("╔═══════════════════════════════════╗");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("║      ♦♦ VIP ROOM ♦♦             ║");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("╚═══════════════════════════════════╝");
            Console.ResetColor();
        }

        static void VIPMegaWinAnimation(string amount)
        {
            for (int i = 0; i < 6; i++)
            {
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Magenta : ConsoleColor.White;
                Console.WriteLine("  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
                Console.WriteLine("  ♦                                    ♦");
                Console.WriteLine($"  ♦    VIP 777大当たり！×30倍！     ♦");
                Console.WriteLine($"  ♦         {amount.PadLeft(10)}           ♦");
                Console.WriteLine("  ♦                                    ♦");
                Console.WriteLine("  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
                Thread.Sleep(250);
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                for (int j = 0; j < 6; j++) Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
            Console.WriteLine("  ♦                                    ♦");
            Console.WriteLine($"  ♦    VIP 777大当たり！×30倍！     ♦");
            Console.WriteLine($"  ♦         {amount.PadLeft(10)}           ♦");
            Console.WriteLine("  ♦                                    ♦");
            Console.WriteLine("  ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦");
            Console.ResetColor();
        }

        static void VIPBigWinAnimation(string amount)
        {
            for (int i = 0; i < 4; i++)
            {
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"     ♦♦ VIP大当たり×15倍！{amount} ♦♦");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine($"     ♦♦ VIP大当たり×15倍！{amount} ♦♦");
            Console.ResetColor();
        }

        static void VIPSmallWinAnimation(string amount)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"        ♦ VIP当たり×6倍！{amount} ♦");
            Console.ResetColor();
        }

        static void VIPLoseAnimation()
        {
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("           × ハズレ… ×");
            Console.ResetColor();
        }

        static void VIPReachEffect(int[] result)
        {
            Console.Clear();
            DrawVIPTitle();
            Console.WriteLine("\n");

            int[] tempResult = new int[] { result[0], result[1], result[0] };
            DrawReels(tempResult);

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n        ♦♦♦ VIPリーチ！！ ♦♦♦");
            Console.WriteLine($"        {vipDealerName}が微笑んだ...");
            Console.ResetColor();
            Thread.Sleep(1500);

            for (int i = 0; i < 12; i++)
            {
                tempResult[1] = rand.Next(symbols.Length);
                Console.Clear();
                DrawVIPTitle();
                Console.WriteLine("\n");
                DrawReels(tempResult);
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("\n        ♦♦♦ VIPリーチ！！ ♦♦♦");
                Console.WriteLine($"        {vipDealerName}が微笑んだ...");
                Console.ResetColor();
                Thread.Sleep(120 + i * 40);
            }
        }

        static void VIPDoubleUpChallenge(ref int winAmount)
        {
            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine($"  {vipDealerName}のダブルアップ！");
            Console.WriteLine($"  現在の獲得金: {winAmount}G");
            Console.WriteLine("  ━━━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("  成功で2倍、失敗で半分");
            Console.WriteLine("  挑戦しますか？ [Y/N]");
            Console.ResetColor();

            var choice = Console.ReadKey(true);
            if (choice.Key == ConsoleKey.Y)
            {
                Console.WriteLine($"\n\n  {vipDealerName}がカードを裏返す...");
                Thread.Sleep(1500);

                for (int i = 0; i < 5; i++)
                {
                    Console.Write(i % 2 == 0 ? "\r  ♦ ハート " : "\r  ♠ スペード ");
                    Thread.Sleep(300);
                }

                bool success = rand.Next(2) == 0;

                Thread.Sleep(500);
                Console.WriteLine();

                if (success)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n  ★★★ 成功！2倍獲得！ ★★★");
                    int oldAmount = winAmount;
                    winAmount *= 2;
                    money += winAmount - oldAmount;
                    Console.WriteLine($"  獲得金: {winAmount}G");
                    Console.ResetColor();
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n  × 失敗...半分に減った ×");
                    int oldAmount = winAmount;
                    winAmount /= 2;
                    money -= (oldAmount - winAmount);
                    Console.WriteLine($"  獲得金: {winAmount}G");
                    Console.ResetColor();
                }
                Thread.Sleep(2000);
            }
        }

        // ========== VIPイベント ==========
        static void VIPThreeLossEvent()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         VIP 3連敗ペナルティ");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine($"\n\n    {vipDealerName}が近づいてきた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「お客様...運が悪いようですね」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...もっと刺激的な場所をご存知ですか？」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    彼女が手渡したのは黒い招待状だった");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n    『地下カジノへようこそ』");
            Console.ResetColor();
            Thread.Sleep(2000);

            undergroundUnlocked = true;

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    ★★★ 地下カジノが解放されました ★★★");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("地下への招待"))
                unlockedEvents.Add("地下への招待");
        }

        static void VIPRandomEvent()
        {
            int eventType = rand.Next(5);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");

            switch (eventType)
            {
                case 0:
                    Console.WriteLine($"    {vipDealerName}: 「今日の運勢は...まずまずですね」");
                    break;
                case 1:
                    Console.WriteLine("    天井から豪華なシャンデリアが輝いている...");
                    break;
                case 2:
                    Console.WriteLine("    他のVIP客が大勝ちして歓声を上げている");
                    break;
                case 3:
                    Console.WriteLine($"    {vipDealerName}が意味深に微笑んだ...");
                    break;
                case 4:
                    Console.WriteLine("    監視カメラが静かにあなたを見ている...");
                    if (!unlockedEvents.Contains("監視カメラ"))
                        unlockedEvents.Add("監視カメラ");
                    break;
            }
            Console.ResetColor();
            Thread.Sleep(2500);
        }

        // ========== 地下カジノ（スタブ） ==========
        static void UndergroundUnlockByDebt()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         絶望の淵");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n    黒服の一人が近づいてきた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「おい...借金が膨れ上がってるな」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...一か八かの勝負に出るか？」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    黒い招待状を手渡された");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Black;
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n    『奈落の底へようこそ』");
            Console.ResetColor();
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    ★★★ 地下カジノが解放されました ★★★");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("絶望からの招待"))
                unlockedEvents.Add("絶望からの招待");
        }

        static void UndergroundDealerFirstMeeting()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    暗闇の中...仮面を被った男が現れた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「ようこそ...奈落へ...」");
            Thread.Sleep(2000);

            Console.WriteLine($"\n    「私は{undergroundDealerName}」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「ここは...最後の賭場だ...」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n    「勝てば天国...負ければ...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...地獄だ」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n    仮面の奥から不気味な笑い声が聞こえた...");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("ダークロード登場"))
                unlockedEvents.Add("ダークロード登場");
        }
        static void EnterUnderground()
        {
            if (!hasSeenUndergroundDealer)
            {
                UndergroundDealerFirstMeeting();
                hasSeenUndergroundDealer = true;
            }

            isInUnderground = true;
            undergroundVisits++;
            undergroundConsecutiveLoses = 0;

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ════════════════════════════════");
            Console.WriteLine("         奈落へ...降りていく...");
            Console.WriteLine("    ════════════════════════════════");
            Thread.Sleep(2000);

            Console.WriteLine("\n    階段を降りるたびに空気が重くなる...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    血の匂いがする...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("          地下カジノ - 奈落");
            Console.WriteLine("    ================================");
            Console.ResetColor();
            Thread.Sleep(2000);
        }

        static void ExitUnderground()
        {
            isInUnderground = false;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    地下カジノを後にした...");
            Console.WriteLine("\n    生きて戻れた...それだけで奇跡だ...");
            Console.ResetColor();
            Thread.Sleep(2000);
        }

        static void UndergroundLoop()
        {
            EnterUnderground();

            while (isInUnderground)
            {
                // 強欲の指輪チェック
                if (greedRingEquipped && debt >= 5000)
                {
                    GreedRingBadEnding();
                    return;
                }

                if (money <= 0 && debt > 0)
                {
                    DebtCollectionEvent();
                    return;
                }

                // 借金期限チェック
                if (debt > 0 && debtTurnsRemaining > 0)
                {
                    debtTurnsRemaining--;
                    if (debtTurnsRemaining == 0)
                    {
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\n借金の期限が切れた...");
                        Thread.Sleep(2000);
                        Console.ResetColor();
                        DebtCollectionEvent();
                        return;
                    }
                }

                // 地下5連敗で呪いモード（既存）
                if (undergroundConsecutiveLoses >= 5)
                {
                    UndergroundCursedEvent();
                    undergroundConsecutiveLoses = 0;
                }

                // ↓ 下に追加！勝利後に呪い解除
                if (undergroundCursedMode && undergroundWins > 0 && rand.Next(3) == 0)
                {
                    undergroundCursedMode = false;
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n\n\n    呪いが...解けた...");
                    Console.WriteLine($"\n    {undergroundDealerName}が舌打ちをした...");
                    Console.ResetColor();
                    Thread.Sleep(2500);
                }

                // ランダムイベント
                if (rand.Next(100) < 10)
                {
                    UndergroundRandomEvent();
                }

                Console.Clear();

                // 地下専用背景色
                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.DarkRed;

                DrawUndergroundTitle();

                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n🔥🔥🔥 地下カジノ - {undergroundDealerName}が見つめている 🔥🔥🔥");
                Console.ResetColor();

                if (undergroundCursedMode)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("\n💀 呪いモード発動中 💀");
                    Console.ResetColor();
                }

                if (godMode && godModeRemaining > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n★★★ GOD MODE 発動中！残り{godModeRemaining}回 ★★★");
                    Console.ResetColor();
                }

                Console.WriteLine($"\nプレイヤー: {playerName}");
                Console.WriteLine($"所持金: {money}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    if (debtTurnsRemaining > 0)
                    {
                        Console.WriteLine($"返済期限: あと{debtTurnsRemaining}回転");
                    }
                    Console.ResetColor();
                }

                Console.ForegroundColor = ConsoleColor.DarkYellow;
                Console.WriteLine($"\n地下統計:");
                Console.WriteLine($"  訪問回数: {undergroundVisits}回");
                Console.WriteLine($"  総回転数: {undergroundTotalSpins}回");
                Console.WriteLine($"  勝利回数: {undergroundWins}回");
                if (undergroundConsecutiveLoses > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  連敗中: {undergroundConsecutiveLoses}回");
                }
                Console.ResetColor();

                ShowUncompletedMissions();

                Console.WriteLine("\n┌────────────────────────────┐");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("│  [1] 500G でプレイ        │");
                Console.WriteLine("│  [2] 1000G でプレイ       │");
                Console.WriteLine("│  [3] 5000G でプレイ       │");
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("│  [4] 全財産を賭ける       │");
                Console.ResetColor();
                if (money < 500)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("│  [5] 借金する (500G)      │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [M] ミッション確認       │");
                Console.WriteLine("│  [S] ショップ             │");
                if (abandonedCasinoUnlocked)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("│  [A] 廃娯楽施設           │");
                    Console.ResetColor();
                }
                Console.WriteLine("│  [X] 地下退出             │");
                Console.WriteLine("│  [0] ゲーム終了           │");
                Console.WriteLine("└────────────────────────────┘");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);
                int bet = 0;
                bool isAllIn = false;

                if (key.KeyChar == 's' || key.KeyChar == 'S')
                {
                    ShopMenu();
                    continue;
                }

                if ((key.KeyChar == 'a' || key.KeyChar == 'A') && abandonedCasinoUnlocked)
                {
                    EnterAbandonedCasino();
                    continue;
                }

                if (key.KeyChar == 'm' || key.KeyChar == 'M')
                {
                    ShowAllMissions();
                    continue;
                }

                if (key.KeyChar == 'x' || key.KeyChar == 'X')
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n\n本当に地上へ戻りますか？ [Y/N]");
                    Console.ResetColor();
                    var confirm = Console.ReadKey(true);
                    if (confirm.Key == ConsoleKey.Y)
                    {
                        ExitUnderground();
                        break;
                    }
                    continue;
                }

                if (key.KeyChar == '0')
                {
                    isInUnderground = false;
                    return;
                }
                else if (key.KeyChar == '1')
                {
                    bet = 500;
                }
                else if (key.KeyChar == '2')
                {
                    bet = 1000;
                }
                else if (key.KeyChar == '3')
                {
                    bet = 5000;
                }
                else if (key.KeyChar == '4')
                {
                    if (money < 100)
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\n所持金が少なすぎる...");
                        Console.ResetColor();
                        Thread.Sleep(1500);
                        continue;
                    }

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n\n⚠⚠⚠ 警告 ⚠⚠⚠\n");
                    Console.WriteLine("全財産を賭けますか？\n");
                    Console.WriteLine($"ベット額: {money}G");
                    Console.WriteLine("\n成功: 10倍〜100倍");
                    Console.WriteLine("失敗: 全てを失う");
                    Console.WriteLine("\n本当に賭けますか？ [Y/N]");
                    Console.ResetColor();

                    var confirm = Console.ReadKey(true);
                    if (confirm.Key != ConsoleKey.Y)
                        continue;

                    bet = money;
                    isAllIn = true;
                }
                else if (key.KeyChar == '5' && money < 500)
                {
                    BlackSuitArrival();
                    money += 500;
                    debt += 500;
                    hasEverBorrowedMoney = true;
                    debtTurnsRemaining = 20;
                    if (!unlockedEvents.Contains("黒服登場"))
                        unlockedEvents.Add("黒服登場");
                    continue;
                }
                else
                {
                    Console.WriteLine("\n正しい選択をしてください");
                    Thread.Sleep(1000);
                    continue;
                }

                if (bet > money)
                {
                    Console.WriteLine("\n所持金不足！");
                    Thread.Sleep(1500);
                    continue;
                }

                UndergroundSpin(bet, isAllIn);

                Console.WriteLine("\n\n何かキーを押して続ける...");
                Console.ReadKey(true);
            }
        }

        static void UndergroundSpin(int bet, bool isAllIn)
        {
            DateTime spinStartTime = DateTime.Now;

            money -= bet;
            totalSpins++;
            undergroundTotalSpins++;

            Console.Clear();

            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            DrawUndergroundTitle();

            Console.ForegroundColor = ConsoleColor.Red;
            if (isAllIn)
                Console.WriteLine($"\n🔥🔥🔥 全財産ベット: {bet}G 🔥🔥🔥");
            else
                Console.WriteLine($"\n🔥🔥🔥 地下カジノ - ベット: {bet}G 🔥🔥🔥");
            Console.ResetColor();

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(new int[] { 0, 1, 2 });
            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine($"        ▼ {undergroundDealerName}が不気味に笑う ▼");
            Console.ResetColor();
            Thread.Sleep(1200);

            // 血の演出
            if (rand.Next(100) < 30)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n        💀 血が滴る... 💀");
                Console.ResetColor();
                Thread.Sleep(800);
            }

            // リール回転（遅め＆不気味）
            for (int t = 0; t < 25; t++)
            {
                int[] reels = { rand.Next(symbols.Length), rand.Next(symbols.Length), rand.Next(symbols.Length) };
                Console.Clear();

                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.DarkRed;
                DrawUndergroundTitle();

                Console.ForegroundColor = ConsoleColor.Red;
                if (isAllIn)
                    Console.WriteLine($"\n🔥🔥🔥 全財産ベット: {bet}G 🔥🔥🔥");
                else
                    Console.WriteLine($"\n🔥🔥🔥 地下カジノ - ベット: {bet}G 🔥🔥🔥");
                Console.ResetColor();

                Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
                if (debt > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"借金: {debt}G");
                    Console.ResetColor();
                }
                Console.WriteLine("\n");

                // 血のエフェクト
                if (t % 3 == 0)
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                }

                DrawReels(reels);
                Console.ResetColor();

                int delay = t < 15 ? 70 : 70 + (t - 15) * 25;
                Thread.Sleep(delay);
            }

            // 結果決定（超低確率）
            int[] result = new int[3];

            // 地下カジノは当たり確率激減
            int baseChance = isAllIn ? 15 : 10; // 全財産は少し優遇

            if (undergroundCursedMode)
                baseChance /= 2; // 呪いモードで更に半減

            for (int i = 0; i < 3; i++)
            {
                int rnd = rand.Next(100);
                if (rnd < baseChance / 3) result[i] = 2;      // 777: 約3%
                else if (rnd < baseChance) result[i] = 0;     // 他当たり: 約7%
                else result[i] = rand.Next(5, symbols.Length); // ハズレ: 約90%
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            DrawUndergroundTitle();

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"\n🔥🔥🔥 地下カジノ - 結果 🔥🔥🔥");
            Console.ResetColor();

            Console.WriteLine($"\n所持金: {money}G  │  BET: {bet}G");
            if (debt > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"借金: {debt}G");
                Console.ResetColor();
            }
            Console.WriteLine("\n");
            DrawReels(result);
            Thread.Sleep(1000);

            Console.WriteLine("\n");
            int winAmount = 0;

            // 配当倍率（ランダム）
            int[] multipliers = { 10, 20, 50, 100 };
            int multiplier = multipliers[rand.Next(multipliers.Length)];

            if (godMode && godModeRemaining > 0)
                multiplier *= 2;
            if (deathRingEquipped)
                multiplier *= 10;

            bool isWin = false;

            if (result[0] == 2 && result[1] == 2 && result[2] == 2)
            {
                winAmount = bet * multiplier;
                isWin = true;

                UndergroundMegaWinAnimation($"+{winAmount}G", multiplier);

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                undergroundWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                undergroundConsecutiveLoses = 0;
                total777Count++;

                if (isAllIn)
                {
                    undergroundAllInWin = true;
                    if (!unlockedEvents.Contains("地下全財産勝利"))
                        unlockedEvents.Add("地下全財産勝利");
                }

                if (!unlockedEvents.Contains("地下777"))
                    unlockedEvents.Add("地下777");

                UnlockSymbol();
            }
            else if (result[0] == result[1] && result[1] == result[2])
            {
                winAmount = bet * (multiplier / 2);
                isWin = true;

                UndergroundBigWinAnimation($"+{winAmount}G", multiplier / 2);

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                undergroundWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                undergroundConsecutiveLoses = 0;

                if (isAllIn)
                {
                    undergroundAllInWin = true;
                    if (!unlockedEvents.Contains("地下全財産勝利"))
                        unlockedEvents.Add("地下全財産勝利");
                }
                if (deathRingEquipped)
                {
                    deathRing10Wins++;

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n💀 死神の指輪: {deathRing10Wins}回勝利");
                    Console.ResetColor();
                    Thread.Sleep(1000);
                }
            }
            else if (result[0] == result[1] || result[1] == result[2] || result[0] == result[2])
            {
                winAmount = bet * (multiplier / 5);
                isWin = true;

                UndergroundSmallWinAnimation($"+{winAmount}G");

                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                undergroundWins++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses = 0;
                    if (consecutiveWins >= 5)
                    {
                        bloodAmulet5Wins = Math.Max(bloodAmulet5Wins, consecutiveWins);
                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n🩸 血塗られたお守り: {consecutiveWins}連勝！");
                        Console.ResetColor();
                        Thread.Sleep(1000);
                    }
                }
                undergroundConsecutiveLoses = 0;

                if (deathRingEquipped)
                {
                    deathRing10Wins++;

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine($"\n💀 死神の指輪: {deathRing10Wins}回勝利");
                    Console.ResetColor();
                    Thread.Sleep(1000);
                }
            }
            else
            {
                totalLoseAmount += bet;
                UndergroundLoseAnimation(isAllIn);
                consecutiveWins = 0;
                totalLoses++;
                undergroundConsecutiveLoses++;

                if (bloodAmuletEquipped)
                {
                    bloodAmuletLoses++;

                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine($"\n🩸 血の呪い: {bloodAmuletLoses}/3回");
                    Console.ResetColor();
                    Thread.Sleep(1500);

                    if (bloodAmuletLoses >= 3)
                    {
                        BloodAmuletBadEnding();
                        return;
                    }
                }

                if (isAllIn)
                {
                    // 全財産を失った
                    UndergroundAllInLoseEvent();
                }
                if (deathRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n💀 死神の呪い: -1000G");
                    Console.ResetColor();
                    Thread.Sleep(1500);

                    if (money >= 1000)
                    {
                        money -= 1000;
                        totalLoseAmount += 1000;
                    }
                    else
                    {
                        // 所持金不足なら借金に
                        int shortage = 1000 - money;
                        totalLoseAmount += money;
                        money = 0;
                        debt += shortage;
                        hasEverBorrowedMoney = true;

                        Console.ForegroundColor = ConsoleColor.DarkRed;
                        Console.WriteLine($"\n所持金不足...{shortage}Gが借金に追加された");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                    }
                }
            }
            if (devilContractActive && devilContractType == 1 && isWin)
            {
                contract1WinCount++;

                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine($"\n😈 契約勝利: {contract1WinCount}/10回");
                Console.ResetColor();

                if (contract1WinCount >= 10)
                {
                    contract1Complete = true;
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n★ 10回勝利達成！次の回転で... ★");
                    Console.ResetColor();
                }

                Thread.Sleep(1500);
            }

            if (consecutiveWins > maxConsecutiveWins)
                maxConsecutiveWins = consecutiveWins;

            if (money > maxMoney)
                maxMoney = money;

            if (godMode && godModeRemaining > 0)
            {
                godModeRemaining--;
                if (godModeRemaining == 0)
                {
                    godMode = false;
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("\n[GOD MODE 終了...]");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                }
            }

            // スピンごとの中毒度上昇（地下は最多）
            if (addictionLevel < 100)
            {
                int addIncrease = 3;               // 地下基本+3
                if (isAllIn) addIncrease += 2;    // 全財産ベットで+2
                if (!isWin) addIncrease++;        // 負けで+1
                addictionLevel = Math.Min(100, addictionLevel + addIncrease);
            }

            CheckMissions();
            if (debt > 0 && winAmount > 0)
            {
                Thread.Sleep(500);
                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("借金を返済しますか？ [Y/N]");
                Console.ResetColor();
                var repay = Console.ReadKey(true);
                if (repay.Key == ConsoleKey.Y)
                {
                    int repayAmount = Math.Min(money, debt);
                    money -= repayAmount;
                    debt -= repayAmount;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"\n{repayAmount}G返済しました！");
                    Console.ResetColor();
                    if (debt == 0)
                    {
                        debtTurnsRemaining = 0;
                        Console.WriteLine("\n借金完済！黒服たちが去っていった...");
                        if (!unlockedEvents.Contains("借金完済"))
                            unlockedEvents.Add("借金完済");
                    }
                    Thread.Sleep(1500);
                }
            }
        }


        static void DrawUndergroundTitle()
        {
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("╔═══════════════════════════════════╗");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("║      🔥🔥 地下カジノ 🔥🔥      ║");
            Console.WriteLine("║           - 奈落 -                ║");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("╚═══════════════════════════════════╝");
            Console.ResetColor();
        }

        static void UndergroundMegaWinAnimation(string amount, int multiplier)
        {
            for (int i = 0; i < 7; i++)
            {
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Red : ConsoleColor.DarkRed;
                Console.WriteLine("  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥");
                Console.WriteLine("  🔥                                    🔥");
                Console.WriteLine($"  🔥   地下777揃い！×{multiplier}倍！！！   🔥");
                Console.WriteLine($"  🔥         {amount.PadLeft(12)}         🔥");
                Console.WriteLine("  🔥                                    🔥");
                Console.WriteLine("  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥");
                Thread.Sleep(250);
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                for (int j = 0; j < 6; j++) Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥");
            Console.WriteLine("  🔥                                    🔥");
            Console.WriteLine($"  🔥   地下777揃い！×{multiplier}倍！！！   🔥");
            Console.WriteLine($"  🔥         {amount.PadLeft(12)}         🔥");
            Console.WriteLine("  🔥                                    🔥");
            Console.WriteLine("  🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥");
            Console.ResetColor();
        }

        static void UndergroundBigWinAnimation(string amount, int multiplier)
        {
            for (int i = 0; i < 5; i++)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"     🔥🔥 地下大当たり×{multiplier}倍！{amount} 🔥🔥");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"     🔥🔥 地下大当たり×{multiplier}倍！{amount} 🔥🔥");
            Console.ResetColor();
        }

        static void UndergroundSmallWinAnimation(string amount)
        {
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"        🔥 地下当たり！{amount} 🔥");
            Console.ResetColor();
        }

        static void UndergroundLoseAnimation(bool isAllIn)
        {
            if (isAllIn)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n           💀💀💀 全てを失った... 💀💀💀");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("           💀 ハズレ… 💀");
            }
            Console.ResetColor();
            Thread.Sleep(1000);
        }

        static void UndergroundCursedEvent()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkMagenta;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         呪いの発動");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.BackgroundColor = ConsoleColor.Black;
            Console.WriteLine($"\n\n    {undergroundDealerName}が何かを唱え始めた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「五度の敗北...魂に呪いを刻む...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    仮面が赤く光り始める...");
            Thread.Sleep(2000);

            undergroundCursedMode = true;

            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n    💀 呪いモード発動！当たり確率が半減！ 💀");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("地下の呪い"))
                unlockedEvents.Add("地下の呪い");
        }
        static void UndergroundRandomEvent()
        {
            int eventType = rand.Next(6);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");

            switch (eventType)
            {
                case 0:
                    Console.WriteLine("    壁から血が滴っている...");
                    break;
                case 1:
                    Console.WriteLine("    どこからか悲鳴が聞こえる...");
                    break;
                case 2:
                    Console.WriteLine($"    {undergroundDealerName}が不気味に笑っている...");
                    break;
                case 3:
                    Console.WriteLine("    床に血痕が...誰かがここで...");
                    break;
                case 4:
                    Console.WriteLine("    鎖の音が響く...誰かが繋がれている...");
                    if (!unlockedEvents.Contains("地下の囚人"))
                        unlockedEvents.Add("地下の囚人");
                    break;
                case 5:
                    Console.WriteLine("    仮面の奥から赤い目が光った...");
                    break;
            }

            Console.ResetColor();
            Thread.Sleep(2500);
        }
        static void UndergroundAllInLoseEvent()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         全財産喪失");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);
            Console.WriteLine("\n\n    全てを失った...");
            Thread.Sleep(2000);

            Console.WriteLine($"\n    {undergroundDealerName}が静かに語りかける...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「運がなかったな...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...だが、まだチャンスはある」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「もっと...深い場所へ行くか？」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n    仮面の奥で何かがうごめいている...");
            Console.ResetColor();
            Thread.Sleep(2000);

            if (!unlockedEvents.Contains("全財産喪失"))
                unlockedEvents.Add("全財産喪失");
        }

        // ========== セーブ機能 ==========
        static void SaveGame(int slot)
        {
            try
            {
                if (!Directory.Exists("saves"))
                    Directory.CreateDirectory("saves");

                SaveData saveData = new SaveData
                {
                    PlayerName = playerName,
                    SaveDate = DateTime.Now,
                    PlayTime = DateTime.Now - startTime,
                    SaveSlot = slot,

                    Money = money,
                    Debt = debt,
                    MaxMoney = maxMoney,
                    MaxDebt = maxDebt,

                    TotalSpins = totalSpins,
                    Total777Count = total777Count,
                    ConsecutiveWins = consecutiveWins,
                    MaxConsecutiveWins = maxConsecutiveWins,
                    TotalWinAmount = totalWinAmount,
                    TotalLoseAmount = totalLoseAmount,
                    TotalLoses = totalLoses,
                    BigWinCount = bigWinCount,

                    Setting = setting,
                    DebtTurnsRemaining = debtTurnsRemaining,
                    HasEverBorrowedMoney = hasEverBorrowedMoney,

                    GodMode = godMode,
                    GodModeRemaining = godModeRemaining,
                    ConsecutiveHundredPlays = consecutiveHundredPlays,

                    LuckyTimeActive = luckyTimeActive,
                    LuckyTimeRemaining = luckyTimeRemaining,

                    HasSeenConversation = hasSeenConversation,
                    HasSeenMysteriousWoman = hasSeenMysteriousWoman,

                    ItemInventory = new Dictionary<string, int>(itemInventory),
                    TotalLuckyCoinsPurchased = totalLuckyCoinsPurchased,

                    HasGreedRing = hasGreedRing,
                    GreedRingEquipped = greedRingEquipped,
                    GreedRingLoseCount = greedRingLoseCount,

                    VipRoomUnlocked = vipRoomUnlocked,
                    IsInVIPRoom = isInVIPRoom,
                    VipConsecutiveLoses = vipConsecutiveLoses,
                    Vip777Count = vip777Count,
                    Vip5000BetWin = vip5000BetWin,
                    VipTotalVisits = vipTotalVisits,
                    VipTotalWins = vipTotalWins,
                    VipTotalSpins = vipTotalSpins,
                    HasSeenVIPDealer = hasSeenVIPDealer,

                    UndergroundUnlocked = undergroundUnlocked,
                    IsInUnderground = isInUnderground,
                    UndergroundVisits = undergroundVisits,
                    UndergroundWins = undergroundWins,
                    UndergroundAllInWin = undergroundAllInWin,
                    HasSeenUndergroundDealer = hasSeenUndergroundDealer,

                    DevilContractOffered = devilContractOffered,
                    DevilContractType = devilContractType,
                    DevilContractActive = devilContractActive,
                    DevilContractTurns = devilContractTurns,
                    ContractStartTime = contractStartTime,
                    Contract1Complete = contract1Complete,
                    DevilContractSuccess = devilContractSuccess,

                    AddictionLevel = addictionLevel,
                    IsAddicted = isAddicted,
                    AddictionWarningCount = addictionWarningCount,
                    HasUsedRehab = hasUsedRehab,

                    CursedItemCount = cursedItemCount,
                    HasDevilCoin = hasDevilCoin,
                    DevilCoinCurse = devilCoinCurse,
                    DevilCoinWin = devilCoinWin,
                    HasBloodAmulet = hasBloodAmulet,
                    BloodAmuletLoses = bloodAmuletLoses,
                    BloodAmulet5Wins = bloodAmulet5Wins,
                    HasDeathRing = hasDeathRing,
                    DeathRing10Wins = deathRing10Wins,
                    HasTimeClock = hasTimeClock,
                    HasOracleBall = hasOracleBall,
                    OracleBallPrediction = oracleBallPrediction,
                    DevilCoinActive = devilCoinActive,
                    BloodAmuletEquipped = bloodAmuletEquipped,
                    DeathRingEquipped = deathRingEquipped,
                    TimeClockEquipped = timeClockEquipped,


                    MetaEventCount = metaEventCount,

                    UnlockedSymbols = new List<string>(unlockedSymbols),
                    UnlockedEvents = new List<string>(unlockedEvents),
                    UndergroundConsecutiveLoses = undergroundConsecutiveLoses,
                    UndergroundTotalSpins = undergroundTotalSpins,
                    UndergroundCursedMode = undergroundCursedMode,

                    Missions = missions.Select(m => new MissionSaveData
                    {
                        Name = m.Name,
                        Description = m.Description,
                        Reward = m.Reward,
                        Completed = m.Completed
                    }).ToList(),

                    Rankings = new List<HighScore>(rankings),

                    TrueEndingUnlocked = trueEndingUnlocked,
                    GodModePermanent = godModePermanent,
                    Contract1WinCount = contract1WinCount,
                    Contract2Deadline = contract2Deadline,
                    Contract2OriginalDebt = contract2OriginalDebt,

                    OverflowCleared = overflowCleared,
                    RtaCleared = rtaCleared,
                    GameStartTime = gameStartTime,
                    ShopVisitCount = shopVisitCount,
                    ShopCloseWithoutBuyCount = shopCloseWithoutBuyCount,
                    BellMetFirst = bellMetFirst,
                    MissionOpenCount = missionOpenCount,
                    GodModeActivateCount = godModeActivateCount,
                    DreamCasinoUnlocked = dreamCasinoUnlocked,
                    DreamLayerCleared = dreamLayerCleared,
                    MushroomManMet = mushroomManMet,
                    LuckyCoinsTotal = luckyCoinsTotal,
                    ConsecutiveLosses = consecutiveLosses,

                    Chapter1Seen = chapter1Seen,
                    MemoryFragmentsCleared = memoryFragmentsCleared,
                    BlackSuitIntroduced = blackSuitIntroduced,
                    AbandonedCasinoUnlocked = abandonedCasinoUnlocked,
                    AbandonedCasinoEntered = abandonedCasinoEntered,
                    VanityKeyPurchased = vanityKeyPurchased,
                    RoomsOpened = roomsOpened,
                    HasInnocentGem = hasInnocentGem,
                    HasJewelRing = hasJewelRing,
                    HasExchangedMoney = hasExchangedMoney,
                    HasUnknownCoin = hasUnknownCoin,
                    UnknownCoinFlipCount = unknownCoinFlipCount,
                    BellRouteACompleted = bellRouteACompleted,
                    BellRouteBCompleted = bellRouteBCompleted,

                };

                string json = JsonSerializer.Serialize(saveData, new JsonSerializerOptions
                {
                    WriteIndented = true
                });

                File.WriteAllText($"saves/save_{slot}.json", json);

                if (slot != 0) // オートセーブ以外
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    ╔═══════════════════════════════╗");
                    Console.WriteLine("    ║                               ║");
                    Console.WriteLine($"   ║ スロット{slot}にセーブ完了！  ║");
                    Console.WriteLine("    ║                               ║");
                    Console.WriteLine("    ╚═══════════════════════════════╝");
                    Console.ResetColor();
                    Console.WriteLine($"\n    日時: {saveData.SaveDate:yyyy/MM/dd HH:mm:ss}");
                    Console.WriteLine($"    所持金: {money}G");
                    Console.WriteLine($"    総回転数: {totalSpins}回");
                    Thread.Sleep(2000);
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n\nセーブに失敗しました: {ex.Message}");
                Console.ResetColor();
                Thread.Sleep(2000);
            }
        }

        // ========== ロード機能 ==========
        static bool LoadGame(int slot)
        {
            try
            {
                string filePath = $"saves/save_{slot}.json";

                if (!File.Exists(filePath))
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"\n\nスロット{slot}にセーブデータがありません");
                    Console.ResetColor();
                    Thread.Sleep(1500);
                    return false;
                }

                string json = File.ReadAllText(filePath);
                SaveData? saveData = JsonSerializer.Deserialize<SaveData>(json);
                if (saveData == null) return false;

                playerName = saveData.PlayerName;
                startTime = DateTime.Now - saveData.PlayTime;

                money = saveData.Money;
                debt = saveData.Debt;
                maxMoney = saveData.MaxMoney;
                maxDebt = saveData.MaxDebt;

                totalSpins = saveData.TotalSpins;
                total777Count = saveData.Total777Count;
                consecutiveWins = saveData.ConsecutiveWins;
                maxConsecutiveWins = saveData.MaxConsecutiveWins;
                totalWinAmount = saveData.TotalWinAmount;
                totalLoseAmount = saveData.TotalLoseAmount;
                totalLoses = saveData.TotalLoses;
                bigWinCount = saveData.BigWinCount;

                setting = saveData.Setting;
                debtTurnsRemaining = saveData.DebtTurnsRemaining;
                hasEverBorrowedMoney = saveData.HasEverBorrowedMoney;

                godMode = saveData.GodMode;
                godModeRemaining = saveData.GodModeRemaining;
                consecutiveHundredPlays = saveData.ConsecutiveHundredPlays;

                luckyTimeActive = saveData.LuckyTimeActive;
                luckyTimeRemaining = saveData.LuckyTimeRemaining;

                hasSeenConversation = saveData.HasSeenConversation;
                hasSeenMysteriousWoman = saveData.HasSeenMysteriousWoman;

                itemInventory = new Dictionary<string, int>(saveData.ItemInventory);
                totalLuckyCoinsPurchased = saveData.TotalLuckyCoinsPurchased;

                hasGreedRing = saveData.HasGreedRing;
                greedRingEquipped = saveData.GreedRingEquipped;
                greedRingLoseCount = saveData.GreedRingLoseCount;

                vipRoomUnlocked = saveData.VipRoomUnlocked;
                isInVIPRoom = saveData.IsInVIPRoom;
                vipConsecutiveLoses = saveData.VipConsecutiveLoses;
                vip777Count = saveData.Vip777Count;
                vip5000BetWin = saveData.Vip5000BetWin;
                vipTotalVisits = saveData.VipTotalVisits;
                vipTotalWins = saveData.VipTotalWins;
                vipTotalSpins = saveData.VipTotalSpins;
                hasSeenVIPDealer = saveData.HasSeenVIPDealer;

                undergroundUnlocked = saveData.UndergroundUnlocked;
                isInUnderground = saveData.IsInUnderground;
                undergroundVisits = saveData.UndergroundVisits;
                undergroundWins = saveData.UndergroundWins;
                undergroundAllInWin = saveData.UndergroundAllInWin;
                hasSeenUndergroundDealer = saveData.HasSeenUndergroundDealer;

                devilContractOffered = saveData.DevilContractOffered;
                devilContractType = saveData.DevilContractType;
                devilContractActive = saveData.DevilContractActive;
                devilContractTurns = saveData.DevilContractTurns;
                contractStartTime = saveData.ContractStartTime;
                contract1Complete = saveData.Contract1Complete;
                devilContractSuccess = saveData.DevilContractSuccess;

                addictionLevel = saveData.AddictionLevel;
                isAddicted = saveData.IsAddicted;
                addictionWarningCount = saveData.AddictionWarningCount;
                hasUsedRehab = saveData.HasUsedRehab;

                cursedItemCount = saveData.CursedItemCount;
                hasDevilCoin = saveData.HasDevilCoin;
                devilCoinCurse = saveData.DevilCoinCurse;
                devilCoinWin = saveData.DevilCoinWin;
                hasBloodAmulet = saveData.HasBloodAmulet;
                bloodAmuletLoses = saveData.BloodAmuletLoses;
                bloodAmulet5Wins = saveData.BloodAmulet5Wins;
                hasDeathRing = saveData.HasDeathRing;
                deathRing10Wins = saveData.DeathRing10Wins;
                hasTimeClock = saveData.HasTimeClock;
                hasOracleBall = saveData.HasOracleBall;
                oracleBallPrediction = saveData.OracleBallPrediction;
                devilCoinActive = saveData.DevilCoinActive;
                bloodAmuletEquipped = saveData.BloodAmuletEquipped;
                deathRingEquipped = saveData.DeathRingEquipped;
                timeClockEquipped = saveData.TimeClockEquipped;

                metaEventCount = saveData.MetaEventCount;

                unlockedSymbols = new List<string>(saveData.UnlockedSymbols);
                unlockedEvents = new List<string>(saveData.UnlockedEvents);
                undergroundConsecutiveLoses = saveData.UndergroundConsecutiveLoses;
                undergroundTotalSpins = saveData.UndergroundTotalSpins;
                undergroundCursedMode = saveData.UndergroundCursedMode;

                missions.Clear();
                InitializeMissions();
                for (int i = 0; i < saveData.Missions.Count && i < missions.Count; i++)
                {
                    missions[i].Completed = saveData.Missions[i].Completed;
                    missions[i].Name = saveData.Missions[i].Name;
                    missions[i].Description = saveData.Missions[i].Description;
                }

                rankings = new List<HighScore>(saveData.Rankings);

                trueEndingUnlocked = saveData.TrueEndingUnlocked;
                godModePermanent = saveData.GodModePermanent;
                contract1WinCount = saveData.Contract1WinCount;
                contract2Deadline = saveData.Contract2Deadline;
                contract2OriginalDebt = saveData.Contract2OriginalDebt;

                overflowCleared = saveData.OverflowCleared;
                rtaCleared = saveData.RtaCleared;
                gameStartTime = saveData.GameStartTime;

                shopVisitCount = saveData.ShopVisitCount;
                shopCloseWithoutBuyCount = saveData.ShopCloseWithoutBuyCount;
                bellMetFirst = saveData.BellMetFirst;
                missionOpenCount = saveData.MissionOpenCount;
                godModeActivateCount = saveData.GodModeActivateCount;

                dreamCasinoUnlocked = saveData.DreamCasinoUnlocked;
                dreamLayerCleared = saveData.DreamLayerCleared;
                mushroomManMet = saveData.MushroomManMet;
                luckyCoinsTotal = saveData.LuckyCoinsTotal;
                consecutiveLosses = saveData.ConsecutiveLosses;

                chapter1Seen = saveData.Chapter1Seen;
                memoryFragmentsCleared = saveData.MemoryFragmentsCleared;
                blackSuitIntroduced = saveData.BlackSuitIntroduced;
                abandonedCasinoUnlocked = saveData.AbandonedCasinoUnlocked;
                abandonedCasinoEntered = saveData.AbandonedCasinoEntered;
                vanityKeyPurchased = saveData.VanityKeyPurchased;
                if (saveData.RoomsOpened != null) roomsOpened = saveData.RoomsOpened;
                hasInnocentGem = saveData.HasInnocentGem;
                hasJewelRing = saveData.HasJewelRing;
                hasExchangedMoney = saveData.HasExchangedMoney;
                hasUnknownCoin = saveData.HasUnknownCoin;
                unknownCoinFlipCount = saveData.UnknownCoinFlipCount;
                bellRouteACompleted = saveData.BellRouteACompleted;
                bellRouteBCompleted = saveData.BellRouteBCompleted;

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ╔═══════════════════════════════╗");
                Console.WriteLine("    ║                               ║");
                Console.WriteLine($"   ║ スロット{slot}からロード完了！║");
                Console.WriteLine("    ║                               ║");
                Console.WriteLine("    ╚═══════════════════════════════╝");
                Console.ResetColor();
                Console.WriteLine($"\n    プレイヤー: {playerName}");
                Console.WriteLine($"    セーブ日時: {saveData.SaveDate:yyyy/MM/dd HH:mm:ss}");
                Console.WriteLine($"    所持金: {money}G");
                Console.WriteLine($"    総回転数: {totalSpins}回");
                Thread.Sleep(2500);

                return true;
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n\nロードに失敗しました: {ex.Message}");
                Console.ResetColor();
                Thread.Sleep(2000);
                return false;
            }
        }

        // ========== セーブメニュー ==========
        static void SaveMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║          💾 セーブ 💾            ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.ResetColor();

                Console.WriteLine($"\n所持金: {money}G\n");
                Console.WriteLine("【セーブスロット選択】\n");

                for (int i = 1; i <= 3; i++)
                {
                    Console.WriteLine($"  [{i}] スロット{i}");

                    string filePath = $"saves/save_{i}.json";
                    if (File.Exists(filePath))
                    {
                        try
                        {
                            string json = File.ReadAllText(filePath);
                            SaveData saveData = JsonSerializer.Deserialize<SaveData>(json) ?? throw new Exception("データが空です");

                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine($"      名前: {saveData.PlayerName}");
                            Console.WriteLine($"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}");
                            Console.WriteLine($"      所持金: {saveData.Money}G");
                            Console.WriteLine($"      回転数: {saveData.TotalSpins}回");
                            Console.ResetColor();
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("      [データ破損]");
                            Console.ResetColor();
                        }
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.DarkGray;
                        Console.WriteLine("      [空きスロット]");
                        Console.ResetColor();
                    }
                    Console.WriteLine();
                }

                Console.WriteLine("  [0] 戻る\n");
                Console.Write("選択 > ");

                var key = Console.ReadKey(true);

                if (key.KeyChar == '0') break;
                else if (key.KeyChar >= '1' && key.KeyChar <= '3')
                {
                    int slot = int.Parse(key.KeyChar.ToString());

                    if (File.Exists($"saves/save_{slot}.json"))
                    {
                        Console.WriteLine($"\n\nスロット{slot}に上書きしますか？ [Y/N]");
                        var confirm = Console.ReadKey(true);
                        if (confirm.Key != ConsoleKey.Y)
                            continue;
                    }

                    SaveGame(slot);
                    break;
                }
            }
        }

        // ========== ロードメニュー ==========
        static void LoadMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║          📂 ロード 📂            ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.ResetColor();

                Console.WriteLine("\n【ロードスロット選択】\n");

                bool hasAnySave = false;

                for (int i = 1; i <= 3; i++)
                {
                    string filePath = $"saves/save_{i}.json";

                    if (File.Exists(filePath))
                    {
                        hasAnySave = true;
                        Console.WriteLine($"  [{i}] スロット{i}");

                        try
                        {
                            string json = File.ReadAllText(filePath);
                            SaveData saveData = JsonSerializer.Deserialize<SaveData>(json) ?? throw new Exception("データが空です");

                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine($"      名前: {saveData.PlayerName}");
                            Console.WriteLine($"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}");
                            Console.WriteLine($"      所持金: {saveData.Money}G");
                            Console.WriteLine($"      回転数: {saveData.TotalSpins}回");
                            Console.ResetColor();
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("      [データ破損]");
                            Console.ResetColor();
                        }
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.DarkGray;
                        Console.WriteLine($"  [{i}] スロット{i}");
                        Console.WriteLine("      [データなし]");
                        Console.ResetColor();
                    }
                    Console.WriteLine();
                }

                if (!hasAnySave)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n  セーブデータがありません");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                    break;
                }

                Console.WriteLine("  [0] 戻る\n");
                Console.Write("選択 > ");

                var key = Console.ReadKey(true);

                if (key.KeyChar == '0') break;
                else if (key.KeyChar >= '1' && key.KeyChar <= '3')
                {
                    int slot = int.Parse(key.KeyChar.ToString());

                    if (LoadGame(slot))
                    {
                        return;
                    }
                }
            }
        }

        // ========== セーブデータ削除 ==========
        static void DeleteSaveMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║        ⚠ データ削除 ⚠          ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.ResetColor();

                Console.WriteLine("\n【削除するスロット選択】\n");

                for (int i = 1; i <= 3; i++)
                {
                    Console.WriteLine($"  [{i}] スロット{i}");

                    string filePath = $"saves/save_{i}.json";
                    if (File.Exists(filePath))
                    {
                        try
                        {
                            string json = File.ReadAllText(filePath);
                            SaveData saveData = JsonSerializer.Deserialize<SaveData>(json) ?? throw new Exception("データが空です");

                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine($"      名前: {saveData.PlayerName}");
                            Console.WriteLine($"      日時: {saveData.SaveDate:yyyy/MM/dd HH:mm}");
                            Console.ResetColor();
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("      [データ破損]");
                            Console.ResetColor();
                        }
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.DarkGray;
                        Console.WriteLine("      [データなし]");
                        Console.ResetColor();
                    }
                    Console.WriteLine();
                }

                Console.WriteLine("  [0] 戻る\n");
                Console.Write("選択 > ");

                var key = Console.ReadKey(true);

                if (key.KeyChar == '0') break;
                else if (key.KeyChar >= '1' && key.KeyChar <= '3')
                {
                    int slot = int.Parse(key.KeyChar.ToString());
                    string filePath = $"saves/save_{slot}.json";

                    if (!File.Exists(filePath))
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\n\nデータがありません");
                        Console.ResetColor();
                        Thread.Sleep(1500);
                        continue;
                    }

                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"\n\n本当にスロット{slot}を削除しますか？ [Y/N]");
                    Console.ResetColor();

                    var confirm = Console.ReadKey(true);
                    if (confirm.Key == ConsoleKey.Y)
                    {
                        try
                        {
                            File.Delete(filePath);
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.WriteLine("\n\n削除しました");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\n削除に失敗しました");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                    }
                }
            }
        }

        // ========== ショップメニュー ==========
        static void ShopMenu()
        {
            shopVisitCount++;
            bool boughtSomething = false;

            if (dreamCasinoUnlocked && CanEnterDream())
            {
                if (!mushroomManMet)
                {
                    MushroomManFirstMeet();
                }
                else
                {
                    MushroomManWaiting();
                }
            }

            // ベルの挨拶
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ベル「" + GetBellGreeting() + "」");
            Console.ResetColor();
            Thread.Sleep(2500);

            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║          ♦ ショップ ♦             ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.ResetColor();

                Console.WriteLine($"\n所持金: {money}G\n");
                Console.WriteLine("【通常アイテム】\n");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"  [1] お守り (200G) - 当たりやすくなる（永続）");
                Console.WriteLine($"      所持数: {itemInventory["お守り"]}個");
                if (itemInventory["お守り"] > 0)
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("      ※購入済み");
                    Console.ForegroundColor = ConsoleColor.Yellow;
                }
                Console.WriteLine($"\n  [2] 幸運のコイン (500G) - 次回1回だけ大幅UP（消費）");
                Console.WriteLine($"      所持数: {itemInventory["幸運のコイン"]}個");
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine($"      累計購入数: {totalLuckyCoinsPurchased}個");
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"\n  [3] 返済猶予券/リハビリ券 (1000G)");
                Console.WriteLine($"      借金期限+10回 / 中毒度-50");
                Console.WriteLine($"      所持数: {itemInventory["返済猶予券"]}個");
                Console.ResetColor();

                Console.WriteLine("\n【呪いのアイテム】\n");

                // 悪魔のコイン
                if (totalLoses >= 20)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  [4] 悪魔のコイン (800G)");
                    Console.WriteLine($"      効果: 次回100%勝利 / 呪い: その後5回100%敗北");
                    Console.WriteLine($"      所持数: {(hasDevilCoin ? "1個" : "0個")}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  [4] ??? (条件: 累計負け20回以上)");
                    Console.WriteLine($"      残り: あと{20 - totalLoses}回負けると解放");
                }

                // 血塗られたお守り
                Console.WriteLine();
                if (hasEverBorrowedMoney && totalSpins >= 30)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  [5] 血塗られたお守り (1000G)");
                    Console.WriteLine($"      効果: 当たり確率2倍 / 呪い: 3敗でBAD END");
                    Console.WriteLine($"      所持数: {(hasBloodAmulet ? "1個" : "0個")}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  [5] ??? (条件: 借金経験あり かつ 総回転数30回以上)");
                    if (!hasEverBorrowedMoney)
                        Console.WriteLine($"      借金をまだ経験していない...");
                    else
                        Console.WriteLine($"      残り: あと{Math.Max(0, 30 - totalSpins)}回転で解放");
                }

                // 死神の指輪
                Console.WriteLine();
                if (vip777Count >= 1)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  [6] 死神の指輪 (3000G)");
                    Console.WriteLine($"      効果: 勝ち×10倍 / 呪い: 負け-1000G");
                    Console.WriteLine($"      所持数: {(hasDeathRing ? "1個" : "0個")}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  [6] ??? (条件: VIPルームで777を1回揃える)");
                    if (!vipRoomUnlocked)
                        Console.WriteLine($"      VIPルームがまだ解放されていない...");
                    else
                        Console.WriteLine($"      VIPルームで777を狙え...");
                }

                // 時を刻む懐中時計
                Console.WriteLine();
                if (godModeActivateCount >= 2)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  [7] 時を刻む懐中時計 (1500G)");
                    Console.WriteLine($"      効果: GOD MODE+5回 / 呪い: 1回転3秒制限");
                    Console.WriteLine($"      所持数: {(hasTimeClock ? "1個" : "0個")}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  [7] ??? (条件: GOD MODEを2回以上発動)");
                    Console.WriteLine($"      GOD MODE発動回数: {godModeActivateCount}/2回");
                }

                // 禁断の水晶玉
                Console.WriteLine();
                if (undergroundVisits >= 3)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  [8] 🔮 禁断の水晶玉 (2000G)");
                    Console.WriteLine($"      効果: 次回出目予知 / 50%没収");
                    Console.WriteLine($"      所持数: {(hasOracleBall ? "1個" : "0個")}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  [8] ??? (条件: 地下カジノに3回以上訪問)");
                    if (!undergroundUnlocked)
                        Console.WriteLine($"      地下カジノがまだ解放されていない...");
                    else
                        Console.WriteLine($"      地下訪問回数: {undergroundVisits}/3回");
                }

                Console.ResetColor();

                Console.ResetColor();

                // 換金したお金（無垢な宝石所持中）
                if (hasInnocentGem && !hasExchangedMoney)
                {
                    Console.ForegroundColor = ConsoleColor.DarkYellow;
                    Console.WriteLine("\n  ─────────────────────────────────");
                    Console.WriteLine("  換金したお金　　　　　　　5000G");
                    Console.WriteLine("  ─────────────────────────────────");
                    Console.ResetColor();
                }

                // 隠しページ（チャプター1クリア後）
                if (chapter1Seen && !vanityKeyPurchased)
                {
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("\n  [H] .........");
                    Console.ResetColor();
                }

                Console.WriteLine("\n  [0] 戻る");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);


                if (key.KeyChar == '0')
                {
                    if (!boughtSomething)
                    {
                        Console.ForegroundColor = ConsoleColor.Magenta;
                        Console.WriteLine($"\n    ベル「{GetBellFarewell()}」");
                        Console.ResetColor();
                        Thread.Sleep(2000);

                        // 優柔不断ミッション達成チェック
                        if (shopCloseWithoutBuyCount == 5)
                        {
                            Console.Clear();
                            Console.ForegroundColor = ConsoleColor.DarkMagenta;
                            Console.WriteLine("\n\n\n");
                            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
                            Console.WriteLine("         隠しミッション発見！");
                            Console.WriteLine("         「優柔不断」");
                            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
                            Console.WriteLine("\n    迷うことも、ひとつの選択だ");
                            Console.ResetColor();
                            Thread.Sleep(3000);
                        }
                    }
                    break;
                }

                // 換金したお金
                if ((key.KeyChar == 'e' || key.KeyChar == 'E') && hasInnocentGem && !hasExchangedMoney)
                {
                    BuyExchangedMoney();
                    break;
                }

                // 隠しページ
                if ((key.KeyChar == 'h' || key.KeyChar == 'H') && chapter1Seen && !vanityKeyPurchased)
                {
                    ShopHiddenPage();
                    continue;
                }

                switch (key.KeyChar)
                {
                    case '1':
                        if (itemInventory["お守り"] > 0)
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\nお守りは既に購入済みです");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                        else if (money >= 200)
                        {
                            money -= 200;
                            itemInventory["お守り"]++;
                            boughtSomething = true;
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.WriteLine("\n\nお守りを購入しました！");
                            Console.ForegroundColor = ConsoleColor.Magenta;
                            Console.WriteLine($"\n    ベル「{GetBellPurchaseComment("お守り")}」");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\n所持金が足りません...");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                        break;

                    case '2':
                        if (money >= 500)
                        {
                            money -= 500;
                            itemInventory["幸運のコイン"]++;
                            totalLuckyCoinsPurchased++;
                            luckyCoinsTotal++;
                            if (luckyCoinsTotal >= 10 && !dreamCasinoUnlocked)
                            {
                                dreamCasinoUnlocked = true;
                            }
                            boughtSomething = true;
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.WriteLine("\n\n幸運のコインを購入しました！");
                            Console.WriteLine($"累計購入数: {totalLuckyCoinsPurchased}個");
                            Console.ForegroundColor = ConsoleColor.Magenta;
                            Console.WriteLine($"\n    ベル「{GetBellPurchaseComment("幸運のコイン")}」");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\n所持金が足りません...");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                        break;

                    case '3':
                        if (money >= 1000)
                        {
                            money -= 1000;
                            itemInventory["返済猶予券"]++;
                            boughtSomething = true;
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.WriteLine("\n\n返済猶予券を購入しました！");
                            Console.ForegroundColor = ConsoleColor.Magenta;
                            Console.WriteLine($"\n    ベル「{GetBellPurchaseComment("返済猶予券")}」");
                            Console.ResetColor();
                            Thread.Sleep(2000);
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\n\n所持金が足りません...");
                            Console.ResetColor();
                            Thread.Sleep(1500);
                        }
                        break;

                    case '4':
                        if (PurchaseCursedItemWithBell("悪魔のコイン", 800, ref hasDevilCoin))
                            boughtSomething = true;
                        break;

                    case '5':
                        if (PurchaseCursedItemWithBell("血塗られたお守り", 1000, ref hasBloodAmulet))
                            boughtSomething = true;
                        break;

                    case '6':
                        if (PurchaseCursedItemWithBell("死神の指輪", 3000, ref hasDeathRing))
                            boughtSomething = true;
                        break;

                    case '7':
                        if (PurchaseCursedItemWithBell("時を刻む懐中時計", 1500, ref hasTimeClock))
                            boughtSomething = true;
                        break;

                    case '8':
                        if (PurchaseCursedItemWithBell("禁断の水晶玉", 2000, ref hasOracleBall))
                            boughtSomething = true;
                        break;

                    default:
                        Console.WriteLine("\n\n正しい番号を選択してください");
                        Thread.Sleep(1000);
                        break;

                }
            }
        }
        static bool CanEnterDream()
        {
            int hour = DateTime.Now.Hour;
            bool isLateNight = hour >= 22 || hour < 5;

            switch (dreamLayerCleared)
            {
                case 0: return dreamCasinoUnlocked && isLateNight && addictionLevel >= 50;
                case 1: return isLateNight && consecutiveWins == 0 && totalLoses >= 3;
                case 2: return isLateNight && debt > 0;
                case 3: return isLateNight && money <= 100;
                case 4: return isLateNight && addictionLevel >= 80;
                default: return false;
            }
        }
        static void MushroomManFirstMeet()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n");
            Console.WriteLine("    気づくと、見知らぬ男が立っていた");
            Console.WriteLine("    顔が…キノコだった");
            Console.WriteLine("    スーツを着ていた");
            Console.WriteLine("    じっとこちらを見ていた");
            Thread.Sleep(2000);

            Console.WriteLine("\n    男が口を開いた");
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n    「※▲◎♪✦□…」");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("    「…よる…ねむい…▲◎※…」");
            Thread.Sleep(1500);
            Console.WriteLine("\n    意味が分からなかった");
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine("\n    …これは何かのヒントか？");
            Thread.Sleep(2000);

            Console.WriteLine("\n    [1] 頷く");
            Console.WriteLine("    [2] 首を振る");
            Console.WriteLine("    [3] 無視する");
            Console.WriteLine("    [4] 話しかけてみる");
            Console.ResetColor();

            string input = Console.ReadLine() ?? string.Empty;
            // どれを選んでも同じ

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n");
            Console.WriteLine("    男はゆっくりと頷いた");
            Thread.Sleep(1500);
            Console.WriteLine("    そして振り返り");
            Thread.Sleep(1000);
            Console.WriteLine("    奥の扉の方へ歩き始めた");
            Thread.Sleep(2000);

            Console.WriteLine("\n    [1] ついていく");
            Console.WriteLine("    [2] ついていかない");
            Console.ResetColor();

            input = Console.ReadLine() ?? string.Empty;
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n");
                Console.WriteLine("    男は扉の前で立ち止まり");
                Thread.Sleep(1000);
                Console.WriteLine("    こちらを見た");
                Thread.Sleep(1000);
                Console.WriteLine("    ただ、待っていた");
                Thread.Sleep(2000);
                Console.ResetColor();
                // 結局入る
            }

            mushroomManMet = true;
            EnterDreamCasino();
        }
        static void EnterDreamCasino()
        {
            switch (dreamLayerCleared)
            {
                case 0: DreamLayer1(); break;
                case 1: DreamLayer2(); break;
                case 2: DreamLayer3(); break;
                case 3: DreamLayer4(); break;
                case 4: DreamLayerFinal(); break;
            }
        }
        static void DreamLayer1()
        {
            Console.Clear();
            Thread.Sleep(1000);

            TypeText("    気づいたら、カジノにいた");
            Thread.Sleep(1500);
            TypeText("\n    …でも");
            Thread.Sleep(1000);
            TypeText("\n    気のせいか");
            TypeText("\n    なんだかここはさっきまでいたカジノではない気がする");
            Thread.Sleep(1500);
            TypeText("\n\n    誰もいない");
            Thread.Sleep(800);
            TypeText("\n    音もない");
            Thread.Sleep(800);
            TypeText("\n    スロットだけが");
            TypeText("\n    ただそこにある");
            Thread.Sleep(2000);

            TypeText("\n\n    …どこからか声が聞こえた");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;

            BellDreamLine("あら、いらっしゃい♪ 待ってたわよ？");
            BellDreamLine("また来たのね♪ やっぱり来ると思ってた");
            BellDreamLine("さすが、目の付け所がいいわね♪");
            BellDreamLine("またいつでも来てね♪ 待ってるから");

            Thread.Sleep(1500);
            Console.ResetColor();
            Console.ForegroundColor = ConsoleColor.DarkGray;

            TypeText("\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「ねえ」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…あなたは、どうして来たの？」");
            Thread.Sleep(3000);

            // 暗転
            Console.Clear();
            Console.ResetColor();
            Thread.Sleep(1000);

            // 目覚め
            DreamWakeUp(1);
        }
        static void DreamLayer2()
        {
            Console.Clear();
            Thread.Sleep(1000);

            TypeText("    また、カジノにいた");
            Thread.Sleep(1500);
            TypeText("\n\n    前より");
            TypeText("\n    少し暗い気がした");
            Thread.Sleep(1000);
            TypeText("\n\n    気のせいかもしれない");
            Thread.Sleep(1500);
            TypeText("\n\n    …でも");
            TypeText("\n    なんとなく");
            TypeText("\n    そう感じた");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;

            BellDreamLine("…顔色悪いわよ？");
            BellDreamLine("まあ、私には関係ないけど♪");
            BellDreamLine("借金があっても来てくれるのね。…うれしい♪");
            BellDreamLine("無理しなくていいわよ");
            BellDreamLine("…大丈夫？ まあ、大丈夫じゃないわよね♪");

            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「ねえ」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…大丈夫って」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…誰かに言われたこと、あった？」");
            Thread.Sleep(3000);

            Console.Clear();
            Console.ResetColor();
            Thread.Sleep(1000);

            DreamWakeUp(2);
        }
        static void DreamLayer3()
        {
            Console.Clear();
            Thread.Sleep(1000);

            TypeText("    また、カジノにいた");
            Thread.Sleep(1500);
            TypeText("\n\n    もっと暗くなっていた");
            Thread.Sleep(1000);
            TypeText("\n\n    スロットの光だけが");
            TypeText("\n    ぼんやりと灯っていた");
            Thread.Sleep(1500);
            TypeText("\n\n    …誰かが泣いている気がした");
            Thread.Sleep(1000);
            TypeText("\n    気のせいかもしれない");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;

            BellDreamLine("こんな時間に来るなんて…");
            BellDreamLine("…帰ってきたのね♪");
            BellDreamLine("…無事でよかった。本当に");
            BellDreamLine("また来てね♪ 待ってるから");

            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「ねえ」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…待ってたら」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…来てくれると思ってた？」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypeText("\n\n    ベル「…私は」");
            Thread.Sleep(3000);

            Console.Clear();
            Console.ResetColor();
            Thread.Sleep(1000);

            DreamWakeUp(3);
        }
        static void DreamLayer4()
        {
            Console.Clear();
            Thread.Sleep(1000);

            TypeText("    また、カジノにいた");
            Thread.Sleep(1500);
            TypeText("\n\n    光がほとんどなかった");
            Thread.Sleep(1000);
            TypeText("\n\n    遠くに");
            TypeText("\n    ぼんやりとした明かりだけが見えた");
            Thread.Sleep(1500);
            TypeText("\n\n    …さっきの声が");
            TypeText("\n    まだ耳に残っていた");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkCyan;

            BellDreamLine("…ねえ、覚えてる？");
            BellDreamLine("…あなたは、どうして来たの？");
            BellDreamLine("…大丈夫って、誰かに言われたこと、あった？");
            BellDreamLine("…待ってたら、来てくれると思ってた？");

            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n    …長い沈黙…");
            Thread.Sleep(2500);

            Console.ForegroundColor = ConsoleColor.DarkCyan;
            TypeText("\n\n    ベル「…私は」");
            Thread.Sleep(1500);
            TypeText("\n    ベル「…ずっと待ってたのよ」");
            Thread.Sleep(1500);
            TypeText("\n    ベル「…誰かが来てくれると思って」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkCyan;
            TypeText("\n\n    ベル「でも」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkCyan;
            TypeText("\n\n    ベル「…誰も」");
            Thread.Sleep(3000);

            Console.Clear();
            Console.ResetColor();
            Thread.Sleep(1000);

            DreamWakeUp(4);
        }
        static void DreamLayerFinal()
        {
            Console.Clear();
            Thread.Sleep(1500);

            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("    真っ暗だった");
            Thread.Sleep(1500);
            TypeText("\n\n    光が");
            TypeText("\n    一切なかった");
            Thread.Sleep(1500);
            TypeText("\n\n    声だけが聞こえた");
            Thread.Sleep(1000);
            TypeText("\n    あの声だった");
            Thread.Sleep(1500);
            TypeText("\n\n    でも");
            TypeText("\n    笑っていなかった");
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(1000);

            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2500);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「…ずっと、ひとりだった」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「生まれた時から」");
            Thread.Sleep(1000);
            TypeText("\n    「たぶん、ずっと」");
            Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「泣いたこともあった」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「でも誰も来なかった」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「だから泣くのをやめた」");
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …長い沈黙…");
            Thread.Sleep(3000);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「居場所ができたと思った」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「それだけでよかった」");
            Thread.Sleep(1000);
            TypeText("\n    「それだけで」");
            Thread.Sleep(1000);
            TypeText("\n    「十分だったのに」");
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …長い沈黙…");
            Thread.Sleep(3000);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「…なんで」");
            Thread.Sleep(4000);

            Console.Clear();
            Thread.Sleep(1000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);

            TypeText("\n\n    暗闇の中に");
            TypeText("\n    指輪だけが光っていた");
            Thread.Sleep(3000);

            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「持っていって」");
            Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypeText("\n\n    …沈黙…");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.White;
            TypeText("\n\n    「お願い」");
            Thread.Sleep(4000);

            // 暗転
            Console.Clear();
            Console.ResetColor();
            Thread.Sleep(2000);

            // 強欲の指輪入手
            hasGreedRing = true;
            dreamLayerCleared = 5;

            DreamWakeUpFinal();
        }
        static void DreamWakeUp(int layer)
        {
            dreamLayerCleared = layer;

            Console.ForegroundColor = ConsoleColor.DarkGray;

            string hint = layer switch
            {
                1 => "…まけ…つづける…",
                2 => "…かりた…かえせない…",
                3 => "…なにも…ない…",
                4 => "…もどれない…",
                _ => ""
            };

            TypeText("    目が覚めた");
            Thread.Sleep(1500);
            TypeText("\n\n    耳の奥に声が残っていた");
            Thread.Sleep(1000);
            TypeText($"\n\n    「{hint}」");
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Gray;
            TypeText("\n\n    …これは何かのヒントか？");
            Thread.Sleep(3000);
            Console.ResetColor();

            // 3層クリア後：無垢な宝石が出現
            if (layer == 3 && !hasInnocentGem)
            {
                InnocentGemFound();
            }
        }
        static void DreamWakeUpFinal()
        {
            Console.ForegroundColor = ConsoleColor.DarkGray;

            TypeText("    目が覚めた");
            Thread.Sleep(1500);
            TypeText("\n    手の中に…指輪がある");
            Thread.Sleep(2000);
            TypeText("\n\n    夢だったのか");
            Thread.Sleep(1000);
            TypeText("\n    それとも");
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(500);

            TypeText("\n\n    その時");
            Thread.Sleep(1500);
            TypeText("\n\n    一瞬だけ");
            TypeText("\n    見えた気がした");
            Thread.Sleep(1500);
            TypeText("\n\n    顔がキノコの");
            TypeText("\n    スーツ姿の男");
            Thread.Sleep(1500);
            TypeText("\n\n    ショップの方を");
            TypeText("\n    ただ、見ていた");
            Thread.Sleep(2000);
            TypeText("\n\n    瞬きをしたら");
            TypeText("\n    もういなかった");
            Thread.Sleep(2500);

            Console.ForegroundColor = ConsoleColor.Gray;
            TypeText("\n\n    足が自然と");
            TypeText("\n    ショップに向いていた");
            Thread.Sleep(3000);
            Console.ResetColor();
        }
        static void MushroomManWaiting()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n");
            Console.WriteLine("    キノコの男が立っていた");
            Thread.Sleep(1500);
            Console.WriteLine("    何も言わなかった");
            Thread.Sleep(1000);
            Console.WriteLine("    ただ、こちらを見ていた");
            Thread.Sleep(2000);
            Console.ResetColor();

            EnterDreamCasino();
        }

        static int godModeActivateCount = 0;

        static bool PurchaseCursedItemWithBell(string itemName, int price, ref bool hasItem)
        {
            if (hasItem)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"\n\n{itemName}は既に所持しています");
                Console.ResetColor();
                Thread.Sleep(1500);
                return false;
            }

            if (money < price)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n所持金が足りません...");
                Console.ResetColor();
                Thread.Sleep(1500);
                return false;
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n⚠⚠⚠ 警告 ⚠⚠⚠\n");
            Console.WriteLine($"{itemName}を購入しますか？\n");
            Console.WriteLine("これは呪われたアイテムです");
            Console.WriteLine("強力な効果と引き換えに恐ろしい代償を払います");
            Console.WriteLine("\n本当に購入しますか？ [Y/N]");
            Console.ResetColor();

            var confirm = Console.ReadKey(true);
            if (confirm.Key == ConsoleKey.Y)
            {
                money -= price;
                hasItem = true;
                cursedItemCount++;

                Console.Clear();
                for (int i = 0; i < 5; i++)
                {
                    Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                    Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                    Console.Clear();
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine($"    {itemName}を手に入れた...");
                    Console.WriteLine("\n    呪いのオーラを感じる...");
                    Thread.Sleep(300);
                }

                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"\n\n{itemName}を購入しました！");
                Console.WriteLine("\n※装備管理[E]から装備できます");
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n    ベル「{GetBellPurchaseComment(itemName)}」");
                Console.ResetColor();
                Thread.Sleep(2500);

                if (!unlockedEvents.Contains($"{itemName}入手"))
                    unlockedEvents.Add($"{itemName}入手");

                return true;
            }

            return false;
        }
        static void TypeText(string text, int delay = 40)
        {
            foreach (char c in text)
            {
                Console.Write(c);
                Thread.Sleep(delay);
            }
        }

        static void BellDreamLine(string line)
        {
            Thread.Sleep(800);
            Console.WriteLine($"\n    ベル「{line}」");
            Thread.Sleep(1200);
        }

        // ========== 装備管理 ==========
        static void EquipmentMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║          ⚔ 装備管理 ⚔          ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.ResetColor();

                Console.WriteLine("\n【現在の装備】\n");

                if (greedRingEquipped)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("  💀 強欲の指輪 [装備中]");
                    Console.WriteLine("     効果: 負け-500G / 勝ち×5倍");
                    Console.WriteLine("     デメリット: 他装備無効、演出なし、運気大幅DOWN");
                    Console.ResetColor();
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine("  装備なし");
                    Console.ResetColor();
                }

                Console.WriteLine("\n\n【所持アイテム】\n");

                // 強欲の指輪
                if (hasGreedRing)
                {
                    Console.ForegroundColor = greedRingEquipped ? ConsoleColor.DarkGray : ConsoleColor.Red;
                    Console.WriteLine("  [1] 💀 強欲の指輪");
                    if (!greedRingEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      [装備する]");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      [装備中 - 2で外す]");
                    }
                    Console.ResetColor();
                }

                // 悪魔のコイン
                if (hasDevilCoin)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("  [3] 💀 悪魔のコイン");
                    Console.WriteLine("      次回100%勝利 → その後5回100%負け");
                    if (devilCoinActive)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      [使用済み - 呪い発動中]");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("      [使用する]");
                    }
                    Console.ResetColor();
                }

                // 血塗られたお守り
                if (hasBloodAmulet)
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("  [4] 🩸 血塗られたお守り");
                    Console.WriteLine("      当たり確率2倍 / 3敗でBAD END");
                    if (bloodAmuletEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine($"      [装備中 - 負け: {bloodAmuletLoses}/3]");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("      [装備する]");
                    }
                    Console.ResetColor();
                }

                // 死神の指輪
                if (hasDeathRing)
                {
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("  [5] 💀 死神の指輪");
                    Console.WriteLine("      勝ち×10倍 / 負け-1000G");
                    if (deathRingEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      [装備中]");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("      [装備する]");
                    }
                    Console.ResetColor();
                }

                // 時を刻む懐中時計
                if (hasTimeClock)
                {
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine("  [6] ⏰ 時を刻む懐中時計");
                    Console.WriteLine("      GOD MODE+5 / 1回転3秒制限");
                    if (timeClockEquipped)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("      [装備中]");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("      [装備する]");
                    }
                    Console.ResetColor();
                }

                // 禁断の水晶玉
                if (hasOracleBall)
                {
                    Console.ForegroundColor = ConsoleColor.Blue;
                    Console.WriteLine("  [7] 🔮 禁断の水晶玉");
                    Console.WriteLine("      次回出目予知 / 50%没収");
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("      [使用する]");
                    Console.ResetColor();
                }

                // 🆕 リハビリ券
                if (itemInventory["返済猶予券"] > 0)
                {
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine("\n  [8] 🩺 リハビリ券");
                    Console.WriteLine("      中毒度-50 / 心の回復");
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"      [使用する - 所持数: {itemInventory["返済猶予券"]}個]");
                    Console.ResetColor();
                }

                Console.WriteLine("\n  [9] 全装備を外す");
                Console.WriteLine("\n  [0] 戻る");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);

                if (key.KeyChar == '0') break;

                // 強欲の指輪装備
                if (key.KeyChar == '1' && hasGreedRing && !greedRingEquipped)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n⚠ 警告 ⚠\n");
                    Console.WriteLine("強欲の指輪を装備しますか？\n");
                    Console.WriteLine("装備すると：");
                    Console.WriteLine("  ・負けるたびに-500G（所持金不足なら借金）");
                    Console.WriteLine("  ・勝つと獲得金×5倍");
                    Console.WriteLine("  ・お守り、幸運のコイン無効化");
                    Console.WriteLine("  ・全ての特殊演出が発生しなくなる");
                    Console.WriteLine("  ・当たり確率が大幅DOWN（約14%）");
                    Console.WriteLine("  ・借金5000G到達でBAD END");
                    Console.WriteLine("\n本当に装備しますか？ [Y/N]");
                    Console.ResetColor();

                    var confirm = Console.ReadKey(true);
                    if (confirm.Key == ConsoleKey.Y)
                    {
                        greedRingEquipped = true;
                        GreedRingEquipAnimation();
                        if (!unlockedEvents.Contains("強欲の指輪装備"))
                            unlockedEvents.Add("強欲の指輪装備");
                    }
                }
                // 強欲の指輪を外す
                else if (key.KeyChar == '2' && greedRingEquipped)
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n\n強欲の指輪を外しますか？ [Y/N]");
                    Console.ResetColor();

                    var confirm = Console.ReadKey(true);
                    if (confirm.Key == ConsoleKey.Y)
                    {
                        greedRingEquipped = false;
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine("\n\n強欲の指輪を外した...");
                        Console.WriteLine("オーラが消えていく...");
                        Console.ResetColor();
                        Thread.Sleep(2000);
                    }
                }
                // 悪魔のコイン使用
                else if (key.KeyChar == '3' && hasDevilCoin && !devilCoinActive)
                {
                    UseDevilCoin();
                }
                // 血塗られたお守り装備/解除
                else if (key.KeyChar == '4' && hasBloodAmulet)
                {
                    ToggleBloodAmulet();
                }
                // 死神の指輪装備/解除
                else if (key.KeyChar == '5' && hasDeathRing)
                {
                    ToggleDeathRing();
                }
                // 時を刻む懐中時計装備/解除
                else if (key.KeyChar == '6' && hasTimeClock)
                {
                    ToggleTimeClock();
                }
                // 禁断の水晶玉使用
                else if (key.KeyChar == '7' && hasOracleBall)
                {
                    UseOracleBall();
                }
                // 🆕 リハビリ券使用
                else if (key.KeyChar == '8' && itemInventory["返済猶予券"] > 0)
                {
                    UseRehabTicket();
                }
                // 全装備解除
                else if (key.KeyChar == '9')
                {
                    UnequipAll();
                }
            }
        }

        // ========== 悪魔のコイン使用 ==========
        static void UseDevilCoin()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n⚠ 悪魔のコインを使用しますか？ ⚠\n");
            Console.WriteLine("次回は100%勝利");
            Console.WriteLine("その後5回は100%敗北");
            Console.WriteLine("\n本当に使用しますか？ [Y/N]");
            Console.ResetColor();

            var key = Console.ReadKey(true);
            if (key.Key == ConsoleKey.Y)
            {
                devilCoinActive = true;
                devilCoinWin = false;
                devilCoinCurse = 0;

                Console.Clear();
                for (int i = 0; i < 5; i++)
                {
                    Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                    Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                    Console.Clear();
                    Console.WriteLine("\n\n\n");
                    Console.WriteLine("    💀 悪魔のコインが輝く... 💀");
                    Thread.Sleep(300);
                }

                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n悪魔のコインを使用した！");
                Console.WriteLine("次回は必ず勝つ...しかし...");
                Console.ResetColor();
                Thread.Sleep(2500);
            }
        }

        // ========== 血塗られたお守り装備/解除 ==========
        static void ToggleBloodAmulet()
        {
            if (bloodAmuletEquipped)
            {
                bloodAmuletEquipped = false;
                bloodAmuletLoses = 0;
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n血塗られたお守りを外した...");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            else
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n⚠ 血塗られたお守りを装備しますか？ ⚠\n");
                Console.WriteLine("当たり確率が2倍");
                Console.WriteLine("3回負けるとBAD END");
                Console.WriteLine("\n本当に装備しますか？ [Y/N]");
                Console.ResetColor();

                var key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.Y)
                {
                    bloodAmuletEquipped = true;
                    bloodAmuletLoses = 0;

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine("\n\n血塗られたお守りを装備した...");
                    Console.WriteLine("血の匂いがする...");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                }
            }
        }

        // ========== 死神の指輪装備/解除 ==========
        static void ToggleDeathRing()
        {
            if (deathRingEquipped)
            {
                deathRingEquipped = false;
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n死神の指輪を外した...");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            else
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n⚠ 死神の指輪を装備しますか？ ⚠\n");
                Console.WriteLine("勝利時の獲得金×10倍");
                Console.WriteLine("敗北時-1000G（強制）");
                Console.WriteLine("\n本当に装備しますか？ [Y/N]");
                Console.ResetColor();

                var key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.Y)
                {
                    deathRingEquipped = true;

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n\n死神の指輪を装備した...");
                    Console.WriteLine("冷たい金属が指に食い込む...");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                }
            }
        }

        // ========== 時を刻む懐中時計装備/解除 ==========
        static void ToggleTimeClock()
        {
            if (timeClockEquipped)
            {
                timeClockEquipped = false;
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n時を刻む懐中時計を外した...");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
            else
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n⚠ 時を刻む懐中時計を装備しますか？ ⚠\n");
                Console.WriteLine("GOD MODE持続+5回");
                Console.WriteLine("1回転3秒以内に決定必須");
                Console.WriteLine("\n本当に装備しますか？ [Y/N]");
                Console.ResetColor();

                var key = Console.ReadKey(true);
                if (key.Key == ConsoleKey.Y)
                {
                    timeClockEquipped = true;

                    // 🆕 GOD MODE追加
                    if (!godMode)
                    {
                        godMode = true;
                        godModeRemaining = 5;
                    }
                    else
                    {
                        godModeRemaining += 5;
                    }

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine("\n\n時を刻む懐中時計を装備した...");
                    Console.WriteLine("カチ...カチ...カチ...");
                    Thread.Sleep(1500);

                    Console.ForegroundColor = ConsoleColor.Magenta;
                    Console.WriteLine("\n⏰ GOD MODE +5回 発動！");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                }
            }
        }

        // ========== 禁断の水晶玉使用 ==========
        static void UseOracleBall()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Blue;
            Console.WriteLine("\n\n禁断の水晶玉を使用しますか？\n");
            Console.WriteLine("次回の出目を予知できる");
            Console.WriteLine("ただし50%の確率で没収される");
            Console.WriteLine("\n本当に使用しますか？ [Y/N]");
            Console.ResetColor();

            var key = Console.ReadKey(true);
            if (key.Key == ConsoleKey.Y)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n\n水晶玉が輝く...");
                Thread.Sleep(1500);

                // 50%没収判定
                if (rand.Next(2) == 0)
                {
                    hasOracleBall = false;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n水晶玉が砕け散った！");
                    Console.WriteLine("没収された...");
                    Console.ResetColor();
                    Thread.Sleep(2500);
                }
                else
                {
                    // 次回の出目を予知
                    oracleBallPrediction = rand.Next(symbols.Length);
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n未来が見える...");
                    Console.WriteLine($"\n次回の出目: シンボル#{oracleBallPrediction}");
                    Console.ResetColor();
                    Thread.Sleep(3000);
                }
            }
        }

        // ========== 全装備解除 ==========
        static void UnequipAll()
        {
            bloodAmuletEquipped = false;
            deathRingEquipped = false;
            timeClockEquipped = false;
            greedRingEquipped = false;
            bloodAmuletLoses = 0;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n\n全ての装備を外しました");
            Console.ResetColor();
            Thread.Sleep(1500);
        }

        // ========== ミッション関連 ==========
        static void ShowUncompletedMissions()
        {
            var uncompleted = missions.Where(m => !m.Completed && m.Name != "???").Take(2).ToList();
            if (uncompleted.Any())
            {
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n【進行中ミッション】");
                foreach (var mission in uncompleted)
                {
                    Console.WriteLine($"  ◆ {mission.Name}: {mission.Description}");
                }
                Console.ResetColor();
            }
        }

        static void ShowAllMissions()
        {
            missionOpenCount++;

            // 読んでる？ミッション達成チェック
            if (missionOpenCount == 10)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("         隠しミッション発見！");
                Console.WriteLine("         「読んでる？」");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("\n    「気づいてたよ」");
                Thread.Sleep(1500);
                Console.WriteLine("    「ずっと見てたんだね」");
                Thread.Sleep(1500);
                Console.WriteLine("    「…ねえ、ミッション一覧って面白い？」");
                Thread.Sleep(1500);
                Console.WriteLine("\n    君はゲームを、ゲームとして楽しんでいる。それは…正しいことだ");
                Console.ResetColor();
                Thread.Sleep(4000);
            }

            int pageSize = 15; // 1ページに表示する数
            int page = 0;
            int totalPages = (int)Math.Ceiling(missions.Count / (double)pageSize);

            while (true)
            {
                Console.Clear();
                DrawTitle();
                Console.WriteLine($"\n【ミッション一覧】  {page + 1}/{totalPages}ページ\n");

                int start = page * pageSize;
                int end = Math.Min(start + pageSize, missions.Count);

                for (int i = start; i < end; i++)
                {
                    var mission = missions[i];
                    if (mission.Completed)
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        if (mission.Reward > 0)
                            Console.WriteLine($"✓ {mission.Name}: {mission.Description} (報酬: {mission.Reward}G) [達成済み]");
                        else
                            Console.WriteLine($"✓ {mission.Name}: {mission.Description} [達成済み]");
                    }
                    else
                    {
                        if (mission.Name == "???")
                        {
                            Console.ForegroundColor = ConsoleColor.DarkMagenta;
                            Console.WriteLine($"  ??? : ??? (報酬: ???)");
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.White;
                            if (mission.Reward > 0)
                                Console.WriteLine($"  {mission.Name}: {mission.Description} (報酬: {mission.Reward}G)");
                            else
                                Console.WriteLine($"  {mission.Name}: {mission.Description}");
                        }
                    }
                    Console.ResetColor();
                }

                Console.WriteLine("\n");
                if (page > 0)
                    Console.WriteLine("  [←] 前のページ");
                if (page < totalPages - 1)
                    Console.WriteLine("  [→] 次のページ");
                Console.WriteLine("  [0] 戻る");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);

                if (key.Key == ConsoleKey.LeftArrow && page > 0)
                    page--;
                else if (key.Key == ConsoleKey.RightArrow && page < totalPages - 1)
                    page++;
                else if (key.KeyChar == '0')
                    break;
            }
            // ShowAllMissions() の末尾、2つのブロックをこう置き換える

            // 中毒度増加（ミッション閲覧のごほうび的に1回だけ、少量）
            // ※そもそもミッション開閉で上げたくないなら丸ごと削除でOK
            if (addictionLevel < 100)
            {
                addictionLevel = Math.Min(100, addictionLevel + rand.Next(1, 3));
            }




            CheckMissions();
        }
        // ========== ミッション達成チェック ==========
        static void CheckMissions()
        {
            for (int idx = 0; idx < missions.Count; idx++)
            {
                var mission = missions[idx];
                if (!mission.Completed && mission.CheckComplete != null && mission.CheckComplete())
                {
                    mission.Completed = true;

                    // 隠しミッションの名前解放（インデックスで判定）
                    if (mission.Name == "???")
                    {
                        switch (idx)
                        {
                            case 40: // 伝説のギャンブラーの次
                                mission.Name = "負け続ける者";
                                mission.Description = "累計負け100回";
                                break;
                            case 41:
                                mission.Name = "無敵の男";
                                mission.Description = "20連勝達成";
                                break;
                            case 42:
                                mission.Name = "666の刻印";
                                mission.Description = "所持金がピッタリ6666G";
                                break;
                            case 43:
                                mission.Name = "運命の回転";
                                mission.Description = "総回転数がピッタリ777回";
                                break;
                            case 44:
                                mission.Name = "ぼくがかんがえた、さいきょうのはいじん";
                                mission.Description = "全呪いアイテムを入手";
                                break;
                            case 45:
                                mission.Name = "真の覇者";
                                mission.Description = "所持金10000G以上かつ777を3回";
                                break;
                        }
                    }

                    // 達成演出（???のまま解放できなかった場合は表示しない）
                    if (mission.Name != "???")
                    {
                        if (mission.Reward > 0) money += mission.Reward;

                        // バッジの種類を報酬額で決定
                        bool isHidden = idx >= 40;
                        bool isLegend = mission.Name == "伝説のギャンブラー";

                        Console.Clear();

                        if (isLegend)
                        {
                            // 伝説バッジ（超豪華）
                            for (int f = 0; f < 6; f++)
                            {
                                Console.Clear();
                                Console.ForegroundColor = f % 2 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;
                                Console.BackgroundColor = f % 2 == 0 ? ConsoleColor.DarkYellow : ConsoleColor.Black;
                                Console.WriteLine("\n\n");
                                Console.WriteLine("  ╔══════════════════════════════════════════════════════╗");
                                Console.WriteLine("  ║                                                      ║");
                                Console.WriteLine("  ║   ★ ★ ★   全ミッション達成！！！   ★ ★ ★      ║");
                                Console.WriteLine("  ║        あなたは伝説のギャンブラーだ                  ║");
                                Console.WriteLine("  ║                                                      ║");
                                Console.WriteLine("  ╚══════════════════════════════════════════════════════╝");
                                Console.ResetColor();
                                Thread.Sleep(300);
                            }
                            Thread.Sleep(1000);
                        }
                        else if (isHidden)
                        {
                            // 隠しミッションバッジ
                            Console.BackgroundColor = ConsoleColor.DarkMagenta;
                            Console.ForegroundColor = ConsoleColor.White;
                            Console.WriteLine("\n\n");
                            Console.WriteLine("  ╔══════════════════════════════════════════════╗");
                            Console.WriteLine("  ║                                              ║");
                            Console.WriteLine("  ║   ？？？  隠しミッション解放！  ？？？      ║");
                            Console.WriteLine($"  ║   【{mission.Name.PadRight(20)}】        ║");
                            Console.WriteLine($"  ║   {mission.Description.PadRight(30)}      ║");
                            if (mission.Reward > 0)
                                Console.WriteLine($"  ║   報酬: +{mission.Reward,6}G                            ║");
                            Console.WriteLine("  ║                                              ║");
                            Console.WriteLine("  ╚══════════════════════════════════════════════╝");
                            Console.ResetColor();
                        }
                        else if (mission.Reward >= 3000)
                        {
                            // 金バッジ
                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine("\n\n");
                            Console.WriteLine("  ╔════════════════════════════════════════╗");
                            Console.WriteLine("  ║  🏆  MISSION COMPLETE  🏆             ║");
                            Console.WriteLine($"  ║  ★ {mission.Name.PadRight(24)} ★   ║");
                            Console.WriteLine($"  ║    {mission.Description.PadRight(28)}   ║");
                            if (mission.Reward > 0)
                                Console.WriteLine($"  ║    報酬: +{mission.Reward,6}G                    ║");
                            Console.WriteLine("  ╚════════════════════════════════════════╝");
                            Console.ResetColor();
                        }
                        else
                        {
                            // 通常バッジ
                            Console.ForegroundColor = ConsoleColor.Cyan;
                            Console.WriteLine("\n\n");
                            Console.WriteLine("  ┌──────────────────────────────────────┐");
                            Console.WriteLine("  │  ✓ ミッション達成                    │");
                            Console.WriteLine($"  │  「{mission.Name.PadRight(22)}」  │");
                            if (mission.Reward > 0)
                                Console.WriteLine($"  │   報酬: +{mission.Reward,5}G                      │");
                            Console.WriteLine("  └──────────────────────────────────────┘");
                            Console.ResetColor();
                        }

                        Thread.Sleep(isLegend ? 500 : 1800);

                        // 伝説のギャンブラー追加演出
                        if (isLegend)
                        {
                            Console.Clear();
                            Console.ForegroundColor = ConsoleColor.DarkGray;
                            TypewriterEffect("    ベル「...全部、達成したの？」", 50);
                            Thread.Sleep(2000);
                            TypewriterEffect("\n\n    ...沈黙...", 50);
                            Thread.Sleep(2000);
                            Console.ForegroundColor = ConsoleColor.Cyan;
                            TypewriterEffect("\n\n    ベル「...すごいわね」", 50);
                            Thread.Sleep(2000);
                            TypewriterEffect("\n\n    ベル「...本当に」", 50);
                            Thread.Sleep(3000);

                            Console.Clear();
                            Console.ForegroundColor = ConsoleColor.Yellow;
                            Console.WriteLine("\n\n\n");
                            Console.WriteLine("    ★ 称号解放 ★");
                            Console.WriteLine("    「伝説のギャンブラー」");
                            Console.ResetColor();
                            Thread.Sleep(3000);

                            if (!unlockedEvents.Contains("伝説のギャンブラー"))
                                unlockedEvents.Add("伝説のギャンブラー");
                        }

                        Thread.Sleep(isLegend ? 2500 : 0);
                    }
                }
            }
        }


        // ========== ランキング関連 ==========
        static void SaveRanking()
        {
            rankings.Add(new HighScore
            {
                Name = playerName,
                Money = maxMoney,
                Spins = totalSpins,
                Date = DateTime.Now
            });

            try
            {
                using (StreamWriter sw = new StreamWriter("rankings.txt", true))
                {
                    sw.WriteLine($"{playerName},{maxMoney},{totalSpins},{DateTime.Now:yyyy-MM-dd}");
                }
            }
            catch { }
        }

        static void LoadRankings()
        {
            try
            {
                if (File.Exists("rankings.txt"))
                {
                    string[] lines = File.ReadAllLines("rankings.txt");
                    foreach (string line in lines)
                    {
                        string[] parts = line.Split(',');
                        if (parts.Length >= 4)
                        {
                            rankings.Add(new HighScore
                            {
                                Name = parts[0],
                                Money = int.Parse(parts[1]),
                                Spins = int.Parse(parts[2]),
                                Date = DateTime.Parse(parts[3])
                            });
                        }
                    }
                }
            }
            catch { }
        }

        static void ShowRankings()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("╔═══════════════════════════════════╗");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("║         ★ ランキング ★          ║");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("╚═══════════════════════════════════╝");
            Console.ResetColor();

            Console.WriteLine("\n【歴代TOP10】\n");

            var sorted = rankings.OrderByDescending(r => r.Money).Take(10).ToList();

            if (sorted.Count == 0)
            {
                Console.WriteLine("  まだ記録がありません");
            }
            else
            {
                for (int i = 0; i < sorted.Count; i++)
                {
                    var rank = sorted[i];
                    Console.ForegroundColor = i < 3 ? ConsoleColor.Yellow : ConsoleColor.White;
                    Console.WriteLine($"  {i + 1}位: {rank.Name.PadRight(12)} {rank.Money}G ({rank.Spins}回転) {rank.Date:yyyy/MM/dd}");
                    Console.ResetColor();
                }
            }

            Console.WriteLine("\n\n【あなたの記録】");
            Console.WriteLine($"  最高所持金: {maxMoney}G");
            Console.WriteLine($"  最大連勝: {maxConsecutiveWins}回");
            Console.WriteLine($"  777揃い: {total777Count}回");

            Console.WriteLine("\n\n何かキーを押して戻る...");
            Console.ReadKey(true);
        }

        // ========== コレクション ==========
        static void ShowCollection()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("╔═══════════════════════════════════╗");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("║       ♦ コレクション ♦          ║");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("╚═══════════════════════════════════╝");
            Console.ResetColor();

            Console.WriteLine("\n【解放済み絵柄】");
            Console.WriteLine($"  {unlockedSymbols.Count}/8 種類\n");

            string[] allSymbols = { "スライム", "ゴーレム", "777", "スマイル", "スター", "サークル", "ハッシュ", "ドル" };

            foreach (var sym in allSymbols)
            {
                if (unlockedSymbols.Contains(sym))
                {
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"  ✓ {sym}");
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.WriteLine($"  ? ???");
                }
                Console.ResetColor();
            }

            Console.WriteLine("\n\n【イベントCGギャラリー】");
            Console.WriteLine($"  {unlockedEvents.Count} 種類解放\n");

            foreach (var evt in unlockedEvents)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"  ★ {evt}");
                Console.ResetColor();
            }

            if (unlockedEvents.Count == 0)
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("  まだイベントがありません");
                Console.ResetColor();
            }

            Console.WriteLine("\n\n何かキーを押して戻る...");
            Console.ReadKey(true);
        }

        static void UnlockSymbol()
        {
            string[] allSymbols = { "スライム", "ゴーレム", "777", "スマイル", "スター", "サークル", "ハッシュ", "ドル" };
            var locked = allSymbols.Where(s => !unlockedSymbols.Contains(s)).ToList();

            if (locked.Count > 0 && rand.Next(100) < 30)
            {
                var newSymbol = locked[rand.Next(locked.Count)];
                unlockedSymbols.Add(newSymbol);

                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine($"\n\n  ✨ 新しい絵柄を解放！「{newSymbol}」");
                Console.ResetColor();
                Thread.Sleep(2000);
            }
        }

        // ========== 描画関連 ==========
        static void DrawTitle()
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("╔═══════════════════════════════════╗");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("║      FEWJS  CASINO  SLOT!!!        ║");
            Console.WriteLine("║                                   ║");
            Console.WriteLine("╚═══════════════════════════════════╝");
            Console.ResetColor();
        }

        static void DrawReels(int[] reels)
        {
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("    ┌───────────┬───────────┬───────────┐");
            for (int row = 0; row < 5; row++)
            {
                Console.Write("    │ ");
                for (int col = 0; col < 3; col++)
                {
                    Console.Write(symbols[reels[col]][row]);
                    Console.Write(" │ ");
                }
                Console.WriteLine();
            }
            Console.WriteLine("    └───────────┴───────────┴───────────┘");
            Console.ResetColor();
        }

        // ========== アニメーション ==========
        static void MegaWinAnimation(string amount)
        {
            for (int i = 0; i < 5; i++)
            {
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Yellow : ConsoleColor.Red;
                Console.WriteLine("  ★★★★★★★★★★★★★★★★★★★★");
                Console.WriteLine("  ★                                    ★");
                Console.WriteLine($"  ★    🎊 超激レア！777揃い！🎊    ★");
                Console.WriteLine($"  ★         {amount.PadLeft(10)}           ★");
                Console.WriteLine("  ★                                    ★");
                Console.WriteLine("  ★★★★★★★★★★★★★★★★★★★★");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                for (int j = 0; j < 6; j++) Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("  ★★★★★★★★★★★★★★★★★★★★");
            Console.WriteLine("  ★                                    ★");
            Console.WriteLine($"  ★    🎊 超激レア！777揃い！🎊    ★");
            Console.WriteLine($"  ★         {amount.PadLeft(10)}           ★");
            Console.WriteLine("  ★                                    ★");
            Console.WriteLine("  ★★★★★★★★★★★★★★★★★★★★");
            Console.ResetColor();
        }

        static void BigWinAnimation(string amount)
        {
            for (int i = 0; i < 4; i++)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"     ◆◆◆ 大当たり！{amount} ◆◆◆");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Thread.Sleep(150);
            }
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"     ◆◆◆ 大当たり！{amount} ◆◆◆");
            Console.ResetColor();
        }

        static void SmallWinAnimation(string amount)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"        ◇ 当たり！{amount} ◇");
            Console.ResetColor();
        }

        static void LoseAnimation()
        {
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("           × ハズレ… ×");
            Console.ResetColor();
        }

        static void ReachEffect(int[] result)
        {
            Console.Clear();
            DrawTitle();
            Console.WriteLine("\n");

            int[] tempResult = new int[] { result[0], result[1], result[0] };
            DrawReels(tempResult);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n        ◆◆◆ リーチ！！ ◆◆◆");
            Console.WriteLine("           左右が揃った！");
            Console.ResetColor();
            Thread.Sleep(1200);

            for (int i = 0; i < 10; i++)
            {
                tempResult[1] = rand.Next(symbols.Length);
                Console.Clear();
                DrawTitle();
                Console.WriteLine("\n");
                DrawReels(tempResult);
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n        ◆◆◆ リーチ！！ ◆◆◆");
                Console.WriteLine("           左右が揃った！");
                Console.ResetColor();
                Thread.Sleep(150 + i * 60);
            }
        }

        static void DoubleUpChallenge(ref int winAmount)
        {
            Console.WriteLine("\n");
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("  ダブルアップチャレンジ発生！");
            Console.WriteLine($"  現在の獲得金: {winAmount}G");
            Console.WriteLine("  ━━━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("  成功で2倍、失敗で0G");
            Console.WriteLine("  挑戦しますか？ [Y/N]");
            Console.ResetColor();

            var choice = Console.ReadKey(true);
            if (choice.Key == ConsoleKey.Y)
            {
                Console.WriteLine("\n\n  コインを投げる...");
                Thread.Sleep(1500);

                for (int i = 0; i < 5; i++)
                {
                    Console.Write(i % 2 == 0 ? "\r  ◆ 表 " : "\r  ◇ 裏 ");
                    Thread.Sleep(300);
                }

                bool success = rand.Next(2) == 0;

                Thread.Sleep(500);
                Console.WriteLine();

                if (success)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("\n  ★★★ 成功！2倍獲得！ ★★★");
                    int bonus = winAmount; // 増加分のみ追加（呼び出し元で既に加算済み）
                    winAmount *= 2;
                    money += bonus;
                    Console.WriteLine($"  獲得金: {winAmount}G");
                    Console.ResetColor();
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n  × 失敗...獲得金が消えた ×");
                    money -= winAmount;
                    winAmount = 0;
                    Console.ResetColor();
                }
                Thread.Sleep(2000);
            }
        }

        // ========== イベント系（既存コードより） ==========
        static void GodModeActivation()
        {
            godMode = true;
            godModeRemaining = 10;
            godModeActivateCount++;

            Console.Clear();
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Magenta : ConsoleColor.White;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★★");
                Console.WriteLine("    ★                                    ★");
                Console.WriteLine("    ★      GOD MODE 発動！！！          ★");
                Console.WriteLine("    ★                                    ★");
                Console.WriteLine("    ★   10回転、全ての配当が2倍！      ★");
                Console.WriteLine("    ★                                    ★");
                Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★★");
                Console.ResetColor();
                Thread.Sleep(300);
            }
            Thread.Sleep(2000);

            if (!unlockedEvents.Contains("GOD MODE"))
                unlockedEvents.Add("GOD MODE");
        }

        static void LuckyTimeActivation()
        {
            luckyTimeActive = true;
            luckyTimeRemaining = 5;

            Console.Clear();
            for (int i = 0; i < 4; i++)
            {
                Console.Clear();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Yellow : ConsoleColor.White;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆");
                Console.WriteLine("    ☆                              ☆");
                Console.WriteLine("    ☆   ラッキータイム突入！      ☆");
                Console.WriteLine("    ☆                              ☆");
                Console.WriteLine("    ☆   5回転、当たりやすい！     ☆");
                Console.WriteLine("    ☆                              ☆");
                Console.WriteLine("    ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆");
                Console.ResetColor();
                Thread.Sleep(300);
            }
            Thread.Sleep(1500);
        }

        static void FreezeEffect()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("            画面が止まった...");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n          フ リ ー ズ 確 定 ！！！");
            Thread.Sleep(1500);

            Console.Clear();
            for (int i = 0; i < 6; i++)
            {
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Red : ConsoleColor.Yellow;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ■■■■■■■■■■■■■■■■■■■");
                Console.WriteLine("    ■                                ■");
                Console.WriteLine("    ■   フリーズ演出発動！！！      ■");
                Console.WriteLine("    ■                                ■");
                Console.WriteLine("    ■      777 確 定 ！！！         ■");
                Console.WriteLine("    ■                                ■");
                Console.WriteLine("    ■■■■■■■■■■■■■■■■■■■");
                Thread.Sleep(300);
                Console.Clear();
                Thread.Sleep(200);
            }
            Thread.Sleep(2000);
        }

        static void BlackSuitArrival()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n");
            Console.WriteLine("              コツ...");
            Console.WriteLine("              コツ...");
            Thread.Sleep(1500);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n    黒服の男たちが現れた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「金に困ってるようだな...」");
            Thread.Sleep(1500);
            Console.WriteLine("\n    「500G貸してやるよ」");
            Thread.Sleep(1500);
            Console.WriteLine("\n    「...ただし、20回転以内に返せよ」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    500Gを受け取った...");
            Console.ResetColor();
            Thread.Sleep(2000);
        }

        static void RandomConversationEvent()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n謎のおじさんが話しかけてきた...\n");
            Thread.Sleep(1500);

            string[] messages = {
            "「このスロット、実は設定というものがあってな...」",
            "「777を3回揃えると、黒服が来るって噂だぜ」",
            "「100Gを20回連続で賭けると...何かが起きるらしい」",
            "「借金は怖いぞ...返せなくなったら...」",
            "「強欲の指輪って...知ってるか？...知らないなら別にいい...」",
        };

            Console.WriteLine($"    {messages[rand.Next(messages.Length)]}");
            Thread.Sleep(3000);
            Console.WriteLine("\n    おじさんは去っていった...");
            Thread.Sleep(2000);
        }

        static void MysteriousWomanEvent()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    美しい女性が近づいてきた...", 55);
            Thread.Sleep(1800);

            // 状況によって登場セリフを変える
            string greeting;
            if (addictionLevel >= 70)
                greeting = "    「...また来てたのね」";
            else if (debt >= 5000)
                greeting = "    「大変そうね...受け取って」";
            else if (total777Count >= 3)
                greeting = "    「あなた...何かを持ってるわね」";
            else
                greeting = "    「あなた...運が良さそうね」";

            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n" + greeting, 55);
            Thread.Sleep(1800);
            TypewriterEffect("\n\n    「これを...受け取って」", 55);
            Thread.Sleep(1500);

            // ========== お小遣いをピンキリに ==========
            // 状況・運次第で大きく変わる
            int bonus;
            string bonusComment;
            int roll = rand.Next(100);

            if (roll < 5)
            {
                // 超レア: 大金
                bonus = rand.Next(3000, 8001);
                bonusComment = "    ...思いがけない大金だった";
            }
            else if (roll < 15)
            {
                // レア: まとまった額
                bonus = rand.Next(800, 2001);
                bonusComment = "    ...かなりの額だった";
            }
            else if (roll < 40)
            {
                // やや多め
                bonus = rand.Next(300, 801);
                bonusComment = "    ...そこそこの額だった";
            }
            else if (roll < 70)
            {
                // 普通
                bonus = rand.Next(100, 301);
                bonusComment = "";
            }
            else if (roll < 88)
            {
                // 少ない
                bonus = rand.Next(20, 101);
                bonusComment = "    ...少し、拍子抜けした";
            }
            else if (roll < 96)
            {
                // ほぼ意味なし
                bonus = rand.Next(1, 20);
                bonusComment = "    ...気持ちだけ受け取った";
            }
            else
            {
                // 借金中毒状態だと1Gもあり得る
                bonus = 1;
                bonusComment = "    ...1Gだった";
            }

            // 借金が多いとボーナス増加傾向
            if (debt >= 10000) bonus = (int)(bonus * 1.5);
            // 中毒度が高いと減少傾向
            if (addictionLevel >= 80) bonus = Math.Max(1, bonus / 2);

            money += bonus;

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"\n\n    {bonus:N0}G を受け取った！");
            Console.ResetColor();
            if (bonusComment != "")
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine(bonusComment);
                Console.ResetColor();
            }
            Thread.Sleep(1800);

            // ========== ヒントセリフ（内容もピンキリ） ==========
            string[] hints = {
                "    「この下には、黒服がいる...気をつけて」",
                "    「監視されている...」",
                "    「強欲の指輪には気をつけて...」",
                "    「幸運のコインは...本当に幸運を呼ぶのかしら...」",
                "    「借金は...あなたを壊すわ...」",
                "    「夢と現実の境目が、薄くなってるわ...」",
                "    「悪魔と取引してはダメ...絶対に」",
                "    「あの店の子...あなたのことを待ってるわよ」",
                "    「777は...偶然じゃないことがある」",
                "    「...次、いつ来るの？」",  // 少し怖い
                "    「...」",                  // 何も言わず去る
            };
            string hint = hints[rand.Next(hints.Length)];
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            TypewriterEffect("\n" + hint, 55);
            Thread.Sleep(2500);

            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    女性は微笑んで去っていった...", 55);
            Console.ResetColor();
            Thread.Sleep(2000);

            if (!unlockedEvents.Contains("謎の女性"))
                unlockedEvents.Add("謎の女性");
        }

        static void Devilmonster()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         悪魔の怪物 現る！");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);
            Console.WriteLine("\n\n    画面に悪魔の怪物が映し出された...");
            Thread.Sleep(2000);
            Console.WriteLine("\n    「お前の魂を賭けろ...」");
            Thread.Sleep(2000);
            int penalty = money / 2;
            money -= penalty;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"\n    悪魔の怪物に魂を奪われ、所持金が半分に減った... -{penalty}G");
            Console.ResetColor();
            Thread.Sleep(3000);
        }

        static void BlackSuitWarningEvent()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n");
            Console.WriteLine("              コツ...");
            Console.WriteLine("              コツ...");
            Thread.Sleep(1000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine(@"
        _______________
       |  ___________  |
       | |           | |
       | |  黒服が   | |
       | |  近づく   | |
       | |___________| |
       |_______________|

             ■■■
            ■■■■■
           ■■■■■■
            ■■■■■
           ■  ■  ■
          ■■■■■■■
         ■■■■■■■■■
            ■■■■■
            ■■  ■■
            ■■  ■■
           ■■■ ■■■");
            Thread.Sleep(2000);
            Console.WriteLine("\n\n       「調子に乗るなよ...」");
            Thread.Sleep(2000);
            Console.WriteLine("\n       黒服たちは去っていった...");
            Thread.Sleep(2000);
        }
        static void DebtCollectionEvent()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         借金取り立て発生！");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n    黒服たちがやってきた...");
            Thread.Sleep(2000);

            if (itemInventory["返済猶予券"] > 0)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n\n    返済猶予券を使用しますか？ [Y/N]");
                Console.ResetColor();
                var useTicket = Console.ReadKey(true);
                if (useTicket.Key == ConsoleKey.Y)
                {
                    itemInventory["返済猶予券"]--;
                    debtTurnsRemaining = 10;
                    money += 100;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("\n\n    返済猶予券を使用した！");
                    Console.WriteLine("    期限が10回延長され、100G獲得した！");
                    Console.ResetColor();
                    Thread.Sleep(3000);
                    return;
                }
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    [1] 過酷な労働で返済");
            Console.WriteLine("    [2] 楽に終わらせる");
            Console.ResetColor();
            Console.Write("\n選択 > ");

            var choice = Console.ReadKey(true);

            if (choice.KeyChar == '1')
            {
                LaborEnding();
            }
            else
            {
                ExecutionEnding();
            }
        }

        static void LaborEnding()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkBlue;
            Console.WriteLine("\n\n黒服たちに連行される...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("     あなたは見知らぬ施設に連れてこられた...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     過酷な労働が待っている...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     二度と自由な生活には戻れないだろう...");
            Thread.Sleep(3000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("              BAD END - 強制労働");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("BAD END"))
                unlockedEvents.Add("BAD END");
        }

        static void ExecutionEnding()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n黒服が静かに銃を取り出す...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.WriteLine("\n\n\n");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("     ================================");
            Console.WriteLine("          冷たい銃口が向けられた");
            Console.WriteLine("     ================================");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n     黒服「悪く思うなよ...」");
            Console.WriteLine("\n     銃口があなたのこめかみに押し当てられる...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n          カチッ...");
            Thread.Sleep(1500);

            Console.Clear();
            Console.WriteLine("\n\n\n");
            Console.WriteLine("           パァンッ！！！");
            Thread.Sleep(1000);

            Console.Clear();
            Console.WriteLine("\n\n\n");
            Console.WriteLine("     ================================");
            Console.WriteLine("              一発の銃声");
            Console.WriteLine("     ================================");
            Thread.Sleep(1500);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n     あなたは崩れ落ちた...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     意識が遠のいていく...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     ...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Black;
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("              GAME OVER");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("GAME OVER"))
                unlockedEvents.Add("GAME OVER");
        }

        // ========== 強欲の指輪関連 ==========
        static void GreedRingEquipAnimation()
        {
            Console.Clear();
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    💀💀💀💀💀💀💀💀💀💀💀💀💀");
                Console.WriteLine("    💀                              💀");
                Console.WriteLine("    💀    強欲の指輪 装備！       💀");
                Console.WriteLine("    💀                              💀");
                Console.WriteLine("    💀   邪悪なオーラが纏う...    💀");
                Console.WriteLine("    💀                              💀");
                Console.WriteLine("    💀💀💀💀💀💀💀💀💀💀💀💀💀");
                Console.ResetColor();
                Thread.Sleep(300);
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n指輪から黒い霧が溢れ出す...");
            Thread.Sleep(2000);
            Console.WriteLine("\n全身が邪悪なオーラに包まれた！");
            Thread.Sleep(2000);
            Console.WriteLine("\n\n...もっと...もっと賭けろ...");
            Thread.Sleep(2000);
            Console.ResetColor();
        }

        static void GreedWhisperEvent()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");

            string[] whispers = {
            "...もっと...もっと賭けろ...",
            "...全てを賭けるのだ...",
            "...欲望のままに...",
            "...恐れるな...賭け続けろ...",
            "...富を...無限の富を..."
        };

            Console.WriteLine($"    {whispers[rand.Next(whispers.Length)]}");
            Console.ResetColor();
            Thread.Sleep(2500);
        }

        static void GreedRingBadEnding()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         強欲の代償");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n指輪が激しく輝き始めた...");
            Thread.Sleep(2000);
            Console.WriteLine("\n黒い霧があなたを包み込む...");
            Thread.Sleep(2000);
            Console.WriteLine("\n\n「...我が糧となれ...」");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("     あなたの魂は指輪に吸い込まれた...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     強欲に溺れた者の末路...");
            Thread.Sleep(2000);
            Console.WriteLine("\n     二度と戻ることはない...");
            Thread.Sleep(3000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("          BAD END - 破滅への道");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("破滅への道"))
                unlockedEvents.Add("破滅への道");
        }

        static void GreedRingMegaWinAnimation(string amount)
        {
            for (int i = 0; i < 5; i++)
            {
                Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                Console.WriteLine("  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀");
                Console.WriteLine("  💀                                    💀");
                Console.WriteLine($"  💀    強欲の祝福！777揃い！×5倍   💀");
                Console.WriteLine($"  💀         {amount.PadLeft(10)}           💀");
                Console.WriteLine("  💀                                    💀");
                Console.WriteLine("  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                for (int j = 0; j < 6; j++) Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 6);
                Thread.Sleep(150);
            }
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀");
            Console.WriteLine("  💀                                    💀");
            Console.WriteLine($"  💀    強欲の祝福！777揃い！×5倍   💀");
            Console.WriteLine($"  💀         {amount.PadLeft(10)}           💀");
            Console.WriteLine("  💀                                    💀");
            Console.WriteLine("  💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀");
            Console.ResetColor();
        }

        static void GreedRingBigWinAnimation(string amount)
        {
            for (int i = 0; i < 4; i++)
            {
                Console.BackgroundColor = ConsoleColor.DarkRed;
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"     💀💀 大当たり×5倍！{amount} 💀💀");
                Thread.Sleep(200);
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Console.WriteLine(new string(' ', 50));
                Console.SetCursorPosition(0, Console.CursorTop - 1);
                Thread.Sleep(150);
            }
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"     💀💀 大当たり×5倍！{amount} 💀💀");
            Console.ResetColor();
        }

        static void GreedRingSmallWinAnimation(string amount)
        {
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"        💀 当たり×5倍！{amount} 💀");
            Console.ResetColor();
        }

        static void GreedRingLoseAnimation()
        {
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("           💀 ハズレ... -500G 💀");
            Console.ResetColor();
            Thread.Sleep(1000);
        }

        // ========== エンディング ==========
        static void AddictionBadEnding()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         中毒の末路");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n    あなたは...もう止まれない...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    カジノから出ることができない...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    レバーを引き続ける...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    何日も...何週間も...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    体が...動かなくなった...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    意識が...薄れていく...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    ...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("          BAD END - 中毒の虜");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("中毒の虜"))
                unlockedEvents.Add("中毒の虜");
        }

        // ========== 悪魔契約1 BADエンディング ==========
        static void DevilContract1BadEnding()
        {
            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         魂の回収");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n10回の勝利を果たした...");
            Thread.Sleep(2000);

            Console.WriteLine("\n...しかし...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    悪魔「契約通り...魂を頂こう...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    体が...動かない...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    魂が...引き抜かれていく...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.WriteLine("\n\n\n    ...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("          BAD END - 悪魔の契約");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("悪魔に魂を奪われる"))
                unlockedEvents.Add("悪魔に魂を奪われる");

            ShowEnding();
        }

        // ========== 悪魔契約2 時間切れエンディング ==========
        static void DevilContract2TimeUpEnding()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         時間切れ");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n時計の音が止まった...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    悪魔「時間だ...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔「完済できなかったな...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔「契約通り...魂を頂く...」");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("          BAD END - 時間との取引失敗");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("時間切れ"))
                unlockedEvents.Add("時間切れ");

            ShowEnding();
        }

        // ========== 悪魔契約1 成功 ==========
        static void DevilContract1Success()
        {
            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.DarkRed;
            TypewriterEffect("    10回目の勝利の瞬間...", 60);
            Thread.Sleep(2000);

            Console.Clear();
            for (int f = 0; f < 5; f++)
            {
                Console.Clear();
                Console.ForegroundColor = f % 2 == 0 ? ConsoleColor.Red : ConsoleColor.DarkRed;
                Console.BackgroundColor = f % 2 == 0 ? ConsoleColor.Black : ConsoleColor.DarkRed;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("  ╔══════════════════════════════════════╗");
                Console.WriteLine("  ║                                      ║");
                Console.WriteLine("  ║    💀  魂の担保  達成  💀           ║");
                Console.WriteLine("  ║    10連勝 — 契約履行               ║");
                Console.WriteLine("  ║                                      ║");
                Console.WriteLine("  ╚══════════════════════════════════════╝");
                Console.ResetColor();
                Thread.Sleep(280);
            }
            Thread.Sleep(800);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    静寂...", 80);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    悪魔「...見事だ」", 60);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    悪魔「10連勝...約束は守られた」", 60);
            Thread.Sleep(2500);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            TypewriterEffect("    悪魔「だが...魂を返すとは言っていない」", 60);
            Thread.Sleep(3000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...笑い声が遠ざかる...", 60);
            Thread.Sleep(3000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ★ 契約1「魂の担保」— 達成 ★");
            Console.WriteLine("    報酬 +5000G");
            Console.ResetColor();
            money += 5000;
            Thread.Sleep(3000);
        }

        // ========== 悪魔契約2 成功 ==========
        static void DevilContract2Success()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★");
            Console.WriteLine("    ★                                ★");
            Console.WriteLine("    ★      借金完済成功！！！      ★");
            Console.WriteLine("    ★                                ★");
            Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    悪魔「...約束は守られた...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔「貴様は自由だ...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔の姿が消えていく...");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    ★ 悪魔との契約を成功させた！ ★");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("悪魔契約成功"))
                unlockedEvents.Add("悪魔契約成功");
        }

        // ========== TRUEエンディング ==========
        static void TrueEnding()
        {
            Console.Clear();
            Thread.Sleep(1000);

            // フェーズ1: 異変
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    いつものように、カジノへ向かった", 50);
            Thread.Sleep(2000);

            Console.WriteLine("\n");
            TypewriterEffect("    でも", 50);
            Thread.Sleep(1000);

            Console.WriteLine("\n");
            TypewriterEffect("    何かが違った", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ2: カジノの様子
            TypewriterEffect("    扉を開けると", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    カジノは静かだった", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    スロットの音も", 50);
            Thread.Sleep(800);
            Console.WriteLine("\n");
            TypewriterEffect("    客の声も", 50);
            Thread.Sleep(800);
            Console.WriteLine("\n");
            TypewriterEffect("    何もなかった", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ3: ベルとの再会
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("    カウンターに、ベルがいた", 50);
            Thread.Sleep(2000);
            Console.WriteLine("\n");
            TypewriterEffect("    いつもと違った", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    笑っていなかった", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("    ベル「...来てくれたのね」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「このカジノ...来月で閉まるの」", 50);
            Thread.Sleep(2500);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ4: 真実
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    知らなかった", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    ずっと通っていたのに", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    気づかなかった", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("    ベル「オーナーが...去年死んだの」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「キノコみたいな帽子が好きな...変な人だったけど」", 50);
            Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...優しい人だったわ」", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ4.5: キノコ男の正体
            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    そういえば", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    夢の中にいた", 50);
            Thread.Sleep(1000);
            Console.WriteLine("\n");
            TypewriterEffect("    キノコの帽子の男", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("    ベル「...あの人ね」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「死ぬ前に...夢の中でだけ会いに来てくれてたの」", 50);
            Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...あなたにも、会わせたかったのかもしれない」", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ5: 夢の種明かし
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    夢カジノのことを思い出した", 50);
            Thread.Sleep(2000);
            Console.WriteLine("\n");
            TypewriterEffect("    あの声", 50);
            Thread.Sleep(1000);
            Console.WriteLine("\n");
            TypewriterEffect("    あの言葉", 50);
            Thread.Sleep(1000);
            Console.WriteLine("\n");
            TypewriterEffect("    全部", 50);
            Thread.Sleep(1000);
            Console.WriteLine("\n");
            TypewriterEffect("    ベルの記憶だったんだ", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("    ベル「...ずっとひとりだったの」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でも...あなたが来てくれた」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「それだけで...よかった」", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ6: 最後の選択
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    何か言おうとした", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    でも言葉が出なかった", 50);
            Thread.Sleep(1500);
            Console.WriteLine("\n");
            TypewriterEffect("    代わりに", 50);
            Thread.Sleep(1000);

            Console.Clear();
            Thread.Sleep(500);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    [1] スロットを回す");
            Console.WriteLine("    [2] 何も言わずに座る");
            Console.WriteLine("    [3] ベルの隣に立つ");
            Console.ResetColor();

            Console.ReadKey(true);
            // どれを選んでも同じ結末

            Console.Clear();
            Thread.Sleep(500);

            // フェーズ7: エンディング
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("    2人で最後の夜を過ごした", 50);
            Thread.Sleep(2000);
            Console.WriteLine("\n");
            TypewriterEffect("    スロットの音だけが響いていた", 50);
            Thread.Sleep(2000);

            Console.Clear();
            Thread.Sleep(1000);

            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("    ベル「...また来てね♪」", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ...沈黙...", 50);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「待ってるから」", 50);
            Thread.Sleep(3000);

            Console.Clear();
            Thread.Sleep(2000);

            // フェーズ8: タイトル表示
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Cyan : ConsoleColor.White;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ═══════════════════════════════════════");
                Console.WriteLine("                                           ");
                Console.WriteLine("                 TRUE END                 ");
                Console.WriteLine("                                           ");
                Console.WriteLine("              - また来てね♪ -             ");
                Console.WriteLine("                                           ");
                Console.WriteLine("    ═══════════════════════════════════════");
                Console.ResetColor();
                Thread.Sleep(400);
            }

            Thread.Sleep(3000);

            // 永続GOD MODE解放
            godModePermanent = true;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ★ 隠し要素解放 ★");
            Console.WriteLine("    「永続GOD MODE」が解放されました");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains("TRUE END"))
                unlockedEvents.Add("TRUE END");

            ShowEnding();
        }
        static void ShowEnding()
        {
            SaveRanking();

            Console.Clear();

            var playTime = DateTime.Now - startTime;

            if (debt > 0)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ==============================");
                Console.WriteLine("              BAD  END");
                Console.WriteLine("    ==============================");
                Console.ResetColor();
                Thread.Sleep(2000);

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                if (addictionLevel >= 80)
                {
                    TypewriterEffect($"    {playerName}は気づけばまたカジノにいた", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    借金は膨れ上がり、止める気力もなかった", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    それでも、スロットのリールだけが輝いていた...", 50);
                }
                else if (devilContractActive)
                {
                    TypewriterEffect("    悪魔との契約は果たされなかった", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect($"\n\n    {playerName}が支払うべきものは、お金ではなかった", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    ...代償は静かに、確実に回収された", 50);
                }
                else if (debt >= 20000)
                {
                    TypewriterEffect($"    {playerName}の借金は限界を超えた", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    黒服たちが静かに近づいてきた...", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    カジノは今日も回り続ける", 50);
                }
                else
                {
                    TypewriterEffect($"    {playerName}はカジノを後にした", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    借金だけが残った...", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    また来る気がした", 50);
                }
                Console.ResetColor();
                Thread.Sleep(2500);

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("    ベル「...また来てね♪」", 50);
                Thread.Sleep(1500);
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    ...小さな声だった", 50);
                Console.ResetColor();
                Thread.Sleep(3000);
            }
            else if (money >= 5000 && debt == 0)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★");
                Console.WriteLine("    ★                                ★");
                Console.WriteLine("    ★          GOOD  END             ★");
                Console.WriteLine("    ★                                ★");
                Console.WriteLine("    ★★★★★★★★★★★★★★★★★★★");
                Console.ResetColor();
                Thread.Sleep(2000);

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                if (total777Count >= 5)
                {
                    TypewriterEffect($"    {playerName}は777を{total777Count}回揃えた", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    それは運なのか、才能なのか", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    本人にも、わからなかった...", 50);
                }
                else if (hasEverBorrowedMoney)
                {
                    TypewriterEffect($"    {playerName}は借金を完済し、カジノを後にした", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    あの夜、全てを失いかけた記憶は", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    今でも、薄く残っている...", 50);
                }
                else
                {
                    TypewriterEffect($"    {playerName}は大金を手に入れてカジノを後にした", 50);
                    Thread.Sleep(2000);
                    TypewriterEffect("\n\n    また来るだろう、という気がした", 50);
                }
                Console.ResetColor();
                Thread.Sleep(2500);

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Magenta;
                TypewriterEffect("    帰り際、ベルが声をかけてきた", 50);
                Thread.Sleep(2000);
                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("    ベル「おめでとう♪ よかったわね」", 50);
                Thread.Sleep(2000);
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    ...沈黙...", 50);
                Thread.Sleep(1500);
                Console.ForegroundColor = ConsoleColor.Cyan;
                if (addictionLevel >= 50)
                    TypewriterEffect("\n\n    ベル「...でも、もう来ないでね♪」", 50);
                else if (shopCloseWithoutBuyCount >= 20)
                    TypewriterEffect("\n\n    ベル「...また来るでしょ。わかってる♪」", 50);
                else
                    TypewriterEffect("\n\n    ベル「...また来てね♪ 待ってるから」", 50);
                Thread.Sleep(3000);
                Console.ResetColor();
                Thread.Sleep(3000);
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ===============================");
                Console.WriteLine("             NORMAL END");
                Console.WriteLine("    ===============================");
                Console.ResetColor();
                Console.WriteLine($"\n\n    {playerName}はカジノを後にした...");
                // ベルとの別れ
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Magenta;
                TypewriterEffect("    出口に向かうと、ベルが手を振っていた", 50);
                Thread.Sleep(2000);
                Console.WriteLine("\n");
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("    ベル「またいつでも来てね♪」", 50);
                Thread.Sleep(2000);
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    ...沈黙...", 50);
                Thread.Sleep(1500);
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("\n\n    ベル「...待ってるから」", 50);
                Thread.Sleep(3000);
                Console.ResetColor();
                Thread.Sleep(3000);
            }
            if (money >= 100000 && total777Count >= 3 && playTime.Hours >= 3)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    スロットが回る音...");
                Thread.Sleep(2000);
                Console.WriteLine("\n    ...デン");
                Thread.Sleep(2000);
                Console.WriteLine("\n    ...デン");
                Thread.Sleep(2000);
                Console.WriteLine("\n    ...デデン！");
                Thread.Sleep(2000);
                Console.WriteLine("\n    ...");
                Thread.Sleep(2000);
                Console.Clear();
                Console.WriteLine($"    俺は {playerName} ");
                Console.WriteLine("    伝説のスロッターだ！");
                Thread.Sleep(3000);
                Console.WriteLine("\n    777を3回も揃えた俺に");
                Console.WriteLine("    敵う奴なんていない！...と");
                Thread.Sleep(4000);
                Console.WriteLine("\n    思っていた時期が俺にもあった...");
                Thread.Sleep(4000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ...なあ..おい");
                Thread.Sleep(3000);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n    何だよ？");
                Thread.Sleep(2000);
                Console.WriteLine("\n    知らない男が話しかけてきた...");
                Thread.Sleep(3000);
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("\n    お前...とうとうココの禁忌に触れてなおかつ破った...");
                Thread.Sleep(4000);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n    何のことだ？");
                Thread.Sleep(2000);
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("\n    ここはな...選ばれし者しか来てはいけない場所なんだよ...");
                Thread.Sleep(4000);
                Console.WriteLine("\n    お前はその資格がなかった...");
                Thread.Sleep(4000);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n    そんなの関係ないだろ...");
                Thread.Sleep(3000);
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("\n    そうかもしれないな...");
                Thread.Sleep(3000);
                Console.WriteLine("\n    だがな...お前はもうここから出られない...");
                Thread.Sleep(4000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ダッ..ダッ..");
                Thread.Sleep(2000);
                Console.Clear();
                Console.WriteLine("黒服が現れた..!");
                Console.WriteLine("    奴を捕らえよ..!");
                Thread.Sleep(3000);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n    くそっ..逃げるしかない！");
                Thread.Sleep(3000);
                Console.WriteLine($"\n  {playerName}は今になって事態の深刻さに気づき ");
                Thread.Sleep(4000);
                Console.WriteLine("\n  さっきからずっと押していたボタンから手を放し、ここにきて席を立ったのだ...");
                Thread.Sleep(5000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    ===============================");
                Console.WriteLine("          BAD? END?? - 永遠の迷宮");
                Console.WriteLine("    ===============================");
                Console.WriteLine("    逃亡生活は順調かな？");
                Console.ResetColor();
            }
            ShowCredits();

            // ========== 統計画面（グラフ付き2カラム） ==========
            Console.Clear();
            int w = Math.Max(Console.WindowWidth, 80);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n  ╔══════════════════════════════════════════════════════════════════════════╗");
            Console.WriteLine("  ║                          P L A Y  S T A T S                            ║");
            Console.WriteLine("  ╚══════════════════════════════════════════════════════════════════════════╝");
            Console.ResetColor();

            // --- ヘルパー：バー計算はインライン ---

            // --- 左カラム：基本情報 ---
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐");
            Console.WriteLine("  │         基 本 情 報             │  │         戦 績 グ ラ フ          │");
            Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤");
            Console.ResetColor();

            // プレイヤー名・時間
            Console.Write($"  │  プレイヤー: {playerName,-18} │  │  ");
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write($"所持金  ");
            Console.ResetColor();
            int barLen = 20;
            int moneyBar = (int)((double)money / Math.Max(maxMoney, 1000) * barLen);
            moneyBar = Math.Clamp(moneyBar, 0, barLen);
            Console.ForegroundColor = money >= 1000 ? ConsoleColor.Green : ConsoleColor.Red;
            Console.Write("[" + new string('█', moneyBar) + new string('░', barLen - moneyBar) + "]");
            Console.ResetColor();
            Console.WriteLine("  │");

            Console.Write($"  │  プレイ時間: {FormatTimeSpan(playTime),-16} │  │  ");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write($"最高額  ");
            Console.ResetColor();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write("[" + new string('█', barLen) + "]");
            Console.ResetColor();
            Console.WriteLine($" {maxMoney,6}G│");

            Console.Write($"  │  最終所持金: {money,7:N0}G          │  │  ");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write($"回転数  ");
            Console.ResetColor();
            int spinBar = Math.Min(totalSpins * barLen / Math.Max(totalSpins, 100), barLen);
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write("[" + new string('█', spinBar) + new string('░', barLen - spinBar) + "]");
            Console.ResetColor();
            Console.WriteLine($"{totalSpins,4}回 │");

            Console.Write($"  │  最高所持金: {maxMoney,7:N0}G          │  │  ");
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.Write($"777回数 ");
            Console.ResetColor();
            int bar777 = Math.Min(total777Count * 4, barLen);
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.Write("[" + new string('█', bar777) + new string('░', barLen - bar777) + "]");
            Console.ResetColor();
            Console.WriteLine($"  x{total777Count,-3}  │");

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤");
            Console.ResetColor();

            // 勝敗
            int totalPlays = totalWinAmount + totalLoseAmount > 0 ? (totalSpins) : 1;
            Console.Write($"  │  総回転数:   {totalSpins,5}回            │  │  ");
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write("獲得額  ");
            Console.ResetColor();
            int winBar = totalWinAmount + totalLoseAmount > 0
                ? (int)((double)totalWinAmount / (totalWinAmount + totalLoseAmount) * barLen) : 0;
            winBar = Math.Clamp(winBar, 0, barLen);
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write("[" + new string('█', winBar) + new string('░', barLen - winBar) + "]");
            Console.ResetColor();
            Console.WriteLine("  │");

            Console.Write($"  │  777達成:    {total777Count,5}回            │  │  ");
            Console.ForegroundColor = ConsoleColor.Red;
            Console.Write("損失額  ");
            Console.ResetColor();
            int loseBar = barLen - winBar;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.Write("[" + new string('█', loseBar) + new string('░', barLen - loseBar) + "]");
            Console.ResetColor();
            Console.WriteLine("  │");

            Console.Write($"  │  最大連勝:   {maxConsecutiveWins,5}回            │  │  ");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write("中毒度  ");
            Console.ResetColor();
            int addBar = addictionLevel * barLen / 100;
            var addColor = addictionLevel < 40 ? ConsoleColor.Green
                         : addictionLevel < 70 ? ConsoleColor.Yellow : ConsoleColor.Red;
            Console.ForegroundColor = addColor;
            Console.Write("[" + new string('█', addBar) + new string('░', barLen - addBar) + "]");
            Console.ResetColor();
            Console.WriteLine($" {addictionLevel,3}%  │");

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("  ├─────────────────────────────────┤  ├─────────────────────────────────┤");
            Console.ResetColor();

            // 収支
            int netProfit = money - 1000;
            Console.Write($"  │  総獲得額:  {totalWinAmount,8:N0}G        │  │  ");
            if (netProfit >= 0)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write($"★ 純利益: +{netProfit:N0}G");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write($"▼ 純損失:  {-netProfit:N0}G");
            }
            Console.ResetColor();
            Console.WriteLine("".PadRight(Math.Max(0, 17 - netProfit.ToString().Length)) + "  │");

            Console.Write($"  │  総損失額:  {totalLoseAmount,8:N0}G        │  │  ");
            int completedM = missions.Count(m => m.Completed);
            int missionBar = missions.Count > 0 ? completedM * barLen / missions.Count : 0;
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write($"実績 [{new string('█', missionBar)}{new string('░', barLen - missionBar)}]");
            Console.ResetColor();
            Console.WriteLine("  │");

            Console.Write($"  │  最大借金:  {maxDebt,8:N0}G        │  │  ");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.Write($"  {completedM}/{missions.Count} ミッション達成");
            Console.ResetColor();
            Console.WriteLine("             │");

            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("  └─────────────────────────────────┘  └─────────────────────────────────┘");
            Console.ResetColor();

            // 解放コレクション
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"\n  絵柄: {unlockedSymbols.Count}/8  │  イベント: {unlockedEvents.Count}種  │  VIP訪問: {vipTotalVisits}回  │  地下訪問: {undergroundVisits}回");
            Console.ResetColor();

            // 強欲の指輪情報
            if (greedRingLoseCount > 0)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"  強欲の指輪: 負け{greedRingLoseCount}回 / 総損失 {greedRingLoseCount * 500:N0}G");
                Console.ResetColor();
            }

            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n\n  何かキーを押してタイトルに戻る...");
            Console.ResetColor();
            Console.ReadKey(true);
        }

        static void ShowCredits()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n\n\n");
            Console.WriteLine("         ━━━━━━━━━━━━━━━━━");
            Console.WriteLine("              STAFF ROLL");
            Console.WriteLine("         ━━━━━━━━━━━━━━━━━");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n         Game Director");
            Console.WriteLine("              Claude(AI)");
            Console.WriteLine("              Chisato Sugita");
            Console.WriteLine("              Rito Matsuhashi");
            Console.WriteLine("              Hinata Hase");
            Console.WriteLine("              Tomu Usui");
            Thread.Sleep(1500);

            Console.WriteLine("\n         Programming");
            Console.WriteLine("              C# / .NET");
            Thread.Sleep(1500);

            Console.WriteLine("\n         Special Thanks");
            Console.WriteLine("              Haru Setugetu");
            Thread.Sleep(1500);

            Console.WriteLine("\n\n━━━━━━━━━━━━━━━━━");
            Console.WriteLine("   _____                     ");
            Console.WriteLine("  |_   _|                    ");
            Console.WriteLine("    | |                      ");
            Console.WriteLine("    |_|hanks for playing      ");
            Console.WriteLine("\n\n━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(3000);
        }

        // ========== 血塗られたお守り BAD ENDING ==========
        static void BloodAmuletBadEnding()
        {
            Console.Clear();

            // 点滅演出
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸");
                Console.WriteLine("    🩸                          🩸");
                Console.WriteLine("    🩸    呪いの発動...      🩸");
                Console.WriteLine("    🩸                          🩸");
                Console.WriteLine("    🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸");
                Thread.Sleep(300);
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    お守りから血が溢れ出す...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    それはあなたの体を包み込む...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    動けない...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    息ができない...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    血の呪いに飲み込まれた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    意識が...遠のく...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    ...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("        ===============================");
            Console.WriteLine("          BAD END - 血の代償");
            Console.WriteLine("        ===============================");
            Console.ResetColor();
            Thread.Sleep(4000);

            if (!unlockedEvents.Contains("血の代償"))
                unlockedEvents.Add("血の代償");

            ShowEnding();
        }

        // ========== 中毒システム強化 ==========

        static void ShowAddictionMessage()
        {
            if (addictionLevel >= 21 && rand.Next(100) < 30)
            {
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine($"\n{addictionMessages[rand.Next(addictionMessages.Count)]}");
                Console.ResetColor();
                Thread.Sleep(1500);
            }
        }

        static void AddictionHallucinationEffect()
        {
            if (addictionLevel >= 61 && rand.Next(100) < 20)
            {
                Console.Clear();
                Console.CursorVisible = false;

                // 中毒度に応じて演出を変化
                if (addictionLevel >= 90)
                    AddictionWaveEffect_Chaos();
                else if (addictionLevel >= 75)
                    AddictionWaveEffect_Break();
                else
                    AddictionWaveEffect_Soft();

                Console.BackgroundColor = ConsoleColor.Black;
                Console.ForegroundColor = ConsoleColor.White;
                Console.Clear();
                Thread.Sleep(300);

                if (!unlockedEvents.Contains("中毒幻覚"))
                    unlockedEvents.Add("中毒幻覚");
            }
        }

        // ========== 中毒波形演出（61-74%）穏やかな揺れ ==========
        static void AddictionWaveEffect_Soft()
        {
            int width = 60;
            int height = 12;
            double speed = 0.18;
            int frames = 28;

            for (int frame = 0; frame < frames; frame++)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n");

                // sinグラフで揺れる波
                for (int row = 0; row < height; row++)
                {
                    // 各行のy座標を正規化 (-1.0 〜 1.0)
                    double y = 1.0 - 2.0 * row / (height - 1);

                    // 時間と行に応じてsinカーブ
                    for (int col = 0; col < width; col++)
                    {
                        double x = (double)col / width * Math.PI * 4;
                        double wave = Math.Sin(x - frame * speed)
                                    * Math.Cos(x * 0.3 + frame * 0.1);

                        // 波の山にいるか判定（閾値内なら描画）
                        double threshold = 0.12 + 0.04 * Math.Sin(frame * 0.2);
                        if (Math.Abs(wave - y) < threshold)
                        {
                            double brightness = 1.0 - Math.Abs(wave - y) / threshold;
                            Console.ForegroundColor = brightness > 0.6
                                ? ConsoleColor.White : ConsoleColor.DarkGray;
                            Console.Write("·");
                        }
                        else
                        {
                            Console.Write(" ");
                        }
                    }
                    Console.WriteLine();
                }

                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n    ...何かが見える...");
                Console.ResetColor();
                Thread.Sleep(55);
            }
        }

        // ========== 中毒波形演出（75-89%）崩れ始める ==========
        static void AddictionWaveEffect_Break()
        {
            int width = 64;
            int height = 14;
            double speed = 0.28;
            int frames = 35;

            for (int frame = 0; frame < frames; frame++)
            {
                Console.Clear();
                Console.WriteLine("\n");

                double chaos = (double)frame / frames; // 後半ほど乱れる

                for (int row = 0; row < height; row++)
                {
                    double y = 1.0 - 2.0 * row / (height - 1);

                    for (int col = 0; col < width; col++)
                    {
                        double x = (double)col / width * Math.PI * 6;

                        // sin + cos の合成波（リサジュー風）
                        double wave = Math.Sin(x - frame * speed)
                                    + 0.4 * Math.Cos(x * 1.7 + frame * 0.15)
                                    + 0.2 * Math.Sin(frame * 0.3) * chaos;
                        wave /= 1.6; // 正規化

                        // 後半はノイズを混入
                        if (chaos > 0.5 && rand.NextDouble() < chaos * 0.08)
                            wave += (rand.NextDouble() - 0.5) * 0.8;

                        double threshold = 0.14;
                        double dist = Math.Abs(wave - y);
                        if (dist < threshold)
                        {
                            double t = dist / threshold;
                            ConsoleColor color;
                            if (t < 0.25)
                                color = ConsoleColor.Yellow;
                            else if (t < 0.6)
                                color = ConsoleColor.DarkYellow;
                            else
                                color = ConsoleColor.DarkGray;
                            Console.ForegroundColor = color;

                            // 後半は文字が壊れる
                            if (chaos > 0.6 && rand.NextDouble() < chaos * 0.3)
                                Console.Write((char)(rand.Next(0x21, 0x7E)));
                            else
                                Console.Write("█");
                        }
                        else
                        {
                            Console.Write(" ");
                        }
                    }
                    Console.WriteLine();
                }

                ConsoleColor msgColor = chaos < 0.5 ? ConsoleColor.Yellow : ConsoleColor.Red;
                Console.ForegroundColor = msgColor;
                string[] msgs = { "    ...止められない...", "    ...もっと...", "    ...あと少しで...", "    ...どこかへ消えたい..." };
                Console.WriteLine(msgs[frame % msgs.Length]);
                Console.ResetColor();
                Thread.Sleep(45);
            }
        }

        // ========== 中毒波形演出（90%+）完全崩壊 ==========
        static void AddictionWaveEffect_Chaos()
        {
            int width = 70;
            int height = 16;
            int frames = 45;

            for (int frame = 0; frame < frames; frame++)
            {
                Console.Clear();
                Console.WriteLine();

                double t = (double)frame / frames;
                double amp = 1.0 + t * 1.5; // 振幅が時間とともに増大

                for (int row = 0; row < height; row++)
                {
                    double y = 1.0 - 2.0 * row / (height - 1);

                    for (int col = 0; col < width; col++)
                    {
                        double x = (double)col / width * Math.PI * 8;

                        // tanを含む複合波（発散する感じ）
                        double tanPart = Math.Tan(x * 0.08 + frame * 0.05);
                        tanPart = Math.Max(-1.5, Math.Min(1.5, tanPart)); // クランプ
                        double wave = (Math.Sin(x - frame * 0.35) * amp
                                     + 0.5 * Math.Cos(x * 2.1 - frame * 0.2)
                                     + 0.2 * tanPart) / (amp + 0.7);

                        // 強いノイズ
                        if (rand.NextDouble() < t * 0.15)
                            wave += (rand.NextDouble() - 0.5) * amp;

                        double threshold = 0.16 + t * 0.1;
                        double dist = Math.Abs(wave - y);

                        if (dist < threshold)
                        {
                            double brightness = 1.0 - dist / threshold;

                            // 色が暴れる
                            ConsoleColor[] colors = {
                                ConsoleColor.Red, ConsoleColor.DarkRed,
                                ConsoleColor.Magenta, ConsoleColor.DarkMagenta,
                                ConsoleColor.Yellow, ConsoleColor.White
                            };
                            int colorIdx = (int)(brightness * 3) + (frame % 2 == 0 ? 0 : 2);
                            Console.ForegroundColor = colors[Math.Min(colorIdx, colors.Length - 1)];

                            // 文字が崩れる
                            double glitchChance = t * 0.6;
                            if (rand.NextDouble() < glitchChance)
                            {
                                char[] glitchChars = { '▓', '▒', '░', '╬', '╪', '╫', '║', '═', '#', '%' };
                                Console.Write(glitchChars[rand.Next(glitchChars.Length)]);
                            }
                            else
                            {
                                Console.Write(brightness > 0.5 ? "█" : "▓");
                            }
                        }
                        else if (rand.NextDouble() < t * 0.04)
                        {
                            // 背景にもノイズ粒子
                            Console.ForegroundColor = ConsoleColor.DarkRed;
                            Console.Write('·');
                        }
                        else
                        {
                            Console.Write(" ");
                        }
                    }
                    Console.WriteLine();
                }

                // メッセージも崩れる
                Console.ForegroundColor = frame % 3 == 0 ? ConsoleColor.Red : ConsoleColor.DarkRed;
                string[] msgs = {
                    "    声が...聞こえる...",
                    "    誰かが...呼んでいる...",
                    "    これは...夢か...？",
                    "    画面が...歪んで見える...",
                    "    もうやめろ...",
                    "    タスケテ..."
                };
                string msg = msgs[frame % msgs.Length];
                // 後半はメッセージもノイズ化
                if (t > 0.7)
                {
                    char[] corrupted = msg.ToCharArray();
                    for (int i = 0; i < corrupted.Length; i++)
                        if (rand.NextDouble() < t * 0.4 && corrupted[i] != ' ')
                            corrupted[i] = (char)(rand.Next(0x21, 0x7E));
                    Console.WriteLine(new string(corrupted));
                }
                else
                {
                    Console.WriteLine(msg);
                }
                Console.ResetColor();
                Thread.Sleep(35);
            }
        }

        static void UseRehabTicket()
        {
            if (itemInventory["返済猶予券"] <= 0)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\nリハビリ券を持っていません");
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\nリハビリ券を使用しますか？ [Y/N]");
            Console.WriteLine("（中毒度-50、1枚消費）");
            Console.ResetColor();

            var key = Console.ReadKey(true);
            if (key.Key == ConsoleKey.Y)
            {
                itemInventory["返済猶予券"]--;
                addictionLevel = Math.Max(0, addictionLevel - 50);
                hasUsedRehab = true;

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    深呼吸をする...");
                Thread.Sleep(2000);
                Console.WriteLine("\n    心が落ち着いてきた...");
                Thread.Sleep(2000);
                Console.WriteLine("\n    少し...楽になった...");
                Thread.Sleep(2000);
                Console.WriteLine($"\n\n    中毒度: {addictionLevel}%");
                Console.ResetColor();
                Thread.Sleep(2000);
            }
        }
        // ========== 悪魔契約システム ==========

        static void DevilContractOfferEvent()
        {
            Console.Clear();

            // 画面を暗転
            for (int i = 0; i < 5; i++)
            {
                Console.Clear();
                Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.DarkRed;
                Thread.Sleep(300);
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    ================================");
            Console.WriteLine("         悪魔の囁き");
            Console.WriteLine("    ================================");
            Thread.Sleep(2000);

            Console.WriteLine("\n\n    突然、世界が静止した...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    音が消える...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    時が止まる...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    闇の中から声が響く...");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n    「...苦しいか...？」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...絶望しているか...？」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    「...力が...欲しいか...？」");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.DarkRed;
            Console.ForegroundColor = ConsoleColor.Black;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    巨大な影が現れた...");
            Thread.Sleep(2000);

            Console.WriteLine("\n    それは...悪魔だった...");
            Thread.Sleep(2000);

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈");
            Console.WriteLine("    😈                              😈");
            Console.WriteLine("    😈      悪魔が現れた！        😈");
            Console.WriteLine("    😈                              😈");
            Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈");
            Thread.Sleep(2000);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n\n");
            Console.WriteLine("    悪魔「我と契約を結ばぬか...？」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔「その苦しみ...我が救おう...」");
            Thread.Sleep(2000);

            Console.WriteLine("\n    悪魔「...ただし、代償を払え...」");
            Thread.Sleep(2000);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n    ★ 悪魔との契約が可能になりました ★");
            Console.WriteLine("    ★ ゲームメニューから[D]で契約画面へ ★");
            Console.ResetColor();
            Thread.Sleep(4000);
        }

        static void DevilContractMenu()
        {
            if (!devilContractOffered)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n\n悪魔はまだ現れていない...");
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }

            if (devilContractActive)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n\n既に契約中です");
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }

            while (true)
            {
                Console.Clear();
                Console.BackgroundColor = ConsoleColor.DarkRed;
                Console.ForegroundColor = ConsoleColor.Black;
                Console.WriteLine("\n╔═══════════════════════════════════╗");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("║        😈 悪魔との契約 😈       ║");
                Console.WriteLine("║                                   ║");
                Console.WriteLine("╚═══════════════════════════════════╝");
                Console.BackgroundColor = ConsoleColor.Black;
                Console.ResetColor();

                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine("\n\n悪魔「さあ...選ぶがよい...」\n");
                Console.ResetColor();

                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("【契約1】魂の担保");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("  効果: 次の10回転必ず勝つ");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("  代償: 11回目で即GAME OVER");
                Console.ResetColor();

                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("【契約2】時間との取引");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("  効果: 借金が半額になる");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("  代償: 5分以内に完済必須");
                Console.ResetColor();

                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("【契約3】記憶の代償");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("  効果: 借金全額帳消し");
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("  代償: 全データリセット");
                Console.WriteLine("        (アイテム/実績/コレクション消失)");
                Console.ResetColor();

                Console.WriteLine("\n\n  [1] 契約1を結ぶ");
                Console.WriteLine("  [2] 契約2を結ぶ");
                Console.WriteLine("  [3] 契約3を結ぶ");
                Console.WriteLine("  [0] 契約しない");
                Console.Write("\n選択 > ");

                var key = Console.ReadKey(true);

                if (key.KeyChar == '0')
                {
                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.DarkMagenta;
                    Console.WriteLine("\n\n\n悪魔「...いつでも呼ぶがよい...」");
                    Console.ResetColor();
                    Thread.Sleep(2000);
                    break;
                }
                else if (key.KeyChar >= '1' && key.KeyChar <= '3')
                {
                    int choice = int.Parse(key.KeyChar.ToString());

                    Console.Clear();
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\n\n⚠⚠⚠ 最終確認 ⚠⚠⚠\n");
                    Console.WriteLine($"契約{choice}を結びますか？\n");
                    Console.WriteLine("一度契約すると取り消せません");
                    Console.WriteLine("\n本当に契約しますか？ [Y/N]");
                    Console.ResetColor();

                    var confirmKey = Console.ReadKey(true);  // ← 変数名を変更
                    if (confirmKey.Key == ConsoleKey.Y)      // ← key を confirmKey に変更
                    {
                        ExecuteDevilContract(choice);
                        break;
                    }
                }
            }
        }  // ← DevilContractMenu() の終了
           // ========== 中毒システム強化 ==========


        static void ExecuteDevilContract(int contractType)
        {
            devilContractActive = true;
            devilContractType = contractType;
            contractStartTime = DateTime.Now;

            Console.Clear();

            for (int i = 0; i < 7; i++)
            {
                Console.Clear();
                Console.BackgroundColor = i % 2 == 0 ? ConsoleColor.DarkRed : ConsoleColor.Black;
                Console.ForegroundColor = i % 2 == 0 ? ConsoleColor.Black : ConsoleColor.Red;
                Console.WriteLine("\n\n\n");
                Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈");
                Console.WriteLine("    😈                              😈");
                Console.WriteLine("    😈      契約成立！！！        😈");
                Console.WriteLine("    😈                              😈");
                Console.WriteLine("    😈😈😈😈😈😈😈😈😈😈😈😈😈");
                Thread.Sleep(300);
            }

            Console.Clear();
            Console.BackgroundColor = ConsoleColor.Black;
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n\n");

            switch (contractType)
            {
                case 1:
                    Console.WriteLine("    悪魔「魂を担保に...10回の勝利を与えよう...」");
                    Thread.Sleep(2000);
                    Console.WriteLine("\n    悪魔「...だが11回目には...魂を頂く...」");
                    Thread.Sleep(2000);
                    contract1WinCount = 0;
                    break;

                case 2:
                    Console.WriteLine("    悪魔「借金を半額にしてやろう...」");
                    Thread.Sleep(2000);
                    int reduction = debt / 2;
                    debt -= reduction;
                    contract2OriginalDebt = debt;
                    contract2Deadline = DateTime.Now.AddMinutes(5);
                    Console.WriteLine($"\n    借金が{reduction}G減少した！");
                    Thread.Sleep(2000);
                    Console.WriteLine("\n    悪魔「...だが5分以内に完済せよ...」");
                    Thread.Sleep(2000);
                    Console.WriteLine("\n    悪魔「...さもなくば...魂を頂く...」");
                    Thread.Sleep(2000);
                    break;

                case 3:
                    Console.WriteLine("    悪魔「借金を全て消してやろう...」");
                    Thread.Sleep(2000);
                    debt = 0;
                    debtTurnsRemaining = 0;
                    Console.WriteLine("\n    借金が消えた！");
                    Thread.Sleep(2000);
                    Console.WriteLine("\n    悪魔「...だが、お前の記憶は消える...」");
                    Thread.Sleep(2000);

                    // データリセット
                    itemInventory["お守り"] = 0;
                    itemInventory["幸運のコイン"] = 0;
                    itemInventory["返済猶予券"] = 0;
                    hasGreedRing = false;
                    greedRingEquipped = false;
                    unlockedSymbols.Clear();
                    unlockedSymbols.Add("スライム");
                    unlockedSymbols.Add("ゴーレム");
                    unlockedEvents.Clear();

                    foreach (var mission in missions)
                    {
                        mission.Completed = false;
                    }

                    Console.WriteLine("\n    全てのアイテム・実績が消失した...");
                    Thread.Sleep(2000);

                    devilContractActive = false;
                    devilContractSuccess = true;
                    contract1Complete = true;
                    break;
            }

            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n\n    契約は完了した...");
            Console.ResetColor();
            Thread.Sleep(3000);

            if (!unlockedEvents.Contains($"悪魔契約{contractType}"))
                unlockedEvents.Add($"悪魔契約{contractType}");
        }

        // ========================================
        // ========== DEV MODE ==========
        // ========================================

        static void DevModeEntry()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGreen;
            Console.WriteLine("\n\n\n    [DEV] パスワードを入力してください > ");
            Console.ResetColor();
            Console.CursorVisible = true;
            string input = Console.ReadLine() ?? string.Empty;
            Console.CursorVisible = false;

            if (input.Trim() != "youmukawaii")
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("\n    アクセス拒否");
                Console.ResetColor();
                Thread.Sleep(1200);
                return;
            }

            // 初期化（ゲーム開始前でも使えるように）
            if (!itemInventory.ContainsKey("お守り")) itemInventory["お守り"] = 0;
            if (!itemInventory.ContainsKey("幸運のコイン")) itemInventory["幸運のコイン"] = 0;
            if (!itemInventory.ContainsKey("返済猶予券")) itemInventory["返済猶予券"] = 0;

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n    ✓ DEV MODE アクセス許可");
            Console.ResetColor();
            Thread.Sleep(800);

            DevModeMenu();
        }

        static void DevModeMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.BackgroundColor = ConsoleColor.DarkGreen;
                Console.ForegroundColor = ConsoleColor.Black;
                Console.WriteLine("  ╔══════════════════════════════════════╗  ");
                Console.WriteLine("  ║         ⚙  DEV MODE MENU  ⚙        ║  ");
                Console.WriteLine("  ╚══════════════════════════════════════╝  ");
                Console.ResetColor();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine($"\n  所持金: {money:N0}G  借金: {debt:N0}G  中毒度: {addictionLevel}%  設定: {setting}");
                Console.ResetColor();

                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  [1] ステータス操作");
                Console.WriteLine("  [2] フラグ操作");
                Console.WriteLine("  [3] アイテム操作");
                Console.WriteLine("  [4] スロット設定");
                Console.WriteLine("  [5] 時間・ターン設定");
                Console.WriteLine("  [6] デバッグ情報表示");
                Console.WriteLine("  [7] 全解放（テスト用）");
                Console.WriteLine("  [8] 全フラグリセット");
                Console.WriteLine("  [G] イベントギャラリー");
                Console.WriteLine("  [0] DEV MODE終了");
                Console.ResetColor();
                Console.Write("\n  選択 > ");

                var key = Console.ReadKey(true);
                switch (key.KeyChar)
                {
                    case '1': DevStatusMenu(); break;
                    case '2': DevFlagMenu(); break;
                    case '3': DevItemMenu(); break;
                    case '4': DevSlotMenu(); break;
                    case '5': DevTimeMenu(); break;
                    case '6': DevDebugInfo(); break;
                    case '7': DevUnlockAll(); break;
                    case '8': DevResetAll(); break;
                    case 'g': case 'G': DevEventGallery(); break;
                    case '0': return;
                }
            }
        }

        // ========== [1] ステータス操作 ==========
        static void DevStatusMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  ═══ ステータス操作 ═══");
                Console.WriteLine($"\n  現在値: 所持金={money:N0}G  借金={debt:N0}G  中毒度={addictionLevel}%  設定={setting}");
                Console.WriteLine("\n  [1] 所持金を設定");
                Console.WriteLine("  [2] 借金を設定");
                Console.WriteLine("  [3] 中毒度を設定 (0-100)");
                Console.WriteLine("  [4] 設定を変更 (1-6)");
                Console.WriteLine("  [5] 所持金 +10000G");
                Console.WriteLine("  [6] 借金をゼロにする");
                Console.WriteLine("  [7] 中毒度をゼロにする");
                Console.WriteLine("  [0] 戻る");
                Console.ResetColor();
                Console.Write("\n  選択 > ");

                var key = Console.ReadKey(true);
                if (key.KeyChar == '0') return;

                Console.CursorVisible = true;
                Console.WriteLine();

                switch (key.KeyChar)
                {
                    case '1':
                        Console.Write("  所持金 > ");
                        if (int.TryParse(Console.ReadLine(), out int m)) { money = m; DevMsg($"所持金を {m:N0}G に設定"); }
                        break;
                    case '2':
                        Console.Write("  借金 > ");
                        if (int.TryParse(Console.ReadLine(), out int d)) { debt = d; if (d > 0) { hasEverBorrowedMoney = true; debtTurnsRemaining = 10; } DevMsg($"借金を {d:N0}G に設定"); }
                        break;
                    case '3':
                        Console.Write("  中毒度 (0-100) > ");
                        if (int.TryParse(Console.ReadLine(), out int a)) { addictionLevel = Math.Clamp(a, 0, 100); DevMsg($"中毒度を {addictionLevel}% に設定"); }
                        break;
                    case '4':
                        Console.Write("  設定 (1-6) > ");
                        if (int.TryParse(Console.ReadLine(), out int s) && s >= 1 && s <= 6) { setting = s; DevMsg($"設定{s}に変更"); }
                        break;
                    case '5':
                        money += 10000; DevMsg("+10000G");
                        break;
                    case '6':
                        debt = 0; debtTurnsRemaining = 0; DevMsg("借金ゼロ");
                        break;
                    case '7':
                        addictionLevel = 0; isAddicted = false; DevMsg("中毒度ゼロ");
                        break;
                }
                Console.CursorVisible = false;
            }
        }

        // ========== [2] フラグ操作 ==========
        static void DevFlagMenu()
        {
            // (名前, getter, setter) のリスト
            var flags = new List<(string label, Func<bool> get, Action<bool> set)>
            {
                ("godMode",                  () => godMode,                  v => godMode = v),
                ("godModePermanent",         () => godModePermanent,         v => godModePermanent = v),
                ("luckyTimeActive",          () => luckyTimeActive,          v => luckyTimeActive = v),
                ("vipRoomUnlocked",          () => vipRoomUnlocked,          v => vipRoomUnlocked = v),
                ("isInVIPRoom",              () => isInVIPRoom,              v => isInVIPRoom = v),
                ("undergroundUnlocked",      () => undergroundUnlocked,      v => undergroundUnlocked = v),
                ("isInUnderground",          () => isInUnderground,          v => isInUnderground = v),
                ("dreamCasinoUnlocked",      () => dreamCasinoUnlocked,      v => dreamCasinoUnlocked = v),
                ("hasEverBorrowedMoney",     () => hasEverBorrowedMoney,     v => hasEverBorrowedMoney = v),
                ("hasSeenConversation",      () => hasSeenConversation,      v => hasSeenConversation = v),
                ("hasSeenMysteriousWoman",   () => hasSeenMysteriousWoman,   v => hasSeenMysteriousWoman = v),
                ("hasSeenVIPDealer",         () => hasSeenVIPDealer,         v => hasSeenVIPDealer = v),
                ("hasSeenUndergroundDealer", () => hasSeenUndergroundDealer, v => hasSeenUndergroundDealer = v),
                ("mushroomManMet",           () => mushroomManMet,           v => mushroomManMet = v),
                ("devilContractOffered",     () => devilContractOffered,     v => devilContractOffered = v),
                ("devilContractActive",      () => devilContractActive,      v => devilContractActive = v),
                ("devilContractSuccess",     () => devilContractSuccess,     v => devilContractSuccess = v),
                ("contract1Complete",        () => contract1Complete,        v => contract1Complete = v),
                ("hasGreedRing",             () => hasGreedRing,             v => hasGreedRing = v),
                ("greedRingEquipped",        () => greedRingEquipped,        v => greedRingEquipped = v),
                ("hasDevilCoin",             () => hasDevilCoin,             v => hasDevilCoin = v),
                ("hasBloodAmulet",           () => hasBloodAmulet,           v => hasBloodAmulet = v),
                ("hasDeathRing",             () => hasDeathRing,             v => hasDeathRing = v),
                ("hasTimeClock",             () => hasTimeClock,             v => hasTimeClock = v),
                ("hasOracleBall",            () => hasOracleBall,            v => hasOracleBall = v),
                ("hasUsedRehab",             () => hasUsedRehab,             v => hasUsedRehab = v),
                ("isAddicted",              () => isAddicted,               v => isAddicted = v),
                ("trueEndingUnlocked",       () => trueEndingUnlocked,       v => trueEndingUnlocked = v),
                ("vip5000BetWin",            () => vip5000BetWin,            v => vip5000BetWin = v),
                ("undergroundAllInWin",      () => undergroundAllInWin,      v => undergroundAllInWin = v),
                ("undergroundCursedMode",    () => undergroundCursedMode,    v => undergroundCursedMode = v),
                ("bellMetFirst",             () => bellMetFirst,             v => bellMetFirst = v),
            };

            int page = 0;
            int perPage = 12;

            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  ═══ フラグ操作 ═══");
                Console.WriteLine("  数字キーでON/OFF切替  [N]次ページ  [P]前ページ  [0]戻る\n");

                int start = page * perPage;
                int end = Math.Min(start + perPage, flags.Count);
                for (int i = start; i < end; i++)
                {
                    var f = flags[i];
                    bool val = f.get();
                    Console.ForegroundColor = val ? ConsoleColor.Yellow : ConsoleColor.DarkGray;
                    Console.WriteLine($"  [{i - start + 1,2}] {(val ? "ON " : "OFF")}  {f.label}");
                }
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine($"\n  ページ {page + 1} / {(flags.Count + perPage - 1) / perPage}");
                Console.ResetColor();
                Console.Write("  選択 > ");

                var key = Console.ReadKey(true);
                if (key.KeyChar == '0') return;
                if (key.Key == ConsoleKey.N) { page = Math.Min(page + 1, (flags.Count - 1) / perPage); continue; }
                if (key.Key == ConsoleKey.P) { page = Math.Max(page - 1, 0); continue; }

                if (key.KeyChar >= '1' && key.KeyChar <= '9')
                {
                    int idx = start + (key.KeyChar - '1');
                    if (idx < flags.Count)
                    {
                        var f = flags[idx];
                        bool newVal = !f.get();
                        f.set(newVal);
                        DevMsg($"{f.label} → {(newVal ? "ON" : "OFF")}");
                    }
                }
            }
        }

        // ========== [3] アイテム操作 ==========
        static void DevItemMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  ═══ アイテム操作 ═══\n");
                Console.WriteLine($"  お守り         : {itemInventory.GetValueOrDefault("お守り", 0)}個");
                Console.WriteLine($"  幸運のコイン   : {itemInventory.GetValueOrDefault("幸運のコイン", 0)}個");
                Console.WriteLine($"  返済猶予券     : {itemInventory.GetValueOrDefault("返済猶予券", 0)}個");
                Console.WriteLine($"  強欲の指輪     : {(hasGreedRing ? "所持" : "なし")}  装備={greedRingEquipped}");
                Console.WriteLine($"  悪魔のコイン   : {(hasDevilCoin ? "所持" : "なし")}");
                Console.WriteLine($"  血塗られたお守り: {(hasBloodAmulet ? "所持" : "なし")}");
                Console.WriteLine($"  死神の指輪     : {(hasDeathRing ? "所持" : "なし")}");
                Console.WriteLine($"  時を刻む懐中時計 : {(hasTimeClock ? "所持" : "なし")}");
                Console.WriteLine($"  予言の水晶球   : {(hasOracleBall ? "所持" : "なし")}");
                Console.WriteLine($"\n  解放シンボル: {string.Join(", ", unlockedSymbols)}");

                Console.WriteLine("\n  [1] お守り +1      [2] 幸運のコイン +1  [3] 返済猶予券 +1");
                Console.WriteLine("  [4] 強欲の指輪入手 [5] 呪いアイテム全入手");
                Console.WriteLine("  [6] 全シンボル解放 [7] イベント全解放");
                Console.WriteLine("  [8] アイテム全クリア");
                Console.WriteLine("  [0] 戻る");
                Console.ResetColor();
                Console.Write("\n  選択 > ");

                var key = Console.ReadKey(true);
                switch (key.KeyChar)
                {
                    case '0': return;
                    case '1': itemInventory["お守り"] = itemInventory.GetValueOrDefault("お守り", 0) + 1; DevMsg("お守り +1"); break;
                    case '2': itemInventory["幸運のコイン"] = itemInventory.GetValueOrDefault("幸運のコイン", 0) + 1; DevMsg("幸運のコイン +1"); break;
                    case '3': itemInventory["返済猶予券"] = itemInventory.GetValueOrDefault("返済猶予券", 0) + 1; DevMsg("返済猶予券 +1"); break;
                    case '4': hasGreedRing = true; greedRingEquipped = true; DevMsg("強欲の指輪 入手・装備"); break;
                    case '5':
                        hasDevilCoin = true; hasBloodAmulet = true; hasDeathRing = true;
                        hasTimeClock = true; hasOracleBall = true; cursedItemCount = 5;
                        DevMsg("呪いアイテム全入手");
                        break;
                    case '6':
                        string[] allSymbols = { "スライム", "ゴーレム", "ドラゴン", "フェニックス", "ユニコーン", "悪魔", "天使", "神" };
                        foreach (var s in allSymbols)
                            if (!unlockedSymbols.Contains(s)) unlockedSymbols.Add(s);
                        DevMsg("全シンボル解放");
                        break;
                    case '7':
                        string[] allEvents = {
                            "設定6解放", "VIPルーム解放", "地下カジノ解放", "夢カジノ解放",
                            "悪魔契約1", "悪魔契約2", "悪魔契約3", "OVERFLOW END", "RTA達成",
                            "謎の女性", "777達成", "GOD MODE", "TRUE END"
                        };
                        foreach (var e in allEvents)
                            if (!unlockedEvents.Contains(e)) unlockedEvents.Add(e);
                        DevMsg($"イベント {unlockedEvents.Count}件解放");
                        break;
                    case '8':
                        itemInventory["お守り"] = 0;
                        itemInventory["幸運のコイン"] = 0;
                        itemInventory["返済猶予券"] = 0;
                        hasGreedRing = false; greedRingEquipped = false;
                        hasDevilCoin = false; hasBloodAmulet = false;
                        hasDeathRing = false; hasTimeClock = false; hasOracleBall = false;
                        cursedItemCount = 0;
                        DevMsg("アイテム全クリア");
                        break;
                }
            }
        }

        // ========== [4] スロット設定 ==========
        static void DevSlotMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  ═══ スロット設定 ═══\n");
                Console.WriteLine($"  totalSpins        = {totalSpins}");
                Console.WriteLine($"  consecutiveWins   = {consecutiveWins}");
                Console.WriteLine($"  consecutiveLosses = {consecutiveLosses}");
                Console.WriteLine($"  total777Count     = {total777Count}");
                Console.WriteLine($"  bigWinCount       = {bigWinCount}");
                Console.WriteLine($"  godMode           = {godMode}  残り={godModeRemaining}");
                Console.WriteLine($"  luckyTimeActive   = {luckyTimeActive}  残り={luckyTimeRemaining}");

                Console.WriteLine("\n  [1] totalSpins を設定");
                Console.WriteLine("  [2] 連続勝利数を設定");
                Console.WriteLine("  [3] 777回数を設定");
                Console.WriteLine("  [4] GOD MODE 即発動 (10ターン)");
                Console.WriteLine("  [5] LUCKY TIME 即発動 (10ターン)");
                Console.WriteLine("  [6] GOD MODE 解除");
                Console.WriteLine("  [7] LUCKY TIME 解除");
                Console.WriteLine("  [0] 戻る");
                Console.ResetColor();
                Console.Write("\n  選択 > ");

                var key = Console.ReadKey(true);
                if (key.KeyChar == '0') return;

                Console.CursorVisible = true;
                Console.WriteLine();
                switch (key.KeyChar)
                {
                    case '1':
                        Console.Write("  totalSpins > ");
                        if (int.TryParse(Console.ReadLine(), out int sp)) { totalSpins = sp; DevMsg($"totalSpins = {sp}"); }
                        break;
                    case '2':
                        Console.Write("  連続勝利数 > ");
                        if (int.TryParse(Console.ReadLine(), out int cw)) { consecutiveWins = cw; DevMsg($"consecutiveWins = {cw}"); }
                        break;
                    case '3':
                        Console.Write("  777回数 > ");
                        if (int.TryParse(Console.ReadLine(), out int s7)) { total777Count = s7; DevMsg($"total777Count = {s7}"); }
                        break;
                    case '4':
                        godMode = true; godModeRemaining = 10; DevMsg("GOD MODE 発動 (10ターン)");
                        break;
                    case '5':
                        luckyTimeActive = true; luckyTimeRemaining = 10; DevMsg("LUCKY TIME 発動 (10ターン)");
                        break;
                    case '6':
                        godMode = false; godModeRemaining = 0; DevMsg("GOD MODE 解除");
                        break;
                    case '7':
                        luckyTimeActive = false; luckyTimeRemaining = 0; DevMsg("LUCKY TIME 解除");
                        break;
                }
                Console.CursorVisible = false;
            }
        }

        // ========== [5] 時間・ターン設定 ==========
        static void DevTimeMenu()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("\n  ═══ 時間・ターン設定 ═══\n");
                Console.WriteLine($"  debtTurnsRemaining     = {debtTurnsRemaining}");
                Console.WriteLine($"  devilContractTurns     = {devilContractTurns}");
                Console.WriteLine($"  devilContractType      = {devilContractType}");
                Console.WriteLine($"  contract1WinCount      = {contract1WinCount}");
                Console.WriteLine($"  dreamLayerCleared      = {dreamLayerCleared}");
                Console.WriteLine($"  undergroundVisits      = {undergroundVisits}");
                Console.WriteLine($"  vipTotalVisits         = {vipTotalVisits}");
                Console.WriteLine($"  autoSaveTurns          = {autoSaveTurns}");

                Console.WriteLine("\n  [1] 借金返済ターン数を設定");
                Console.WriteLine("  [2] 悪魔契約ターン数を設定");
                Console.WriteLine("  [3] 夢カジノクリア層数を設定");
                Console.WriteLine("  [4] 地下カジノ訪問回数を設定");
                Console.WriteLine("  [5] VIP訪問回数を設定");
                Console.WriteLine("  [6] 契約1勝利カウントを設定");
                Console.WriteLine("  [0] 戻る");
                Console.ResetColor();
                Console.Write("\n  選択 > ");

                var key = Console.ReadKey(true);
                if (key.KeyChar == '0') return;

                Console.CursorVisible = true;
                Console.WriteLine();
                switch (key.KeyChar)
                {
                    case '1':
                        Console.Write("  借金返済ターン数 > ");
                        if (int.TryParse(Console.ReadLine(), out int dt)) { debtTurnsRemaining = dt; DevMsg($"debtTurnsRemaining = {dt}"); }
                        break;
                    case '2':
                        Console.Write("  悪魔契約ターン数 > ");
                        if (int.TryParse(Console.ReadLine(), out int dct)) { devilContractTurns = dct; DevMsg($"devilContractTurns = {dct}"); }
                        break;
                    case '3':
                        Console.Write("  夢カジノクリア層 (0-5) > ");
                        if (int.TryParse(Console.ReadLine(), out int dl)) { dreamLayerCleared = Math.Clamp(dl, 0, 5); DevMsg($"dreamLayerCleared = {dreamLayerCleared}"); }
                        break;
                    case '4':
                        Console.Write("  地下カジノ訪問回数 > ");
                        if (int.TryParse(Console.ReadLine(), out int uv)) { undergroundVisits = uv; DevMsg($"undergroundVisits = {uv}"); }
                        break;
                    case '5':
                        Console.Write("  VIP訪問回数 > ");
                        if (int.TryParse(Console.ReadLine(), out int vv)) { vipTotalVisits = vv; DevMsg($"vipTotalVisits = {vv}"); }
                        break;
                    case '6':
                        Console.Write("  契約1勝利カウント > ");
                        if (int.TryParse(Console.ReadLine(), out int c1)) { contract1WinCount = c1; DevMsg($"contract1WinCount = {c1}"); }
                        break;
                }
                Console.CursorVisible = false;
            }
        }

        // ========== [6] デバッグ情報表示 ==========
        static void DevDebugInfo()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n  ════════════════════════════════════");
            Console.WriteLine("       DEV DEBUG INFO");
            Console.WriteLine("  ════════════════════════════════════");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine($"  playerName          = {playerName}");
            Console.WriteLine($"  money               = {money:N0}");
            Console.WriteLine($"  debt                = {debt:N0}");
            Console.WriteLine($"  setting             = {setting}");
            Console.WriteLine($"  totalSpins          = {totalSpins}");
            Console.WriteLine($"  totalWinAmount      = {totalWinAmount:N0}");
            Console.WriteLine($"  totalLoseAmount     = {totalLoseAmount:N0}");
            Console.WriteLine($"  addictionLevel      = {addictionLevel}%");
            Console.WriteLine($"  consecutiveWins     = {consecutiveWins}");
            Console.WriteLine($"  consecutiveLosses   = {consecutiveLosses}");
            Console.WriteLine($"  total777Count       = {total777Count}");
            Console.WriteLine($"  maxMoney            = {maxMoney:N0}");
            Console.WriteLine($"  maxDebt             = {maxDebt:N0}");
            Console.WriteLine($"  godMode             = {godMode} ({godModeRemaining}残)");
            Console.WriteLine($"  luckyTimeActive     = {luckyTimeActive} ({luckyTimeRemaining}残)");
            Console.WriteLine($"  vipRoomUnlocked     = {vipRoomUnlocked}");
            Console.WriteLine($"  undergroundUnlocked = {undergroundUnlocked}");
            Console.WriteLine($"  dreamCasinoUnlocked = {dreamCasinoUnlocked}");
            Console.WriteLine($"  dreamLayerCleared   = {dreamLayerCleared}");
            Console.WriteLine($"  devilContractActive = {devilContractActive} (type={devilContractType})");
            Console.WriteLine($"  cursedItemCount     = {cursedItemCount}");
            Console.WriteLine($"  unlockedSymbols     = {unlockedSymbols.Count}種");
            Console.WriteLine($"  unlockedEvents      = {unlockedEvents.Count}件");
            Console.WriteLine($"  missions completed  = {missions.Count(m => m.Completed)} / {missions.Count}");

            Console.ForegroundColor = ConsoleColor.DarkGreen;
            Console.WriteLine("\n  ════════════════════════════════════");
            Console.WriteLine("  [何かキー] 戻る");
            Console.ResetColor();
            Console.ReadKey(true);
        }

        // ========== [7] 全解放 ==========
        static void DevUnlockAll()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n  全解放しますか？ [Y/N]");
            Console.ResetColor();
            var key = Console.ReadKey(true);
            if (key.Key != ConsoleKey.Y) return;

            money = 999999;
            debt = 0; debtTurnsRemaining = 0;
            addictionLevel = 0; isAddicted = false;
            setting = 6;
            godMode = true; godModeRemaining = 999;
            luckyTimeActive = true; luckyTimeRemaining = 999;
            vipRoomUnlocked = true;
            undergroundUnlocked = true;
            dreamCasinoUnlocked = true;
            dreamLayerCleared = 5;
            hasGreedRing = true; greedRingEquipped = true;
            hasDevilCoin = true; hasBloodAmulet = true;
            hasDeathRing = true; hasTimeClock = true; hasOracleBall = true;
            cursedItemCount = 5;
            total777Count = 5;
            totalSpins = 200;
            hasEverBorrowedMoney = true;
            hasUsedRehab = true;
            vipTotalVisits = 10; vipTotalWins = 5; vipTotalSpins = 30;
            undergroundVisits = 5; undergroundWins = 3;
            itemInventory["お守り"] = 9;
            itemInventory["幸運のコイン"] = 9;
            itemInventory["返済猶予券"] = 9;

            string[] allSymbols = { "スライム", "ゴーレム", "ドラゴン", "フェニックス", "ユニコーン", "悪魔", "天使", "神" };
            foreach (var s in allSymbols)
                if (!unlockedSymbols.Contains(s)) unlockedSymbols.Add(s);

            foreach (var m in missions) m.Completed = true;

            DevMsg("全解放完了！");
        }

        // ========== [8] 全リセット ==========
        static void DevResetAll()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n  全フラグをリセットしますか？ [Y/N]");
            Console.ResetColor();
            var key = Console.ReadKey(true);
            if (key.Key != ConsoleKey.Y) return;

            money = 1000; debt = 0; debtTurnsRemaining = 0;
            addictionLevel = 0; isAddicted = false;
            setting = 0;
            godMode = false; godModePermanent = false; godModeRemaining = 0;
            luckyTimeActive = false; luckyTimeRemaining = 0;
            vipRoomUnlocked = false; isInVIPRoom = false;
            undergroundUnlocked = false; isInUnderground = false;
            dreamCasinoUnlocked = false; dreamLayerCleared = 0;
            hasGreedRing = false; greedRingEquipped = false;
            hasDevilCoin = false; hasBloodAmulet = false;
            hasDeathRing = false; hasTimeClock = false; hasOracleBall = false;
            cursedItemCount = 0;
            total777Count = 0; totalSpins = 0;
            consecutiveWins = 0; consecutiveLosses = 0;
            hasEverBorrowedMoney = false; hasUsedRehab = false;
            devilContractActive = false; devilContractOffered = false;
            devilContractSuccess = false; contract1Complete = false;
            itemInventory["お守り"] = 0;
            itemInventory["幸運のコイン"] = 0;
            itemInventory["返済猶予券"] = 0;
            unlockedSymbols.Clear();
            unlockedSymbols.Add("スライム");
            unlockedSymbols.Add("ゴーレム");
            unlockedEvents.Clear();
            foreach (var m in missions) m.Completed = false;

            DevMsg("全フラグリセット完了");
        }

        // ========== イベントギャラリー ==========
        static void DevEventGallery()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n  ╔══════════════════════════════════════╗");
                Console.WriteLine("  ║       EVENT GALLERY                  ║");
                Console.WriteLine("  ╠══════════════════════════════════════╣");
                Console.ResetColor();
                Console.WriteLine("  ║  [1] チャプター1（最初の会話）       ║");
                Console.WriteLine("  ║  [2] 廃娯楽施設 1階                  ║");
                Console.WriteLine("  ║  [3] 廃娯楽施設 2階                  ║");
                Console.WriteLine("  ║  [4] 廃娯楽施設 3階                  ║");
                Console.WriteLine("  ║  [5] 地下室イベント（時計必要）      ║");
                Console.WriteLine("  ║  [6] クソエンディング（ごめん）      ║");
                Console.WriteLine("  ║  [7] エンディングA（ここにいるから） ║");
                Console.WriteLine("  ║  [8] エンディングB（行こ）           ║");
                Console.WriteLine("  ║  [9] BAD END（そういう人だったんだ） ║");
                Console.WriteLine("  ║  [A] 無垢な宝石 入手演出             ║");
                Console.WriteLine("  ║  [B] 虚栄のカギ 購入演出             ║");
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("  ╚══════════════════════════════════════╝");
                Console.ResetColor();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n  ※ 必要なフラグは自動でセットされます");
                Console.ResetColor();
                Console.Write("  > ");

                var key = Console.ReadKey(true);
                Console.Clear();

                switch (key.KeyChar)
                {
                    case '1':
                        chapter1Seen = false;
                        Chapter1_FirstConversation();
                        break;
                    case '2':
                        hasInnocentGem = true; vanityKeyPurchased = true;
                        abandonedCasinoUnlocked = true; abandonedCasinoEntered = false;
                        if (roomsOpened[0].Length < 5) roomsOpened[0] = new bool[5];
                        money = Math.Max(money, 10000);
                        DevGalleryFloor1();
                        continue;
                    case '3':
                        hasInnocentGem = true; abandonedCasinoUnlocked = true;
                        abandonedCasinoEntered = true;
                        roomsOpened[0] = new bool[] { true, true, true, true, true };
                        if (roomsOpened[1].Length < 5) roomsOpened[1] = new bool[5];
                        money = Math.Max(money, 20000);
                        DevGalleryFloor2();
                        continue;
                    case '4':
                        hasInnocentGem = true; abandonedCasinoUnlocked = true;
                        abandonedCasinoEntered = true;
                        roomsOpened[0] = new bool[] { true, true, true, true, true };
                        roomsOpened[1] = new bool[] { true, true, true, true, true };
                        if (roomsOpened[2].Length < 5) roomsOpened[2] = new bool[5];
                        money = Math.Max(money, 30000);
                        DevGalleryFloor3();
                        continue;
                    case '5':
                        hasInnocentGem = true; timeClockEquipped = true;
                        hasTimeClock = true;
                        BasementDoorFound();
                        break;
                    case '6':
                        hasInnocentGem = true; timeClockEquipped = false;
                        roomsOpened[2] = new bool[] { true, true, true, true, true };
                        AbandonedCasinoExitEvent();
                        break;
                    case '7':
                        hasInnocentGem = false; hasJewelRing = true;
                        EndingRouteA_Owner();
                        break;
                    case '8':
                        hasInnocentGem = false; hasJewelRing = true;
                        EndingRouteB_Bell();
                        break;
                    case '9':
                        hasInnocentGem = true; hasExchangedMoney = false;
                        money = Math.Max(money, 5000);
                        BuyExchangedMoney();
                        break;
                    case 'a':
                    case 'A':
                        hasInnocentGem = false;
                        InnocentGemFound();
                        break;
                    case 'b':
                    case 'B':
                        chapter1Seen = true; vanityKeyPurchased = false;
                        abandonedCasinoUnlocked = false;
                        money = Math.Max(money, 5000);
                        ShopHiddenPage();
                        break;
                    case '0': return;
                    default: continue;
                }

                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n\n  ── イベント終了 ──");
                Console.WriteLine("\n  [何かキー] ギャラリーに戻る");
                Console.ResetColor();
                Console.ReadKey(true);
            }
        }

        static void DevGalleryFloor1()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n  ── 廃娯楽施設 1階 ──");
                Console.ResetColor();
                Console.WriteLine("\n  [1] 部屋A：笑ってる女の子の絵");
                Console.WriteLine("  [2] 部屋B：片方だけの靴");
                Console.WriteLine("  [3] 部屋C：大きな手と小さな手");
                Console.WriteLine("  [4] 部屋D：ベルと書いた紙");
                Console.WriteLine("  [5] 最終部屋：全部繋がる");
                Console.WriteLine("  [6] 1階まるごと（入口から）");
                Console.WriteLine("  [0] 戻る");
                Console.Write("\n  > ");
                var k = Console.ReadKey(true);
                Console.Clear();
                switch (k.KeyChar)
                {
                    case '1': roomsOpened[0][0] = false; OpenRoom(0, 0, 0, Room1F_A); break;
                    case '2': roomsOpened[0][1] = false; OpenRoom(0, 1, 0, Room1F_B); break;
                    case '3': roomsOpened[0][2] = false; OpenRoom(0, 2, 0, Room1F_C); break;
                    case '4': roomsOpened[0][3] = false; OpenRoom(0, 3, 0, Room1F_D); break;
                    case '5':
                        roomsOpened[0] = new bool[] { true, true, true, true, false };
                        OpenRoom(0, 4, 0, Room1F_Final); break;
                    case '6':
                        abandonedCasinoEntered = false;
                        roomsOpened[0] = new bool[5];
                        EnterAbandonedCasino(); return;
                    case '0': return;
                    default: continue;
                }
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る");
                Console.ResetColor();
                Console.ReadKey(true);
            }
        }

        static void DevGalleryFloor2()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n  ── 廃娯楽施設 2階 ──");
                Console.ResetColor();
                Console.WriteLine("\n  [1] 部屋A：古いコート");
                Console.WriteLine("  [2] 部屋B：二人で食卓");
                Console.WriteLine("  [3] 部屋C：半分の本");
                Console.WriteLine("  [4] 部屋D：空っぽの椅子");
                Console.WriteLine("  [5] 最終部屋：また来る");
                Console.WriteLine("  [6] 2階まるごと（入口から）");
                Console.WriteLine("  [0] 戻る");
                Console.Write("\n  > ");
                var k = Console.ReadKey(true);
                Console.Clear();
                switch (k.KeyChar)
                {
                    case '1': roomsOpened[1][0] = false; OpenRoom(1, 0, 0, Room2F_A); break;
                    case '2': roomsOpened[1][1] = false; OpenRoom(1, 1, 0, Room2F_B); break;
                    case '3': roomsOpened[1][2] = false; OpenRoom(1, 2, 0, Room2F_C); break;
                    case '4': roomsOpened[1][3] = false; OpenRoom(1, 3, 0, Room2F_D); break;
                    case '5':
                        roomsOpened[1] = new bool[] { true, true, true, true, false };
                        OpenRoom(1, 4, 0, Room2F_Final); break;
                    case '6':
                        roomsOpened[1] = new bool[5];
                        GoToFloor2(); return;
                    case '0': return;
                    default: continue;
                }
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る");
                Console.ResetColor();
                Console.ReadKey(true);
            }
        }

        static void DevGalleryFloor3()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n  ── 廃娯楽施設 3階 ──");
                Console.ResetColor();
                Console.WriteLine("\n  [1] 部屋A：使い込まれたエプロン");
                Console.WriteLine("  [2] 部屋B：仕事中のベル（顔のない絵）");
                Console.WriteLine("  [3] 部屋C：折れたネームプレート");
                Console.WriteLine("  [4] 部屋D：窓のない部屋に星");
                Console.WriteLine("  [5] 最終部屋：オーナーの手紙");
                Console.WriteLine("  [6] 3階まるごと（入口から）");
                Console.WriteLine("  [0] 戻る");
                Console.Write("\n  > ");
                var k = Console.ReadKey(true);
                Console.Clear();
                switch (k.KeyChar)
                {
                    case '1': roomsOpened[2][0] = false; OpenRoom(2, 0, 0, Room3F_A); break;
                    case '2': roomsOpened[2][1] = false; OpenRoom(2, 1, 0, Room3F_B); break;
                    case '3': roomsOpened[2][2] = false; OpenRoom(2, 2, 0, Room3F_C); break;
                    case '4': roomsOpened[2][3] = false; OpenRoom(2, 3, 0, Room3F_D); break;
                    case '5':
                        roomsOpened[2] = new bool[] { true, true, true, true, false };
                        OpenRoom(2, 4, 0, Room3F_Final); break;
                    case '6':
                        roomsOpened[2] = new bool[5];
                        GoToFloor3(); return;
                    case '0': return;
                    default: continue;
                }
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGreen;
                Console.WriteLine("\n\n  ── イベント終了 ──\n  [何かキー] 戻る");
                Console.ResetColor();
                Console.ReadKey(true);
            }
        }

        // ========== DEV共通メッセージ ==========
        static void DevMsg(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"\n  ✓ {msg}");
            Console.ResetColor();
            Thread.Sleep(800);
        }

        // ========================================
        // ========== コンソールグリッチ演出 ==========
        // ========================================

        static readonly char[] glitchChars = {
            '█','▓','▒','░','╬','╪','╫','║','═','╔','╗','╚','╝',
            '▲','▼','◆','◇','★','☆','※','〓','■','□','●','○',
            '?','!','#','%','&','@','$','/','\\','|','+','-','~'
        };

        // テキストをグリッチさせて表示する
        static void GlitchText(string text, ConsoleColor baseColor, int cycles = 6, int delayMs = 40)
        {
            var chars = text.ToCharArray();
            var rng = rand;

            ConsoleColor[] flashColors = {
                ConsoleColor.Red, ConsoleColor.Cyan, ConsoleColor.Magenta,
                ConsoleColor.Yellow, ConsoleColor.White, ConsoleColor.DarkRed
            };

            int left = Console.CursorLeft;
            int top = Console.CursorTop;

            for (int c = 0; c < cycles; c++)
            {
                Console.SetCursorPosition(left, top);

                // 乱れ具合：最初は激しく、後半は落ち着く
                double chaos = 1.0 - (double)c / cycles;

                Console.ForegroundColor = flashColors[c % flashColors.Length];

                for (int i = 0; i < chars.Length; i++)
                {
                    if (chars[i] == ' ')
                    {
                        Console.Write(' ');
                        continue;
                    }

                    if (rng.NextDouble() < chaos * 0.6)
                        Console.Write(glitchChars[rng.Next(glitchChars.Length)]);
                    else
                        Console.Write(chars[i]);
                }

                Thread.Sleep(delayMs);
            }

            // 最後は元のテキストに戻す
            Console.SetCursorPosition(left, top);
            Console.ForegroundColor = baseColor;
            Console.Write(text);
            Console.ResetColor();
        }

        // 画面全体がバグる演出
        static void ScreenGlitch(int intensity = 1)
        {
            // intensity: 1=軽め 2=中 3=ガチバグ
            int frames = 4 + intensity * 3;

            ConsoleColor[] colors = {
                ConsoleColor.Red, ConsoleColor.DarkCyan, ConsoleColor.Magenta,
                ConsoleColor.DarkRed, ConsoleColor.Yellow
            };

            string[] noiseLines = {
                "▓▒░█▓╬▒░╪▓█░▒╫╬▓▒░█▓▒░╬╪",
                "╔═╗║╚╝╬╫╪▲▼◆◇★☆※〓■□●○",
                "!?#%&@$/\\|+-~▓▒░█▓╬╪╫▲▼",
                "〓■□●○◆◇▲▼╔═╗║╚╝╬╫╪▓▒░",
            };

            int savedTop = Math.Min(Console.CursorTop, Console.BufferHeight - 1);

            for (int f = 0; f < frames; f++)
            {
                // 画面の一部にノイズラインを挿入
                int noiseRow = rand.Next(2, Math.Min(Console.WindowHeight - 2, 20));
                try
                {
                    Console.SetCursorPosition(0, noiseRow);
                    Console.ForegroundColor = colors[f % colors.Length];
                    Console.Write(noiseLines[rand.Next(noiseLines.Length)].PadRight(Console.WindowWidth - 1));
                }
                catch { }

                Thread.Sleep(35 + intensity * 15);

                // ノイズを消す
                try
                {
                    Console.SetCursorPosition(0, noiseRow);
                    Console.Write(new string(' ', Console.WindowWidth - 1));
                }
                catch { }
            }

            Console.ResetColor();
            try { Console.SetCursorPosition(0, savedTop); } catch { }
        }

        // 777グリッチ：JACKPOTの文字が乱れてから確定する
        static void JackpotGlitch()
        {
            Console.WriteLine();

            string line1 = "    ╔══════════════════════════════╗";
            string line2 = "    ║   ★  7  7  7  ★  JACKPOT  ★  ║";
            string line3 = "    ╚══════════════════════════════╝";

            // 枠が崩れる
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.Write(line1); GlitchText(line1, ConsoleColor.DarkRed, 5, 50);
            Console.WriteLine();
            Console.Write(line2); GlitchText(line2, ConsoleColor.Yellow, 8, 45);
            Console.WriteLine();
            Console.Write(line3); GlitchText(line3, ConsoleColor.DarkRed, 5, 50);
            Console.WriteLine();

            Thread.Sleep(200);

            // 画面ノイズ
            ScreenGlitch(2);

            // 最終的にキレイに表示
            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("    ╔══════════════════════════════╗");
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("    ║   ★  7  7  7  ★  JACKPOT  ★  ║");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("    ╚══════════════════════════════╝");
            Console.ResetColor();

            Thread.Sleep(600);
        }

        // スピン中グリッチ：リール表示が一瞬バグる
        static void SpinGlitch()
        {
            if (addictionLevel < 60 && !devilContractActive) return;

            // 発動確率：中毒度/悪魔契約で変化
            int chance = devilContractActive ? 25 : (addictionLevel - 60) / 3;
            if (rand.Next(100) >= chance) return;

            ScreenGlitch(1);

            // 一瞬だけ不穏なテキストを表示
            string[] messages = {
                "    ERROR: REEL_SYNC_FAILED",
                "    ████ 存在してはいけない ████",
                "    SYSTEM: memory corruption detected",
                "    ▓▒░ 現実が　　歪んで　　いる ░▒▓",
                "    ??? UNDEFINED BEHAVIOR ???",
            };

            int savedTop = Console.CursorTop;
            try
            {
                Console.SetCursorPosition(0, Math.Max(0, savedTop - 2));
                Console.ForegroundColor = ConsoleColor.DarkRed;
                string msg = messages[rand.Next(messages.Length)];
                GlitchText(msg, ConsoleColor.DarkRed, 4, 40);
                Thread.Sleep(300);
                Console.SetCursorPosition(0, Console.CursorTop);
                Console.Write(new string(' ', msg.Length + 4));
                Console.SetCursorPosition(0, savedTop);
            }
            catch { }

            Console.ResetColor();
        }

        // メニューグリッチ：選択肢の一部が一瞬化ける
        static void MenuGlitch()
        {
            if (addictionLevel < 80) return;
            if (rand.Next(100) >= 8) return;

            string[] flickers = {
                "    ??? 何かが見えた気がした",
                "    ▓▓▓ ベル「...逃げないで」 ▓▓▓",
                "    ERROR 404: 現実が見つかりません",
                "    ░░░ もうやめろ ░░░",
            };

            Thread.Sleep(100);
            int savedTop = Console.CursorTop;
            try
            {
                Console.SetCursorPosition(0, Math.Max(0, savedTop - 1));
                Console.ForegroundColor = ConsoleColor.DarkRed;
                string msg = flickers[rand.Next(flickers.Length)];
                Console.Write(msg);
                Thread.Sleep(180);
                Console.SetCursorPosition(0, Console.CursorTop);
                Console.Write(new string(' ', msg.Length + 4));
                Console.SetCursorPosition(0, savedTop);
            }
            catch { }
            Console.ResetColor();
        }
        static void Chapter1_FirstConversation()
        {
            Console.Clear();
            Thread.Sleep(800);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n\n    カラン..カランと店の呼び鈴が鳴った", 35);
            Thread.Sleep(1500);
            Console.Clear();
            TypewriterEffect("\n\n    店の中に入り　カウンターにいるベルに目をやる", 35);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}：「来ちゃった」", 40);
            Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「...」", 40);
            Thread.Sleep(1200);
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n    {playerName}：「...」", 40);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    いつもなら元気のある声が聞こえるはずが　今日はやけに静かだ", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    すると　「はっ！」とした勢いで私の方を見て　思い出したかのように", 35);
            Thread.Sleep(500);
            TypewriterEffect("\n\n    ベル：「..! い、いらっしゃい！！」", 45);
            Thread.Sleep(1500);
            TypewriterEffect("\n\n    ベル：「あ、なーんだ。あなただったのですね。」", 40);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    そう言い終えると　また静かになってしまった", 35);
            Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}：「どうしたんだ？　いつもとは違って変だけど　何かあったの？」", 38);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルは少し考えた様子を見せた後　私に話してくれた", 35);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「実はね　最近ここのオーナーが亡くなったんだ」", 40);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル：「でね　これからのオーナーは誰なのか　オーナー争いが始まっちゃったの..」", 38);
            Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    少しため息交じりに話してくれた", 35);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}：「でも　なんで君が落ち込む必要があるのさ」", 40);
            Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「それがね　オーナーは私の..」", 40);
            Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    カランカラン", 60);
            Thread.Sleep(1500);
            Console.Clear();
            TypewriterEffect("\n\n    入り口を見るとそこには黒服の男が立っていた", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect($"\n\n    黒服の男：「おい　{playerName}!! 確か借金を滞納していたなぁ！！」", 38);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「えぇ；　そうなの？」", 40);
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}：「いやいや！　滞納なんかしたことないし身に覚えもないよ；；」", 38);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    と言ってみたものの　実際にあるかもしれない..", 35);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    ...何故だ？　なぜ私は逃げようと...", 35);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    なおのこと堂々としていた方がいいのではないのだろうか？", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            TypewriterEffect("\n\n    まずい　このままでは", 35);
            Thread.Sleep(1000);
            TypewriterEffect("\n    最悪な状況だ...", 35);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「..ふっ」", 45);
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ？", 60);
            Thread.Sleep(1500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「ふはははは！　冗談だよ！　冗談！　はははは！」", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「なんなんですか？　冷やかしなら帰ってください！」", 40);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    怒りをあらわにしながら注意をすると　黒服の男は冷静になった", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「すまんな　話が合ってきたんだ」", 40);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    黒服の男：「お前たちも知っての通り　このカジノにはオーナーがいない」", 38);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    黒服の男：「ならばこの俺が　なってやろうじゃないか！　って話さ」", 38);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    なんとなくこの先が手に取って見える..", 35);
            Thread.Sleep(1500);
            TypewriterEffect("\n    わかってるよ　俺に入れろよって話だろうな...", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「俺に入れろ！」", 45);
            Thread.Sleep(1500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ほ～ら　やっぱり；；", 35);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}：「嫌と言ったら？」", 45);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「俺の口から聞きたいか？」", 40);
            Thread.Sleep(1800);
            TypewriterEffect("\n\n    黒服の男：「風のうわさになって聞いた方がいいだろう」", 38);
            Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    といい終わって「じゃ」っといって店をあとにして行った", 35);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「はぁ～　やっぱりあの人嫌い」", 40);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    なんとなく気まずい空気になってしまって", 35);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    軽くあいさつを交わし　店をあとにした...", 35);
            Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         Chapter 1");
            Console.WriteLine("         「最初の会話」");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            blackSuitIntroduced = true;
            if (!unlockedEvents.Contains("チャプター1完了"))
                unlockedEvents.Add("チャプター1完了");
        }

        static void InnocentGemFound()
        {
            Console.Clear();
            Thread.Sleep(800);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    目が覚めると", 42);
            Thread.Sleep(1800);
            TypewriterEffect("\n\n    足元に　何かが光っていた", 42);
            Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    拾い上げると", 42);
            Thread.Sleep(1800);
            TypewriterEffect("\n\n    宝石だった", 44);
            Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    色がない", 44);
            Thread.Sleep(1500);
            TypewriterEffect("\n    形も　特にない", 42);
            Thread.Sleep(1800);
            TypewriterEffect("\n\n    でも　なんでも取り込んでしまいそうな", 40);
            Thread.Sleep(2000);
            TypewriterEffect("\n    美しい宝石だった", 42);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         アイテム入手！");
            Console.WriteLine("         「無垢な宝石」");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n         それはただの無。");
            Console.WriteLine("         色も形も特にない。");
            Console.WriteLine("         だが、なんでも取り込んでしまいそうな");
            Console.WriteLine("         美しい宝石。");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(3500);
            hasInnocentGem = true;
            if (!unlockedEvents.Contains("無垢な宝石入手"))
                unlockedEvents.Add("無垢な宝石入手");
        }

        static void ShopHiddenPage()
        {
            Console.Clear();
            Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ページをめくると", 45);
            Thread.Sleep(1500);
            TypewriterEffect("\n    そこだけ　少し空気が違った", 45);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n    ╔═══════════════════════════════╗");
            Console.WriteLine("    ║        ？？？ページ           ║");
            Console.WriteLine("    ╚═══════════════════════════════╝");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    ┌─────────────────────────┐");
            Console.WriteLine("    │  虚栄のカギ              │");
            Console.WriteLine("    │  価格：3000G             │");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("    │  夢も希望もない場所への  │");
            Console.WriteLine("    │  一歩。どこか冷たい鍵。  │");
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("    └─────────────────────────┘");
            Console.WriteLine("\n    [1] 購入する（3000G）");
            Console.WriteLine("    [0] 戻る");
            Console.Write("\n    > ");
            Console.ResetColor();
            var key = Console.ReadKey(true);
            if (key.KeyChar != '1') return;
            if (money < 3000)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                TypewriterEffect("\n\n    所持金が足りない...", 40);
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }
            money -= 3000;
            vanityKeyPurchased = true;
            abandonedCasinoUnlocked = true;
            Console.Clear();
            Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    会計をしようとすると", 40);
            Thread.Sleep(1500);
            TypewriterEffect("\n    ベルがそのカギをじっと見た", 40);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...こんなの　店に出した覚えないけど」", 42);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「どこから出てきたんだろ　これ」", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    少し間があった", 40);
            Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ねえ」", 45);
            Thread.Sleep(1500);
            TypewriterEffect("\n\n    ベル「そのカギ　どこに繋がってるか　確かめてみたくない？」", 40);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「一緒に行ってみようよ♪」", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...どこ行くんだよ」", 42);
            Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「わかんない♪　でもなんか　知ってる気がするんだよね」", 40);
            Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「...不思議でしょ」", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         虚栄のカギ　入手");
            Console.WriteLine("         廃娯楽施設が解放された");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(3500);
            if (!unlockedEvents.Contains("廃娯楽施設解放"))
                unlockedEvents.Add("廃娯楽施設解放");
        }

        static void BuyExchangedMoney()
        {
            Console.Clear();
            Thread.Sleep(500);
            if (money < 5000)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                TypewriterEffect("\n\n    所持金が足りない...", 40);
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine("\n\n    ┌─────────────────────────┐");
            Console.WriteLine("    │  換金したお金            │");
            Console.WriteLine("    │  価格：5000G             │");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("    │  見たことない額のお金。  │");
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine("    └─────────────────────────┘");
            Console.ResetColor();
            Console.WriteLine("\n    [1] 購入する");
            Console.WriteLine("    [0] やめる");
            Console.Write("\n    > ");
            var key = Console.ReadKey(true);
            if (key.KeyChar != '1') return;
            money -= 5000;
            hasExchangedMoney = true;
            Console.Clear();
            Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    お金を受け取った", 42);
            Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    見たことない額だった", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect("\n\n    これでカジノは　俺のものだ", 42);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    そう思った瞬間", 42);
            Thread.Sleep(1800);
            Console.Clear();
            TypewriterEffect("\n\n    ベルが　こちらを見ていた", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...そっか」", 42);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「そういう人だったんだ」", 40);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　カウンターの奥に引っ込んだ", 40);
            Thread.Sleep(2000);
            TypewriterEffect("\n    それ以上　何も言わなかった", 42);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         BAD END");
            Console.WriteLine("         「そういう人だったんだ」");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            if (!unlockedEvents.Contains("バッドエンド:カジノを乗っ取る"))
                unlockedEvents.Add("バッドエンド:カジノを乗っ取る");
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    気づくと　自分が黒服を着ていた", 40);
            Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    カジノのオーナーになった", 42);
            Thread.Sleep(2000);
            TypewriterEffect("\n\n    でも　何も変わらなかった", 42);
            Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    スロットの音だけが　鳴り続けていた", 40);
            Thread.Sleep(2500);
            Console.Clear();
            Console.ResetColor();
        }

        static void EnterAbandonedCasino()
        {
            if (!hasInnocentGem)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    カギを差し込んだが", 42);
                Thread.Sleep(1800);
                TypewriterEffect("\n\n    扉は　開かなかった", 42);
                Thread.Sleep(2000);
                Console.Clear();
                Console.ResetColor();
                return;
            }
            Console.Clear();
            Thread.Sleep(500);
            if (!abandonedCasinoEntered)
            {
                abandonedCasinoEntered = true;
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n\n    カギを使うと", 45);
                Thread.Sleep(1500);
                TypewriterEffect("\n    重い扉が　ゆっくりと開いた", 45);
                Thread.Sleep(2000);
                Console.Clear();
                TypewriterEffect("\n\n    埃っぽい空気が　流れてきた", 45);
                Thread.Sleep(2000);
                TypewriterEffect("\n\n    古い照明が　かろうじて灯っている", 45);
                Thread.Sleep(2000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("\n\n    ベル「...わあ」", 48);
                Thread.Sleep(1800);
                TypewriterEffect("\n\n    ベル「すごいね　こんな場所あったんだ」", 42);
                Thread.Sleep(2000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    錆びたスロットマシンが並んでいる", 42);
                Thread.Sleep(1800);
                TypewriterEffect("\n    天井の蛍光灯が　ひとつ　点滅している", 42);
                Thread.Sleep(2000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("\n\n    ベル「なんか...懐かしい気がする」", 42);
                Thread.Sleep(2000);
                TypewriterEffect("\n\n    ベル「来たことないはずなのに」", 42);
                Thread.Sleep(2200);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.White;
                TypewriterEffect($"\n\n    {playerName}「大丈夫か？」", 42);
                Thread.Sleep(1800);
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("\n\n    ベル「うん♪　大丈夫　なんか　面白いじゃん」", 40);
                Thread.Sleep(2200);
                TypewriterEffect("\n\n    ベル「行ってみようよ」", 42);
                Thread.Sleep(2000);
                Console.Clear();
                Console.ResetColor();
            }
            AbandonedCasinoFloor1();
        }

        static void PrintRoomOption(int num, string name, int cost, bool opened)
        {
            if (opened)
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine($"  [{num}] {name,-16}… 開放済み");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"  [{num}] {name,-16}… {cost}G");
            }
            Console.ResetColor();
        }

        static void OpenRoom(int floor, int room, int cost, Action roomEvent)
        {
            if (roomsOpened[floor].Length <= room)
            {
                var newArr = new bool[room + 1];
                roomsOpened[floor].CopyTo(newArr, 0);
                roomsOpened[floor] = newArr;
            }
            if (roomsOpened[floor][room]) { roomEvent(); return; }
            if (cost > 0 && money < cost)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Red;
                TypewriterEffect("\n\n    お金が足りない...", 40);
                Console.ResetColor();
                Thread.Sleep(1500);
                return;
            }
            if (cost > 0)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect($"\n\n    {cost}G　支払った", 40);
                Thread.Sleep(1500);
                money -= cost;
            }
            roomsOpened[floor][room] = true;
            roomEvent();
        }

        static void ExitAbandonedCasino()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「また来ようね♪」", 42);
            Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    重い扉が　閉まった", 42);
            Thread.Sleep(2000);
            Console.Clear();
            Console.ResetColor();
        }

        static void AbandonedCasinoFloor1()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n    ══════════════════════════════");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("          廃娯楽施設　1階");
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("    ══════════════════════════════");
                Console.ResetColor();
                Console.WriteLine($"\n    所持金：{money:N0}G\n");
                bool r0 = roomsOpened[0].Length > 0 && roomsOpened[0][0];
                bool r1 = roomsOpened[0].Length > 1 && roomsOpened[0][1];
                bool r2 = roomsOpened[0].Length > 2 && roomsOpened[0][2];
                bool r3 = roomsOpened[0].Length > 3 && roomsOpened[0][3];
                bool r4 = roomsOpened[0].Length > 4 && roomsOpened[0][4];
                bool allOpened = r0 && r1 && r2 && r3;
                PrintRoomOption(1, "錆びた扉の先", 1500, r0);
                PrintRoomOption(2, "薄暗い通路", 500, r1);
                PrintRoomOption(3, "古い休憩室", 500, r2);
                PrintRoomOption(4, "奥の部屋", 500, r3);
                if (allOpened) PrintRoomOption(5, "最奥の扉", 800, r4);
                else { Console.ForegroundColor = ConsoleColor.DarkGray; Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???"); Console.ResetColor(); }
                if (r4) { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine("  [6] 階段（2階へ）　　　　　… 1500G"); Console.ResetColor(); }
                Console.WriteLine("\n  [0] 廃娯楽施設を出る");
                Console.Write("\n  > ");
                var key = Console.ReadKey(true);
                switch (key.KeyChar)
                {
                    case '1': OpenRoom(0, 0, 1500, Room1F_A); break;
                    case '2': OpenRoom(0, 1, 500, Room1F_B); break;
                    case '3': OpenRoom(0, 2, 500, Room1F_C); break;
                    case '4': OpenRoom(0, 3, 500, Room1F_D); break;
                    case '5': if (allOpened) OpenRoom(0, 4, 800, Room1F_Final); break;
                    case '6':
                        if (r4) { if (money < 1500) { Console.Clear(); Console.ForegroundColor = ConsoleColor.Red; TypewriterEffect("\n\n    お金が足りない...", 40); Console.ResetColor(); Thread.Sleep(1500); break; } money -= 1500; GoToFloor2(); }
                        break;
                    case '0': ExitAbandonedCasino(); return;
                }
            }
        }

        static void Room1F_A()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    埃っぽい小部屋だった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    壁に　何かが貼ってある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「あ　なんか貼ってある♪」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「絵じゃん　子供が描いたやつ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    クレヨンで描かれた絵だ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    小さな女の子が　一人で立っている", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    周りには　誰もいない", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    でも　女の子は笑っている", 42); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    足元に　小さな鈴が描いてある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...笑ってるんだ　その子」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「ああ　めちゃくちゃ笑ってる」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「一人なのに？」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「一人なのに」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...なんか　わかる気がする」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「一人でも　別に　さみしくなかった時期ってあるじゃん」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...お前の話か？」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「さあ♪　どうだろ」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「でも　なんか　懐かしい感じがする」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが少し笑った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    その絵の女の子みたいに", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片A入手")) unlockedEvents.Add("断片A入手");
        }

        static void Room1F_B()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    薄暗い通路の奥に　小部屋があった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    床に　何かが落ちている", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 拾って見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    小さな靴だ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    子供用の　片方だけ", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    もう片方は　どこにもない", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「片方だけ？」", 42); Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「ああ　もう片方はない」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...どこ行ったんだろ　もう片方」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが靴を受け取って　じっと見た", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「捨てた側か　なくした側かで　全然違う話だよね」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルがその靴を　元あった場所に　そっと戻した", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...なんか　置いてかれた感じがするね　この靴」", 38); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「まあ　いっか♪　次行こ」", 42); Thread.Sleep(2000);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片B入手")) unlockedEvents.Add("断片B入手");
        }

        static void Room1F_C()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    古い休憩室だった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    テーブルが一つ　椅子が二つ", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    壁に　また絵が貼ってある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    手が二つ　描いてある", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    大きい手と　小さい手が　繋がっている", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    絵の下に　小さく文字が書いてある", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    「あたたかかった」", 48); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...あたたかかった」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「誰かに手を引いてもらったんだろうな」", 40); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...その人　好きだったんだと思う　この子」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「今もいるのかな　その人」", 42); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「いないんじゃないかな」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　椅子に少し寄りかかった", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でも　あたたかかったって　覚えてるんだよ　この子」", 38); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「それって　いいことじゃん♪」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...強いな　お前」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「え♪　急に何」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「この子の話してるんだけど」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが笑った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    でも　少しだけ　目が笑ってなかった", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片C入手")) unlockedEvents.Add("断片C入手");
        }

        static void Room1F_D()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    奥の部屋は　他より少し広かった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    何もない部屋だ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    でも　床の真ん中に　一枚だけ紙が落ちている", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 紙を拾って読む\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    古い紙だ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    文字が書いてある", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    「ベル」", 55); Thread.Sleep(2500);
            TypewriterEffect("\n\n    それだけだ", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ベル？」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「お前と同じ名前だな」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「誰かがこの名前を　誰かのために書いたんだ」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　その紙を　大事そうに折りたたんだ", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「もらっていい？　これ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「ここのものだろ　お前が持ってていいんじゃないか」", 38); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん♪」", 42); Thread.Sleep(2000);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片D入手")) unlockedEvents.Add("断片D入手");
        }

        static void Room1F_Final()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    最奥の扉を開けると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    壁一面に　絵が貼ってある", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    さっきの絵が　ここにもある", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    笑ってる女の子", 42); Thread.Sleep(1500);
            TypewriterEffect("\n    大きな手と小さな手", 42); Thread.Sleep(1500);
            Console.Clear();
            TypewriterEffect("\n\n    床には　あの靴が　今度は両方揃って置いてある", 40); Thread.Sleep(2200);
            TypewriterEffect("\n    隣に　小さな鈴が一つ", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    壁の真ん中に　大きな紙が貼ってある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect("\n\n    「ベルへ", 48); Thread.Sleep(1500);
            TypewriterEffect("\n\n     あなたが笑っていられますように", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n     どこにいても　あなたはベルだから」", 42); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...あ」", 52); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「これ」", 48); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「全部　私のだ」", 46); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...知ってたか？」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「知らなかった」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「でも　なんか　わかった気がする」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「誰かが　私のことを　思ってくれてたってこと」", 38); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「捨てられたって思ってたけど」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「...ちゃんと　思われてたんだ　私」", 40); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　鈴を一つ　そっと拾った", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「これ　持って帰っていい？」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「お前のもんだろ」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん♪」", 44); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが笑った", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    さっきより　少し　違う笑い方で", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         廃娯楽施設　1階");
            Console.WriteLine("         「ベルへ」　解放");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            memoryFragmentsCleared = true;
            if (!unlockedEvents.Contains("廃娯楽施設1階クリア"))
                unlockedEvents.Add("廃娯楽施設1階クリア");
        }

        static void GoToFloor2()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    階段を上ると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    2階は　1階より静かだった", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    空気が　少し重い", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「なんか　1階より緊張する」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「やめるか？」", 42); Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「ううん♪　行く」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「...なんか　知らないといけない気がして」", 38); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            AbandonedCasinoFloor2();
        }

        static void AbandonedCasinoFloor2()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n    ══════════════════════════════");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("          廃娯楽施設　2階");
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("    ══════════════════════════════");
                Console.ResetColor();
                Console.WriteLine($"\n    所持金：{money:N0}G\n");
                bool r0 = roomsOpened[1].Length > 0 && roomsOpened[1][0];
                bool r1 = roomsOpened[1].Length > 1 && roomsOpened[1][1];
                bool r2 = roomsOpened[1].Length > 2 && roomsOpened[1][2];
                bool r3 = roomsOpened[1].Length > 3 && roomsOpened[1][3];
                bool r4 = roomsOpened[1].Length > 4 && roomsOpened[1][4];
                bool allOpened = r0 && r1 && r2 && r3;
                PrintRoomOption(1, "重い扉", 2000, r0);
                PrintRoomOption(2, "細い廊下の先", 800, r1);
                PrintRoomOption(3, "窓のある小部屋", 800, r2);
                PrintRoomOption(4, "突き当たりの部屋", 800, r3);
                if (allOpened) PrintRoomOption(5, "最奥の扉", 1200, r4);
                else { Console.ForegroundColor = ConsoleColor.DarkGray; Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???"); Console.ResetColor(); }
                if (r4) { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine("  [7] 階段（3階へ）　　　　　… 2000G"); Console.ResetColor(); }
                Console.WriteLine("  [6] 1階に戻る");
                Console.WriteLine("  [0] 廃娯楽施設を出る");
                Console.Write("\n  > ");
                var key = Console.ReadKey(true);
                switch (key.KeyChar)
                {
                    case '1': OpenRoom(1, 0, 2000, Room2F_A); break;
                    case '2': OpenRoom(1, 1, 800, Room2F_B); break;
                    case '3': OpenRoom(1, 2, 800, Room2F_C); break;
                    case '4': OpenRoom(1, 3, 800, Room2F_D); break;
                    case '5': if (allOpened) OpenRoom(1, 4, 1200, Room2F_Final); break;
                    case '6': AbandonedCasinoFloor1(); return;
                    case '7':
                        if (r4) { if (money < 2000) { Console.Clear(); Console.ForegroundColor = ConsoleColor.Red; TypewriterEffect("\n\n    お金が足りない...", 40); Console.ResetColor(); Thread.Sleep(1500); break; } money -= 2000; GoToFloor3(); }
                        break;
                    case '0': ExitAbandonedCasino(); return;
                }
            }
        }

        static void Room2F_A()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    重い扉を開けると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ハンガーが一本　立っている", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    そこに　コートがかかっていた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] コートをよく見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    古いコートだ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    子供用の小さいサイズだ", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ポケットに小さな飴玉が一つ　包み紙ごと", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...飴」", 48); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「ポケットに入ってた」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...あ」", 48); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「思い出した」", 44); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　少し遠くを見た", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「雨の日だった」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「外で　ずっと座ってたら」", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「でかいコートの人が来て　これくれたんだ」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「その人が　拾ってくれたのか」", 40); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「何も言わずに　ただ飴だけくれて」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「それで　手を引いて歩いてくれた」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　飴玉をそっとポケットに戻した", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「このコート　あの人のだ　きっと」", 40); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片2A入手")) unlockedEvents.Add("断片2A入手");
        }

        static void Room2F_B()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    小さな部屋があった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    壁に絵が一枚　貼ってある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    テーブルを挟んで　二人が向き合って座っている絵だ", 38); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    一人は小さな子供　もう一人は大きな人", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    二人とも　笑っている", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ふふ」", 44); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「笑ってる」", 42); Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「毎日ご飯作ってくれたんだよね　あの人」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「うまかったか？」", 42); Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「おいしかった♪」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「全部おいしかった」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　絵の大きい人の方を指でなぞった", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「怒ったとこ　一回も見たことなかったな」", 38); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「ずっと笑ってた」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「いい人だったんだな」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「すごくいい人だった」", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片2B入手")) unlockedEvents.Add("断片2B入手");
        }

        static void Room2F_C()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    窓のある小部屋だった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    棚の上に　本が一冊置いてある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 本を手に取る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    古い本だ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ページを開くと　しおりが挟んである", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    ちょうど　半分あたりのページ", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    しおりの代わりに　小さなメモが挟んであった", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    「続きはまた今度」", 48); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...毎晩ね　眠くなるまで　読んでくれてた」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「半分で止まってる」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「ある朝　起きたら　いなかった」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「何も言わずに」", 42); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「この本も　置いてったんだ」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「続き　読めないまま」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルの声が　いつもより少しだけ　低かった", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でも　まあ♪」", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ベル「読んでもらえた分だけ　よかったんだと思う」", 38); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片2C入手")) unlockedEvents.Add("断片2C入手");
        }

        static void Room2F_D()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    突き当たりの部屋は　他より狭かった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    壁に　絵が一枚", 42); Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    椅子が一つ　描いてある", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    誰も座っていない", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    椅子だけが　真ん中に　ぽつんとある", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    絵の下に　文字が書いてある", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    「いなくなった」", 48); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...」", 52); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「描いたのか　自分で」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...たぶん」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「さみしかったんだろうな　その子」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...お前じゃないのか」", 42); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「さあ♪」", 44); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ベル「でも　この椅子　誰かのために取っといたんだと思う」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「また来るかもって」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「来なかったけどね」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　小さく息を吐いた", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でも　いい人だったから　いっか♪」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「次行こ」", 44); Thread.Sleep(1800);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片2D入手")) unlockedEvents.Add("断片2D入手");
        }

        static void Room2F_Final()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    最奥の扉を開けると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    部屋の中に　テーブルが一つあった", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    あのコートが　椅子の背にかかっている", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    テーブルに　例の本が置いてある", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    テーブルの端に　小さなメモが一枚", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    「また来る　待ってろ」", 48); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...また来る」", 44); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　そのメモをじっと見た", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「待ってたんだ　私」", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「来なかったけど　ずっと待ってた」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...」", 52); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でもさ」", 44); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ベル「書いてくれてたんだよ　ちゃんと」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「また来るって」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「それだけでいいのか」", 42); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...十分じゃん♪」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　コートのポケットを触った", 42); Thread.Sleep(2200);
            TypewriterEffect("\n    飴玉が　まだそこにあった", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「ねえ　これ食べていい？」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「古いだろそれ」", 42); Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「いいじゃん別に♪」", 42); Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　飴を口に入れた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...あまい」", 44); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「ちゃんと　あまい」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　小さく笑った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    泣いてるのか笑ってるのか　わからない顔で", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         廃娯楽施設　2階");
            Console.WriteLine("         「また来る」　解放");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            if (!unlockedEvents.Contains("廃娯楽施設2階クリア"))
                unlockedEvents.Add("廃娯楽施設2階クリア");
        }

        static void GoToFloor3()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    階段を上ると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    3階は　暗かった", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    照明がほとんど切れている", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    煙草と　何か腐ったものの匂いが　残っていた", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...」", 52); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「知ってる場所か」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　いつもと違う顔をしていた", 42); Thread.Sleep(2200);
            TypewriterEffect("\n    笑っていない", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...行こ」", 44); Thread.Sleep(2000);
            Console.Clear(); Console.ResetColor();
            AbandonedCasinoFloor3();
        }

        static void AbandonedCasinoFloor3()
        {
            while (true)
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("\n\n    ══════════════════════════════");
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("          廃娯楽施設　3階");
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.WriteLine("    ══════════════════════════════");
                Console.ResetColor();
                Console.WriteLine($"\n    所持金：{money:N0}G\n");
                bool r0 = roomsOpened[2].Length > 0 && roomsOpened[2][0];
                bool r1 = roomsOpened[2].Length > 1 && roomsOpened[2][1];
                bool r2 = roomsOpened[2].Length > 2 && roomsOpened[2][2];
                bool r3 = roomsOpened[2].Length > 3 && roomsOpened[2][3];
                bool r4 = roomsOpened[2].Length > 4 && roomsOpened[2][4];
                bool allOpened = r0 && r1 && r2 && r3;
                PrintRoomOption(1, "鉄扉", 3000, r0);
                PrintRoomOption(2, "廊下の突き当たり", 1000, r1);
                PrintRoomOption(3, "裏の小部屋", 1000, r2);
                PrintRoomOption(4, "通用口の先", 1000, r3);
                if (allOpened) PrintRoomOption(5, "最奥の扉", 2000, r4);
                else { Console.ForegroundColor = ConsoleColor.DarkGray; Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???"); Console.ResetColor(); }
                if (r4) { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine("  [7] 出口へ"); Console.ResetColor(); }
                Console.WriteLine("  [6] 2階に戻る");
                Console.WriteLine("  [0] 廃娯楽施設を出る");
                Console.Write("\n  > ");
                var key = Console.ReadKey(true);
                switch (key.KeyChar)
                {
                    case '1': OpenRoom(2, 0, 3000, Room3F_A); break;
                    case '2': OpenRoom(2, 1, 1000, Room3F_B); break;
                    case '3': OpenRoom(2, 2, 1000, Room3F_C); break;
                    case '4': OpenRoom(2, 3, 1000, Room3F_D); break;
                    case '5': if (allOpened) OpenRoom(2, 4, 2000, Room3F_Final); break;
                    case '6': AbandonedCasinoFloor2(); return;
                    case '7': if (r4) { AbandonedCasinoExit(); return; } break;
                    case '0': ExitAbandonedCasino(); return;
                }
            }
        }

        static void Room3F_A()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    鉄扉の向こうは　フロアだった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    スロットマシンが並んでいる", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    カウンターの内側に　何かが引っかかっている", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 取って見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    エプロンだ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ひどく使い込まれている", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    子供用の小さいサイズだ", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    胸のあたりに　茶色い染みがある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「それ　私のだ」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「子供のころから　ここで働いてたのか」", 38); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「雇ってもらえたから」", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「他に行く場所　なかったし」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「どんな仕事をしてたんだ」", 42); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...なんでも」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「言われたことは　全部やってた」", 40); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「...それだけじゃ　ないこともあったけど」", 36); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　そこで言葉を止めた", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「聞かないで」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    静かに言った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    ただ　話せないだけだ　という顔だった", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...次　行こ」", 42); Thread.Sleep(2200);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片3A入手")) unlockedEvents.Add("断片3A入手");
        }

        static void Room3F_B()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    廊下の突き当たりに　絵が一枚　貼ってあった", 38); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 絵を見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    小さな子が　トレーを持って立っている絵だ", 38); Thread.Sleep(2200);
            TypewriterEffect("\n\n    顔のところが　黒いクレヨンで　ぐるぐると塗りつぶされている", 36); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    周りに　大人が何人か描いてある", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    全員　笑っている", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「顔　塗りつぶしてあるね」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「描きたくなかったのか」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...どんな顔してたか　わかんなかったんじゃないかな」", 34); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「自分の顔が　わかんない？」", 40); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「笑えって言われてたから　笑ってたけど」", 36); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「...本当に笑ってたかどうかは　わかんない」", 36); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...今は　わかるか」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...今は」", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「笑ってるときは　笑ってるってわかる」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    それだけ言って　ベルは黙った", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片3B入手")) unlockedEvents.Add("断片3B入手");
        }

        static void Room3F_C()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    裏の小部屋は　物置だった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    棚にがらくたが積んである", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    その中に　金属の光るものがあった", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 取り出して見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ネームプレートだ", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    二つに折れている", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    読める部分は「ベ」だけだ", 46); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ああ　これ」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「折られたのか」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「うん」", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「名前なんかいらないって」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「客に名前で呼ばれたら　なれなれしいから」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「じゃあ　なんて呼ばれてたんだ」", 40); Thread.Sleep(2200);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「おい　とか　お前　とか」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「...気に入った客はベルって呼んでくれたけど」", 34); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　そのネームプレートを両手で持った", 38); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「合わせたら　ベルって読めるから」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「...それでよかった」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　折れたネームプレートを　ポケットにしまった", 36); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片3C入手")) unlockedEvents.Add("断片3C入手");
        }

        static void Room3F_D()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    通用口の先に　小さな部屋があった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    窓がない", 44); Thread.Sleep(1800);
            TypewriterEffect("\n    鍵穴だけある　外から鍵をかける仕様の扉が一つ", 36); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「ここで　寝てた」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...外から　鍵をかけられるのか　この扉」", 36); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「逃げないようにって」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　淡々と言った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    当たり前のことを言うように", 42); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    部屋の天井に　何かが描いてある", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 天井を見る\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    星だ", 46); Thread.Sleep(2000);
            TypewriterEffect("\n\n    天井いっぱいに　星が描いてある", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    クレヨンで　一つひとつ　丁寧に", 42); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    窓がない部屋なのに", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    天井だけ　夜空だ", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「暗くて　怖かったから」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「星があれば　外にいる気がするかなって」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...何歳のときだ　これ描いたの」", 38); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...何歳からかな」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　天井を見上げた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「きれいでしょ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    きれいだと思った", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    同時に　胸が痛かった", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...ああ　きれいだ」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「でしょ♪」", 44); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　初めて笑った", 42); Thread.Sleep(2000);
            TypewriterEffect("\n    3階に来てから　初めて", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("断片3D入手")) unlockedEvents.Add("断片3D入手");
        }

        static void Room3F_Final()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    最奥の扉を開けると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    オーナー室だった", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    机の上に　ものが並べてある", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    たたまれたエプロン", 42); Thread.Sleep(1500);
            TypewriterEffect("\n    折れたネームプレート", 42); Thread.Sleep(1500);
            TypewriterEffect("\n    誰かが描いた　顔のない絵", 42); Thread.Sleep(1800);
            Console.Clear();
            TypewriterEffect("\n\n    引き出しが　少し開いていた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 引き出しを開ける\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    封筒が一つ入っていた", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    「ベルへ」", 52); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...」", 55); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「開けるか」", 44); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...開けて」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect("\n\n    「ベルへ", 50); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n     俺がお前にしたことは　最低だった", 44); Thread.Sleep(2500);
            TypewriterEffect("\n\n     わかっていた　やめなかった", 44); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n     お前がいたから　ここは回っていた", 42); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n     名前を折ったこと　謝る", 44); Thread.Sleep(2200);
            TypewriterEffect("\n\n     鍵をかけたこと　謝る", 44); Thread.Sleep(2200);
            TypewriterEffect("\n\n     それ以外のことも　全部」", 44); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...」", 55); Thread.Sleep(3500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　動かなかった", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「謝られても」", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「...もう死んでんじゃん」", 40); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルの声が　震えていた", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「許してあげたかったのに」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「直接　言えなかった」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    泣いていた", 44); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...手紙　置いてく」", 42); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「ここのものだから　ここにあっていい」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　手紙を机に戻した", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...来てくれてよかった」", 40); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         廃娯楽施設　3階");
            Console.WriteLine("         「来てくれてよかった」　解放");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            if (!unlockedEvents.Contains("廃娯楽施設3階クリア"))
                unlockedEvents.Add("廃娯楽施設3階クリア");
        }

        static void AbandonedCasinoExit()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    出口へ向かった", 42); Thread.Sleep(2000);
            Console.Clear();
            if (timeClockEquipped)
            {
                TypewriterEffect("\n\n    廊下を歩いていると", 42); Thread.Sleep(1800);
                TypewriterEffect("\n\n    何かが　引っかかった", 42); Thread.Sleep(2000);
                Console.Clear();
                TypewriterEffect("\n\n    壁の一部が　他と少し違う", 42); Thread.Sleep(2000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Cyan;
                TypewriterEffect("\n\n    ベル「...あそこ　なんか変じゃない？」", 40); Thread.Sleep(2200);
                Console.Clear();
                BasementDoorFound();
                return;
            }
            AbandonedCasinoExitEvent();
        }

        static void AbandonedCasinoExitEvent()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    重い扉を開けると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    外の空気が流れてきた", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    黒服の男が　壁に寄りかかっていた", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「遅かったな」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    黒服の男：「全部　見てきたか」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...お前が待ってたのか」", 42); Thread.Sleep(2000);
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「当たり前だろ　俺のカジノなんだから」", 36); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル：「遺言で　私がオーナーって　決まってたのに」", 36); Thread.Sleep(2800);
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「だから　消えてもらった」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服が　ゆっくりと近づいてきた", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;
            TypewriterEffect("\n\n    ベル「...っ」", 44); Thread.Sleep(1500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    音がした", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベルが　崩れ落ちた", 42); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    playerは　動けなかった", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ごめん」", 44); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    それだけ言って", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ベルは　動かなくなった", 42); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkRed;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         ENDING");
            Console.WriteLine("         「ごめん」");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Thread.Sleep(4000);
            Console.Clear(); Console.ResetColor();
            if (!unlockedEvents.Contains("バッドエンド:ごめん"))
                unlockedEvents.Add("バッドエンド:ごめん");
        }

        static void BasementDoorFound()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    壁を押すと　重い音がして", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    隠し扉が　開いた", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    階段が　下に続いている", 42); Thread.Sleep(1800);
            TypewriterEffect("\n    暗い　かなり深い", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...なんだろ　ここ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 降りる\n    [0] 戻る"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            BasementEvent();
        }

        static void BasementEvent()
        {
            if (!hasInnocentGem) { ExitAbandonedCasino(); return; }
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    階段を降りると", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    冷たい空気が　体を包んだ", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    広い部屋だった", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    中央に　白い布が　かけられている", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    [1] 布をめくる\n    [0] やめる"); Console.Write("\n    > "); Console.ResetColor();
            if (Console.ReadKey(true).KeyChar != '1') return;
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    布の下に　人が横たわっていた", 42); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    小さい", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    よく知っている顔だった", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...」", 55); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「これは　お前じゃないか」", 40); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...うん」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「私だ」", 44); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「なんで　お前が殺されなきゃいけなかったんだ」", 34); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「オーナーの遺言で　私がここの次のオーナーって　決まってたから」", 32); Thread.Sleep(3000);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「あの人　それが嫌だったんだよね」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　笑おうとした", 42); Thread.Sleep(1800);
            TypewriterEffect("\n\n    笑えなかった", 44); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「なんか　あっけないよね", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「やっと　自分の場所だって思ってたのに」", 36); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルの声が　少し　揺れた", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「怖かったんだよ　本当は」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「ずっと　どこかに捨てられるんじゃないかって」", 34); Thread.Sleep(3000);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「笑ってれば　大丈夫だって思ってたから　笑ってた」", 34); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルが　亡骸から目を逸らした", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...でも　結局こうなった」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「笑ってても　捨てられた」", 40); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルの声が　震えていた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...悔しい」", 44); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「あなたと一緒にいて　初めて　笑えてた気がしてたのに」", 32); Thread.Sleep(3200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「みっともなくない」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    しばらく　何も言わなかった", 42); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ポケットの中が　光った", 42); Thread.Sleep(2200);
            Console.Clear();
            TypewriterEffect("\n\n    取り出すと　無垢な宝石だった", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...きれいだね」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「お前のものだろ　たぶん」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「...ねえ", 44); Thread.Sleep(1800);
            TypewriterEffect("\n\n    ベル「私　ここで終わりたくない」", 40); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「あなたのそばにいたい」", 40); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「まだ　一緒にいたい」", 42); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...来い」", 46); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            TypewriterEffect("\n\n    ベル「一生ついてく」", 46); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「どこにいても　ずっと　絶対」", 40); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    宝石が　強く光った", 42); Thread.Sleep(1800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            for (int i = 0; i < 4; i++)
            {
                Console.Clear();
                Console.WriteLine(i % 2 == 0 ? "\n\n\n\n         ✦" : "\n\n\n\n      ✦     ✦");
                Thread.Sleep(300);
            }
            Console.Clear();
            Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    ベルの姿が　宝石に吸い込まれていった", 38); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    宝石が　指輪に変わった", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「聞こえる？」", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「ちゃんと　ここにいるから」", 40); Thread.Sleep(2500);
            Console.Clear();
            TypewriterEffect("\n\n    ベル「だから　前向いて」", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         アイテム入手！");
            Console.WriteLine("         「宝石のついた指輪」");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("\n         ベルが宿る指輪。");
            Console.WriteLine("         これで君が救われるのであれば、");
            Console.WriteLine("         僕はすべてを背負う。");
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            hasInnocentGem = false;
            hasJewelRing = true;
            if (!unlockedEvents.Contains("宝石のついた指輪入手"))
                unlockedEvents.Add("宝石のついた指輪入手");
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    地下室を出た", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    黒服が　そこにいた", 42); Thread.Sleep(2500);
            Console.Clear(); Console.ResetColor();
            BlackSuitFinalConfrontation();
        }

        static void BlackSuitFinalConfrontation()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「...なんだ　お前」", 40); Thread.Sleep(2000);
            TypewriterEffect("\n\n    黒服の男：「なんでここに　いる」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服が　初めて　動揺した顔をした", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「全部　知ってる」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「...知って　どうする」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    黒服の男：「証拠もない　誰も信じない」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    指輪が　光った", 44); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「...私が証拠だよ」", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「な　...っ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「全部　覚えてるから」", 40); Thread.Sleep(2200);
            TypewriterEffect("\n\n    ベル「消えてても　忘れてないから」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服が　後退った", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("\n\n    どうする");
            Console.WriteLine("\n    [1] このカジノはベルのものだと言う");
            Console.WriteLine("    [2] 黒服を追い詰める");
            Console.Write("\n    > "); Console.ResetColor();
            var key = Console.ReadKey(true);
            if (key.KeyChar == '1') EndingRouteA_Owner();
            else EndingRouteB_Bell();
        }

        static void EndingRouteA_Owner()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「このカジノは　ベルのものだ」", 40); Thread.Sleep(2200);
            TypewriterEffect($"\n\n    {playerName}「遺言がそう言ってる　お前がなんと言おうと」", 34); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「...証明できるのか」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「できるよ♪」", 44); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「オーナーが書いた遺言書　地下室にあったから」", 34); Thread.Sleep(2800);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服の顔が　青ざめた", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「...くそっ」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服が　その場を去った", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「...やったね♪」", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「これからどうする　このカジノ」", 38); Thread.Sleep(2500);
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「あなたに任せる♪」", 42); Thread.Sleep(2000);
            TypewriterEffect("\n\n    ベル「私は　ここにいるから」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    指輪が　温かかった", 42); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         ENDING　A");
            Console.WriteLine("         「ここにいるから」");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            bellRouteACompleted = true;
            if (!unlockedEvents.Contains("エンディングA:ここにいるから"))
                unlockedEvents.Add("エンディングA:ここにいるから");
        }

        static void EndingRouteB_Bell()
        {
            Console.Clear(); Thread.Sleep(500);
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「お前がやったことは　消えない」", 38); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「だから　なんだ」", 40); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「このカジノは　私のものだった」", 38); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「でも　もういらない」", 42); Thread.Sleep(2200);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「ベル？」", 44); Thread.Sleep(1800);
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「こんな場所に縛られたくない」", 38); Thread.Sleep(2500);
            TypewriterEffect("\n\n    ベル「私は　あなたと行く」", 40); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    指輪が　強く光った", 42); Thread.Sleep(2000);
            Console.Clear();
            TypewriterEffect("\n\n    廃娯楽施設の壁に　ひびが入った", 40); Thread.Sleep(2000);
            TypewriterEffect("\n\n    天井が　崩れ始めた", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            TypewriterEffect("\n\n    黒服の男：「なんだ　なんなんだ　これは！」", 34); Thread.Sleep(2500);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    黒服が　逃げていった", 42); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Magenta;
            TypewriterEffect("\n\n    ベル「行こ♪」", 46); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.White;
            TypewriterEffect($"\n\n    {playerName}「...ああ」", 44); Thread.Sleep(2000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkGray;
            TypewriterEffect("\n\n    廃娯楽施設が　崩れていった", 40); Thread.Sleep(2000);
            TypewriterEffect("\n\n    指輪だけが　光っていた", 42); Thread.Sleep(3000);
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine("         ENDING　B");
            Console.WriteLine("         「行こ」");
            Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
            Console.ResetColor();
            Thread.Sleep(4000);
            bellRouteBCompleted = true;
            if (!unlockedEvents.Contains("エンディングB:行こ"))
                unlockedEvents.Add("エンディングB:行こ");
        }

        static void UnknownCoinFlip(int bet, int multiplier)
        {
            Console.Clear(); Thread.Sleep(300);
            Console.ForegroundColor = ConsoleColor.Yellow;
            TypewriterEffect("\n\n    ポケットの中で　何かが動いた", 42); Thread.Sleep(1500);
            Console.Clear();
            TypewriterEffect("\n\n    知らない硬貨が　宙に浮いている", 42); Thread.Sleep(1800);
            Console.Clear();
            string[] frames = { "  〇", "  ◎", "  ●", "  ◎", "  〇" };
            foreach (var f in frames) { Console.Clear(); Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine("\n\n\n\n" + f); Thread.Sleep(200); }
            Console.Clear(); Thread.Sleep(500);
            bool isFront = rand.Next(2) == 0;
            if (isFront)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                TypewriterEffect("\n\n    表", 60); Thread.Sleep(1000);
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    嘘は嘘", 50); Thread.Sleep(1000);
                TypewriterEffect("\n\n    それはくるりと　裏返る", 45); Thread.Sleep(1500);
                Console.Clear();
                int winAmount = bet * 2 * multiplier;
                money += winAmount;
                totalWinAmount += winAmount;
                consecutiveWins++;
                consecutiveLosses = 0;
                unknownCoinFlipCount++;
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━");
                Console.WriteLine("         外れが　裏返った！");
                Console.WriteLine($"         +{winAmount:N0}G");
                Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━");
                Console.ResetColor(); Thread.Sleep(2500);
         
                if (!unlockedEvents.Contains("コイントス成功")) unlockedEvents.Add("コイントス成功");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.DarkGray;
                TypewriterEffect("\n\n    裏", 60); Thread.Sleep(1000);
                Console.Clear();
                TypewriterEffect("\n\n    ...今回は　そのまま", 42); Thread.Sleep(1500);
                Console.Clear(); Console.ResetColor();
            }
        }
    }
}