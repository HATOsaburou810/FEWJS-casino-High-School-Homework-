# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — ミッション (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod

# ========== ミッション初期化 ==========

def InitializeMissions():
    # 既存ミッション（1-11）
    st.missions.append(Mission("初心者", "50G以下で1回勝利", lambda: st.consecutiveWins >= 1 and st.money <= 1050, 100))
    st.missions.append(Mission("連勝の始まり", "3連勝を達成", lambda: st.consecutiveWins >= 3, 200))
    st.missions.append(Mission("連勝マスター", "5連勝を達成", lambda: st.consecutiveWins >= 5, 500))
    st.missions.append(Mission("無借金主義", "借金せずに所持金2000G達成", lambda: st.money >= 2000 and st.debt == 0, 300))
    st.missions.append(Mission("777ハンター", "777を1回揃える", lambda: st.total777Count >= 1, 1000))
    st.missions.append(Mission("借金返済の達人", "借金を完済する", lambda: st.debt == 0 and st.hasEverBorrowedMoney, 300))
    st.missions.append(Mission("GODへの道", "100G連続10回プレイ", lambda: st.consecutiveHundredPlays >= 10, 200))
    st.missions.append(Mission("粘り強さ", "20回転連続でプレイ", lambda: st.totalSpins >= 20, 150))
    st.missions.append(Mission("強運の持ち主", "設定6を引き当てる", lambda: st.setting == 6, 500))
    st.missions.append(Mission("ギャンブラー", "総回転数100回達成", lambda: st.totalSpins >= 100, 1000))
    st.missions.append(Mission("強欲", "幸運のコインを10個購入", lambda: st.totalLuckyCoinsPurchased >= 10, 0))
    st.missions.append(Mission("破滅への道", "強欲の指輪装備中に借金5000G到達", lambda: st.greedRingEquipped and st.debt >= 5000, 0))
    # VIPルーム関連（12-15）
    st.missions.append(Mission("セレブへの道", "所持金10000G到達してVIPルーム解放", lambda: st.money >= 10000 and st.vipRoomUnlocked, 0))
    st.missions.append(Mission("VIPの洗礼", "VIPルームで初勝利", lambda: st.vipTotalWins >= 1, 1000))
    st.missions.append(Mission("ハイローラー", "VIPルームで5000Gベットで勝利", lambda: st.vip5000BetWin, 3000))
    st.missions.append(Mission("VIPマスター", "VIPルームで777を揃える", lambda: st.vip777Count >= 1, 5000))
    # 地下カジノ関連（16-20）
    st.missions.append(Mission("奈落への扉", "地下カジノを解放", lambda: st.undergroundUnlocked, 0))
    st.missions.append(Mission("地獄の訪問者", "地下カジノに初めて入る", lambda: st.undergroundVisits >= 1, 500))
    st.missions.append(Mission("奈落の生還者", "地下カジノで1回勝利", lambda: st.undergroundWins >= 1, 0))
    st.missions.append(Mission("闇の常連客", "地下カジノを5回訪問", lambda: st.undergroundVisits >= 5, 2000))
    st.missions.append(Mission("奈落の覇者", "地下カジノで全財産ベットして勝利", lambda: st.undergroundAllInWin, 10000))
    # 悪魔契約関連（21-24）
    st.missions.append(Mission("悪魔の誘惑", "悪魔から契約を提示される", lambda: st.devilContractOffered, 0))
    st.missions.append(Mission("契約者", "悪魔と契約する（種類問わず）", lambda: st.devilContractActive, 1500))
    st.missions.append(Mission("魂の代償", "契約1「魂の担保」で10連勝達成", lambda: st.contract1Complete, 5000))
    st.missions.append(Mission("悪魔を欺く者", "いずれかの契約を成功させる", lambda: st.devilContractSuccess, 0))
    # 中毒システム関連（25-29）
    st.missions.append(Mission("止まらない", "中毒度20到達", lambda: st.addictionLevel >= 20, 300))
    st.missions.append(Mission("依存症", "中毒度50到達", lambda: st.addictionLevel >= 50, 800))
    st.missions.append(Mission("末期症状", "中毒度80到達", lambda: st.addictionLevel >= 80, 0))
    st.missions.append(Mission("制御不能", "中毒度100到達", lambda: st.addictionLevel >= 100, 0))
    st.missions.append(Mission("更生の道", "リハビリ券で中毒度を50以下に下げる", lambda: st.hasUsedRehab and st.addictionLevel <= 50, 3000))
    # 呪いアイテム関連（30-35）
    st.missions.append(Mission("禁断の力", "呪いのアイテムを1つ入手", lambda: st.cursedItemCount >= 1, 500))
    st.missions.append(Mission("コレクター", "呪いのアイテムを3種類入手", lambda: st.cursedItemCount >= 3, 1500))
    st.missions.append(Mission("呪われし者", "呪いのアイテムを全種類入手", lambda: st.cursedItemCount >= 5, 0))
    st.missions.append(Mission("悪魔のささやき", "悪魔のコインで勝利", lambda: st.devilCoinWin, 1000))
    st.missions.append(Mission("血の契約", "血塗られたお守りを装備して5連勝", lambda: st.bloodAmulet5Wins >= 5, 2000))
    st.missions.append(Mission("死神との賭け", "死神の指輪で10回勝利", lambda: st.deathRing10Wins >= 10, 5000))
    # メタ・その他関連（36-40）
    st.missions.append(Mission("第四の壁", "メタ演出を3種類以上体験", lambda: st.metaEventCount >= 3, 2000))
    st.missions.append(Mission("真実を知る者", "全てのイベントを閲覧", lambda: len(st.unlockedEvents) >= 20, 3000))
    st.missions.append(Mission("完全主義者", "全ての絵柄を解放", lambda: len(st.unlockedSymbols) >= 8, 2000))
    st.missions.append(Mission("生存者", "借金20000G以上から完済", lambda: st.maxDebt >= 20000 and st.debt == 0, 10000))
    st.missions.append(Mission("伝説のギャンブラー", "全ミッション達成", lambda: sum(1 for m in st.missions if m.Completed) >= 40, 0))
    # 隠しミッション（41-46）
    st.missions.append(Mission("???", "???", lambda: st.totalLoses >= 100, 5000))
    st.missions.append(Mission("???", "???", lambda: st.consecutiveWins >= 20, 0))
    st.missions.append(Mission("???", "???", lambda: st.money == 6666, 0))
    st.missions.append(Mission("???", "???", lambda: st.totalSpins == 777, 0))
    st.missions.append(Mission("???", "???", lambda: sum(1 for m in st.missions if m.Completed) >= 44, 0))
    st.missions.append(Mission("???", "???", lambda: st.money >= 10000 and st.total777Count >= 3, 0))
# ========== ミッション関連 ==========

def ShowUncompletedMissions():
    uncompleted = py_filter_missions_uncompleted(st.missions)
    if len(uncompleted) > 0:
        Console.ForegroundColor = ConsoleColor.Cyan
        Console.WriteLine("\n【進行中ミッション】")
        for mission in uncompleted:
            Console.WriteLine(f"  ◆ {mission.Name}: {mission.Description}")
        Console.ResetColor()

def ShowAllMissions():
    st.missionOpenCount += 1
    # 読んでる？ミッション達成チェック
    if st.missionOpenCount == 10:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkMagenta
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("         隠しミッション発見！")
        Console.WriteLine("         「読んでる？」")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("\n    「気づいてたよ」")
        Thread.Sleep(1500)
        Console.WriteLine("    「ずっと見てたんだね」")
        Thread.Sleep(1500)
        Console.WriteLine("    「…ねえ、ミッション一覧って面白い？」")
        Thread.Sleep(1500)
        Console.WriteLine("\n    君はゲームを、ゲームとして楽しんでいる。それは…正しいことだ")
        Console.ResetColor()
        Thread.Sleep(4000)
    pageSize = 15
    # 1ページに表示する数
    page = 0
    totalPages = int(Math.Ceiling(len(st.missions) / float(pageSize)))
    while True:
        Console.clear()
        ui_mod.DrawTitle()
        Console.WriteLine(f"\n【ミッション一覧】  {page + 1}/{totalPages}ページ\n")
        start = page * pageSize
        end = Math.Min(start + pageSize, len(st.missions))
        for i in range(start, end):
            mission = st.missions[i]
            if mission.Completed:
                Console.ForegroundColor = ConsoleColor.Green
                if mission.Reward > 0:
                    Console.WriteLine(f"✓ {mission.Name}: {mission.Description} (報酬: {mission.Reward}G) [達成済み]")
                else:
                    Console.WriteLine(f"✓ {mission.Name}: {mission.Description} [達成済み]")
            else:
                if mission.Name == "???":
                    Console.ForegroundColor = ConsoleColor.DarkMagenta
                    Console.WriteLine(f"  ??? : ??? (報酬: ???)")
                else:
                    Console.ForegroundColor = ConsoleColor.White
                    if mission.Reward > 0:
                        Console.WriteLine(f"  {mission.Name}: {mission.Description} (報酬: {mission.Reward}G)")
                    else:
                        Console.WriteLine(f"  {mission.Name}: {mission.Description}")
            Console.ResetColor()
        Console.WriteLine("\n")
        if page > 0:
            Console.WriteLine("  [←] 前のページ")
        if page < totalPages - 1:
            Console.WriteLine("  [→] 次のページ")
        Console.WriteLine("  [0] 戻る")
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        if key.Key == ConsoleKey.LeftArrow and page > 0:
            page -= 1
        elif key.Key == ConsoleKey.RightArrow and page < totalPages - 1:
            page += 1
        elif key.KeyChar == "0":
            break
    # ShowAllMissions() の末尾、2つのブロックをこう置き換える
    # 中毒度増加（ミッション閲覧のごほうび的に1回だけ、少量）
    # ※そもそもミッション開閉で上げたくないなら丸ごと削除でOK
    if st.addictionLevel < 100:
        st.addictionLevel = Math.Min(100, st.addictionLevel + st.rand.Next(1, 3))
    CheckMissions()
# ========== ミッション達成チェック ==========

def CheckMissions():
    for idx in range(0, len(st.missions)):
        mission = st.missions[idx]
        if not mission.Completed and mission.CheckComplete != None and mission.CheckComplete():
            mission.Completed = True
            # 隠しミッションの名前解放（インデックスで判定）
            if mission.Name == "???":
                _sw6 = idx
                if _sw6 == 40:
                    mission.Name = "負け続ける者"
                    mission.Description = "累計負け100回"
                elif _sw6 == 41:
                    mission.Name = "無敵の男"
                    mission.Description = "20連勝達成"
                elif _sw6 == 42:
                    mission.Name = "666の刻印"
                    mission.Description = "所持金がピッタリ6666G"
                elif _sw6 == 43:
                    mission.Name = "運命の回転"
                    mission.Description = "総回転数がピッタリ777回"
                elif _sw6 == 44:
                    mission.Name = "ぼくがかんがえた、さいきょうのはいじん"
                    mission.Description = "全呪いアイテムを入手"
                elif _sw6 == 45:
                    mission.Name = "真の覇者"
                    mission.Description = "所持金10000G以上かつ777を3回"
            # 達成演出（???のまま解放できなかった場合は表示しない）
            if mission.Name != "???":
                if mission.Reward > 0:
                    st.money += mission.Reward
                # バッジの種類を報酬額で決定
                isHidden = idx >= 40
                isLegend = mission.Name == "伝説のギャンブラー"
                Console.clear()
                if isLegend:
                    # 伝説バッジ（超豪華）
                    for f in range(0, 6):
                        Console.clear()
                        Console.ForegroundColor =(ConsoleColor.Yellow if f % 2 == 0 else ConsoleColor.White)
                        Console.BackgroundColor =(ConsoleColor.DarkYellow if f % 2 == 0 else ConsoleColor.Black)
                        Console.WriteLine("\n\n")
                        Console.WriteLine("  ╔══════════════════════════════════════════════════════╗")
                        Console.WriteLine("  ║                                                      ║")
                        Console.WriteLine("  ║   ★ ★ ★   全ミッション達成！！！   ★ ★ ★      ║")
                        Console.WriteLine("  ║        あなたは伝説のギャンブラーだ                  ║")
                        Console.WriteLine("  ║                                                      ║")
                        Console.WriteLine("  ╚══════════════════════════════════════════════════════╝")
                        Console.ResetColor()
                        Thread.Sleep(300)
                    Thread.Sleep(1000)
                elif isHidden:
                    # 隠しミッションバッジ
                    Console.BackgroundColor = ConsoleColor.DarkMagenta
                    Console.ForegroundColor = ConsoleColor.White
                    Console.WriteLine("\n\n")
                    Console.WriteLine("  ╔══════════════════════════════════════════════╗")
                    Console.WriteLine("  ║                                              ║")
                    Console.WriteLine("  ║   ？？？  隠しミッション解放！  ？？？      ║")
                    Console.WriteLine(f"  ║   【{(mission.Name).ljust(int(20))}】        ║")
                    Console.WriteLine(f"  ║   {(mission.Description).ljust(int(30))}      ║")
                    if mission.Reward > 0:
                        Console.WriteLine(f"  ║   報酬: +{mission.Reward:>6}G                            ║")
                    Console.WriteLine("  ║                                              ║")
                    Console.WriteLine("  ╚══════════════════════════════════════════════╝")
                    Console.ResetColor()
                elif mission.Reward >= 3000:
                    # 金バッジ
                    Console.ForegroundColor = ConsoleColor.Yellow
                    Console.WriteLine("\n\n")
                    Console.WriteLine("  ╔════════════════════════════════════════╗")
                    Console.WriteLine("  ║  🏆  MISSION COMPLETE  🏆             ║")
                    Console.WriteLine(f"  ║  ★ {(mission.Name).ljust(int(24))} ★   ║")
                    Console.WriteLine(f"  ║    {(mission.Description).ljust(int(28))}   ║")
                    if mission.Reward > 0:
                        Console.WriteLine(f"  ║    報酬: +{mission.Reward:>6}G                    ║")
                    Console.WriteLine("  ╚════════════════════════════════════════╝")
                    Console.ResetColor()
                else:
                    # 通常バッジ
                    Console.ForegroundColor = ConsoleColor.Cyan
                    Console.WriteLine("\n\n")
                    Console.WriteLine("  ┌──────────────────────────────────────┐")
                    Console.WriteLine("  │  ✓ ミッション達成                    │")
                    Console.WriteLine(f"  │  「{(mission.Name).ljust(int(22))}」  │")
                    if mission.Reward > 0:
                        Console.WriteLine(f"  │   報酬: +{mission.Reward:>5}G                      │")
                    Console.WriteLine("  └──────────────────────────────────────┘")
                    Console.ResetColor()
                Thread.Sleep((500 if isLegend else 1800))
                # 伝説のギャンブラー追加演出
                if isLegend:
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.DarkGray
                    ui_mod.TypewriterEffect("    ベル「...全部、達成したの？」", 50)
                    Thread.Sleep(2000)
                    ui_mod.TypewriterEffect("\n\n    ...沈黙...", 50)
                    Thread.Sleep(2000)
                    Console.ForegroundColor = ConsoleColor.Cyan
                    ui_mod.TypewriterEffect("\n\n    ベル「...すごいわね」", 50)
                    Thread.Sleep(2000)
                    ui_mod.TypewriterEffect("\n\n    ベル「...本当に」", 50)
                    Thread.Sleep(3000)
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.Yellow
                    Console.WriteLine("\n\n\n")
                    Console.WriteLine("    ★ 称号解放 ★")
                    Console.WriteLine("    「伝説のギャンブラー」")
                    Console.ResetColor()
                    Thread.Sleep(3000)
                    if not ("伝説のギャンブラー" in st.unlockedEvents):
                        st.unlockedEvents.append("伝説のギャンブラー")
                Thread.Sleep((2500 if isLegend else 0))
