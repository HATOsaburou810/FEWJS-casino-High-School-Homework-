# シナリオキー列の生成器: ReadKey/ReadLine を乗っ取り、呼び出し元の
# (関数名, 行番号) に応じた応答を返しつつ消費キーを記録する。
# 記録列は driver.py の stdin リプレイと消費順が一致する。
# usage: python3 tests/gen_keys.py <s1|s2|...|s15>
import sys, os, time, types, inspect
import datetime as rdt

_FREEZE_ISO_ENV = os.environ.get("FREEZE_ISO", "2026-01-01T12:00:00")
FROZEN = rdt.datetime.fromisoformat(_FREEZE_ISO_ENV)
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo)
wd = os.path.join(repo, "tests/_scratch_gen")
os.makedirs(wd, exist_ok=True)
os.chdir(wd)
for f in ("saves/save_0.json", "saves/save_1.json", "rankings.txt"):
    p = os.path.join(wd, f)
    if os.path.exists(p):
        os.remove(p)
time.sleep = lambda *a, **k: None

import cs_runtime
class FD(rdt.datetime):
    @classmethod
    def now(cls, tz=None):
        return FROZEN
sh = types.ModuleType("datetime")
for a in ("timedelta", "date", "time", "tzinfo", "timezone", "MINYEAR", "MAXYEAR"):
    setattr(sh, a, getattr(rdt, a))
sh.datetime = FD
cs_runtime._dt = sh

scenario = sys.argv[1]
rec = []
trace = []
st = {}
MAX_KEYS = 800

# GameLoop 内の ReadKey 呼び出し位置 (メニュー選択 / スピン後の続行待ち) を
# ソースのマーカー文字列から動的に特定する (分割後のレイアウト対応)
_app_path = os.path.join(repo, "casino", "app.py")
if not os.path.exists(_app_path):
    _app_path = os.path.join(repo, "casino_slot.py")
_app_lines = open(_app_path, encoding="utf-8").read().splitlines()
MENU_LINE = DISMISS_LINE = -1
_in_gameloop = False
for _i, _l in enumerate(_app_lines, 1):
    if _l.startswith("def GameLoop"):
        _in_gameloop = True
    elif _l.startswith("def ") and _in_gameloop:
        break
    elif _in_gameloop:
        if MENU_LINE < 0 and "key = Console.ReadKey(True)" in _l:
            MENU_LINE = _i
        if "何かキーを押して続ける" in _l:
            DISMISS_LINE = _i + 1  # 直後の ReadKey
assert MENU_LINE > 0 and DISMISS_LINE > 0, "GameLoop の ReadKey 位置を特定できない"

# VIPRoomLoop の ReadKey 位置を特定
_vip_path = os.path.join(repo, "casino", "vip.py")
_vip_lines = open(_vip_path, encoding="utf-8").read().splitlines()
VIP_MENU_LINE = VIP_DISMISS_LINE = -1
_in_viploop = False
for _i, _l in enumerate(_vip_lines, 1):
    if _l.startswith("def VIPRoomLoop"):
        _in_viploop = True
    elif _l.startswith("def ") and _in_viploop:
        break
    elif _in_viploop:
        if VIP_MENU_LINE < 0 and "key = Console.ReadKey(True)" in _l:
            VIP_MENU_LINE = _i
        if "何かキーを押して続ける" in _l:
            VIP_DISMISS_LINE = _i + 1
assert VIP_MENU_LINE > 0, "VIPRoomLoop の ReadKey 位置を特定できない"

# UndergroundLoop の ReadKey 位置を特定
_ug_path = os.path.join(repo, "casino", "underground.py")
_ug_lines = open(_ug_path, encoding="utf-8").read().splitlines()
UG_MENU_LINE = UG_DISMISS_LINE = UG_CONFIRM_X_LINE = UG_CONFIRM_ALLIN_LINE = -1
_in_ugloop = False
for _i, _l in enumerate(_ug_lines, 1):
    if _l.startswith("def UndergroundLoop"):
        _in_ugloop = True
    elif _l.startswith("def ") and _in_ugloop:
        break
    elif _in_ugloop:
        if UG_MENU_LINE < 0 and "key = Console.ReadKey(True)" in _l:
            UG_MENU_LINE = _i
        if "何かキーを押して続ける" in _l:
            UG_DISMISS_LINE = _i + 1
        if "本当に地上へ戻りますか" in _l:
            UG_CONFIRM_X_LINE = _i + 1
        if "全財産を賭けますか" in _l:
            UG_CONFIRM_ALLIN_LINE = _i + 3  # 数行後のReadKey
assert UG_MENU_LINE > 0, "UndergroundLoop の ReadKey 位置を特定できない"


_PKG_DIR = os.path.join(repo, "casino") + os.sep  # casino/ パッケージ
def caller():
    for fr in inspect.stack():
        if (os.path.basename(fr.filename) == "casino_slot.py"
                or fr.filename.startswith(_PKG_DIR)):
            return fr.function, fr.lineno
    return "?", 0


class Overflow(Exception):
    pass


def emit(ch, who):
    if len(rec) > MAX_KEYS:
        raise Overflow()
    rec.append(ch)
    trace.append((who, repr(ch)))
    return ch


def menu_choice(cs):
    """GameLoop メインメニュー (line 1573) での選択。"""
    if scenario == "s1":
        if cs.totalSpins >= 6:
            return "0"
        return "1" if cs.totalSpins % 2 == 0 else "2"
    if scenario == "s2":
        if cs.totalSpins >= 22:
            if not st.get("shopped"):
                st["shopped"] = True
                return "s"
            return "0"
        return "2"
    if scenario == "s3":
        for k in ("m", "c", "r", "e"):
            if not st.get(k):
                st[k] = True
                return k
        if cs.totalSpins >= 2:
            return "0"
        return "2"
    if scenario == "s4":
        # vipRoomUnlocked を DevMode で設定済み → V でVIPへ
        if not st.get("vip_visited"):
            st["vip_visited"] = True
            return "v"
        return "0"
    if scenario == "s5":
        # undergroundUnlocked を DevMode で設定済み → U で地下へ
        if not st.get("ug_visited"):
            st["ug_visited"] = True
            return "u"
        return "0"
    # s6/s7: DevMode のみで完結 (GameLoop は最短終了)
    if scenario in ("s6", "s7"):
        return "0"
    # s8: dream casino - shop 1回訪問 (Layer1 + DreamWakeUp1)
    if scenario == "s8":
        if not st.get("shop1_done"):
            st["shop1_done"] = True
            return "s"
        return "0"
    # s9: abandoned casino
    if scenario == "s9":
        if not st.get("abnd_done"):
            st["abnd_done"] = True
            return "a"
        return "0"
    # s10: devil contract + equipment menu
    if scenario == "s10":
        if not st.get("contract_done"):
            st["contract_done"] = True
            return "d"
        if not st.get("equip_done"):
            st["equip_done"] = True
            return "e"
        return "0"
    # s11: persistence - save/load/delete
    if scenario == "s11":
        phase = st.get("s11_phase", 0)
        if phase == 0:
            # 2 spins, then F5=SaveMenu, then quit
            spins = st.get("s11_spins", 0)
            if spins < 2:
                st["s11_spins"] = spins + 1
                return "2"
            if not st.get("s11_saved"):
                st["s11_saved"] = True
                return _SENTINEL_F5  # F5 → SaveMenu
            return "0"
        if phase == 1:
            # loaded game: 1 spin then quit
            if not st.get("s11_spin2"):
                st["s11_spin2"] = True
                return "2"
            return "0"
        if phase == 2:
            # after delete: quit title with q
            return "0"
        return "0"
    # s12: dream Layer2~Final + MushroomManWaiting
    if scenario == "s12":
        # DevMode already set dreamLayerCleared=1, addiction=50, money=50000
        # Need totalLoses >= 3 first (CanEnterDream for layer2 needs consecutiveWins==0 and totalLoses>=3)
        if cs.totalLoses < 3:
            return "2"  # 100G bet → lose to accumulate totalLoses
        if not st.get("dream_visited"):
            st["dream_visited"] = True
            return "s"  # shop → MushroomManWaiting path OR direct dream
        # After dream layer2: need more losses for layer3 (debt>0) → set via dev
        # But we already set dreamLayerCleared via DevTimeMenu progression
        # For layers 3,4,final: handled via separate game loops with DevTimeMenu
        return "0"
    # s13: abandoned 3F + endings via DevEventGallery
    if scenario == "s13":
        return "0"
    # s14: addiction + items
    if scenario == "s14":
        # addiction=90 set by dev; spins trigger hallucination (addictionLevel>=61, rand<20)
        # spin a few times then go to equipment
        spins = st.get("s14_spins", 0)
        if spins < 8:
            st["s14_spins"] = spins + 1
            return "2"
        if not st.get("s14_equip"):
            st["s14_equip"] = True
            return "e"
        return "0"
    # s15: devmode menus + gallery floor3 + misc endings
    if scenario == "s15":
        return "0"
    return "0"


def vip_menu_choice(cs):
    """VIPRoomLoop でのメニュー選択。"""
    if scenario == "s4":
        spins = st.get("vip_spins", 0)
        if spins >= 4:
            return "x"  # 退室
        st["vip_spins"] = spins + 1
        # 1000G ベット
        return "2"
    return "x"


def ug_menu_choice(cs):
    """UndergroundLoop でのメニュー選択。"""
    if scenario == "s5":
        spins = st.get("ug_spins", 0)
        if spins == 0:
            st["ug_spins"] = 1
            return "1"  # 500G
        if spins == 1:
            st["ug_spins"] = 2
            return "2"  # 1000G
        if spins == 2:
            st["ug_spins"] = 3
            return "4"  # all-in
        return "x"  # 退出
    return "x"


def policy():
    try:
        import casino.state as cs  # 分割後レイアウト
    except ImportError:
        import casino_slot as cs
    fn, ln = caller()
    who = "%s:%d" % (fn, ln)

    # ===== 既存シナリオ =====
    if fn == "ShowTitleScreen":
        if st.get("ended"):
            return emit("q", who)
        # DevMode 入口: s4/s5/s6/s7/s8/s9/s10/s11/s12/s13/s14/s15 の初回 ShowTitleScreen でバッキック
        if scenario in ("s4", "s5", "s6", "s7", "s8", "s9", "s10",
                        "s11", "s12", "s13", "s14", "s15") and not st.get("dev_entered"):
            st["dev_entered"] = True
            return emit("`", who)
        # s11 phase1: title shows with save data → L to load
        if scenario == "s11" and st.get("s11_phase") == 1 and not st.get("s11_load_done"):
            st["s11_load_done"] = True
            return emit("l", who)  # L key → LoadMenu
        # s11 phase2: title after load-game-done → D to delete
        if scenario == "s11" and st.get("s11_phase") == 2 and not st.get("s11_del_done"):
            st["s11_del_done"] = True
            return emit("d", who)  # D key → DeleteSaveMenu → then ShowTitleScreen called again
        return emit("\n", who)
    if fn == "GameLoop":
        if ln == MENU_LINE:
            return emit(menu_choice(cs), who)
        if ln == DISMISS_LINE:  # 何かキーを押して続ける
            return emit(".", who)
        return emit(".", who)  # 終了確認・メタ演出など
    if fn == "ShowEnding":
        if scenario == "s11":
            phase = st.get("s11_phase", 0)
            if phase == 0:
                # After first game (saved), advance to phase1 (load)
                st["s11_phase"] = 1
                st["ended"] = False  # don't quit yet
            elif phase == 1:
                # After loaded game, advance to phase2 (delete)
                st["s11_phase"] = 2
                st["ended"] = False
            else:
                st["ended"] = True
        else:
            st["ended"] = True
        return emit(".", who)
    if fn == "DoubleUpChallenge":
        return emit("n", who)
    if fn == "ShopMenu":
        return emit("0", who)  # 即退店 (冷やかしカウント)
    if fn == "ShowAllMissions":
        return emit("0", who)
    if fn in ("ShowRankings", "ShowCollection"):
        return emit(".", who)
    # ===== DevMode ルーティング (s4/s5/s6/s7/s8/s9/s10) =====
    if fn == "DevModeEntry":
        # パスワード入力は fake_readline が処理する (youmukawaii を返す)
        return emit(".", who)  # フォールスルー防止 (ReadLine 呼び出しなし)

    if fn == "DevModeMenu":
        seq = st.get("dev_seq", None)
        if seq is None:
            if scenario == "s4":
                # [1]ステータス(money設定) → [2]フラグ(vipRoomUnlocked ON) → [0]終了
                st["dev_seq"] = ["1", "2", "0"]
            elif scenario == "s5":
                # [1]ステータス(money設定) → [2]フラグ(undergroundUnlocked ON) → [0]終了
                st["dev_seq"] = ["1", "2", "0"]
            elif scenario == "s6":
                # [7]全解放 → [6]デバッグ情報 → [G]ギャラリー → [0]終了
                st["dev_seq"] = ["7", "6", "G", "0"]
            elif scenario == "s7":
                # [G]ギャラリー → [0]終了
                st["dev_seq"] = ["G", "0"]
            elif scenario == "s8":
                # [1]ステータス(money=50000,addiction=50) → [2]フラグ(dreamCasinoUnlocked) → [0]終了
                st["dev_seq"] = ["1", "2", "0"]
            elif scenario == "s9":
                # [1]ステータス(money=50000) → [G]ギャラリー(Floor1フラグ設定) → [0]終了
                st["dev_seq"] = ["1", "G", "0"]
            elif scenario == "s10":
                # [1]ステータス(money=50000) → [2]フラグ(devilContractOffered) → [3]アイテム(cursed) → [0]終了
                st["dev_seq"] = ["1", "2", "3", "0"]
            elif scenario == "s11":
                # [1]ステータス(money=50000) → [0]終了
                st["dev_seq"] = ["1", "0"]
            elif scenario == "s12":
                # [1]ステータス(money=50000,addiction=50) → [2]フラグ(dreamCasinoUnlocked) → [5]時間(dreamLayerCleared=1) → [0]終了
                st["dev_seq"] = ["1", "2", "5", "0"]
            elif scenario == "s13":
                # [1]ステータス(money=100000) → [G]ギャラリー → [0]終了
                st["dev_seq"] = ["1", "G", "0"]
            elif scenario == "s14":
                # [1]ステータス(money=50000,addiction=90) → [3]アイテム(cursed) → [0]終了
                st["dev_seq"] = ["1", "3", "0"]
            elif scenario == "s15":
                # [4]スロット設定 → [5]時間設定 → [8]全リセット → [G]ギャラリー → [0]終了
                st["dev_seq"] = ["4", "5", "8", "G", "0"]
            else:
                st["dev_seq"] = ["0"]
        action = st["dev_seq"].pop(0) if st["dev_seq"] else "0"
        return emit(action, who)

    if fn == "DevUnlockAll":
        # 全解放確認 [Y/N]
        return emit("y", who)

    if fn == "DevStatusMenu":
        # s4: money=50000 を設定して戻る ([1]所持金 → [0]戻る)
        # s5: money=10000 を設定して戻る ([1]所持金 → [0]戻る)
        # s8: money=50000, addiction=50 ([1]所持金 → [3]中毒度 → [0]戻る)
        # s9: money=50000 ([1]所持金 → [0]戻る)
        # s10: money=50000 ([1]所持金 → [0]戻る)
        # s11: money=50000 ([1]所持金 → [0]戻る)
        # s12: money=50000, addiction=50 ([1]所持金 → [3]中毒度 → [0]戻る)
        # s13: money=100000 ([1]所持金 → [0]戻る)
        # s14: money=50000, addiction=90 ([1]所持金 → [3]中毒度 → [0]戻る)
        # s15: [0]戻る (全リセット後なのでステータス不要)
        seq = st.get("status_seq", None)
        if seq is None:
            if scenario in ("s8", "s12"):
                st["status_seq"] = ["1", "3", "0"]  # 1=所持金, 3=中毒度, 0=戻る
            elif scenario == "s14":
                st["status_seq"] = ["1", "3", "0"]  # 1=所持金50000, 3=中毒度90, 0=戻る
            elif scenario == "s15":
                st["status_seq"] = ["0"]
            else:
                st["status_seq"] = ["1", "0"]  # 1=所持金設定, 0=戻る
        action = st["status_seq"].pop(0) if st["status_seq"] else "0"
        return emit(action, who)

    if fn == "DevFlagMenu":
        # flags リスト: index 0=godMode, 1=godModePermanent, 2=luckyTimeActive,
        #               3=vipRoomUnlocked, 4=isInVIPRoom, 5=undergroundUnlocked, ...
        # page 0 (index 0-11): key=index%12+1
        #   key "4" = index 3 (vipRoomUnlocked)
        #   key "6" = index 5 (undergroundUnlocked)
        #   key "8" = index 7 (dreamCasinoUnlocked)
        # page 1 (index 12-23): key=index%12+1
        #   key "3" = index 14 (devilContractOffered)
        # N = 次ページ
        seq = st.get("flag_seq", None)
        if seq is None:
            if scenario == "s4":
                st["flag_seq"] = ["4", "0"]  # toggle vipRoomUnlocked, 戻る
            elif scenario == "s5":
                st["flag_seq"] = ["6", "0"]  # toggle undergroundUnlocked, 戻る
            elif scenario in ("s8", "s12"):
                # dreamCasinoUnlocked (page 0, key "8")
                st["flag_seq"] = ["8", "0"]
            elif scenario == "s10":
                # devilContractOffered (page 1, key "3"): N=次ページ, then "3"
                st["flag_seq"] = ["N", "3", "0"]
            else:
                st["flag_seq"] = ["0"]
        action = st["flag_seq"].pop(0) if st["flag_seq"] else "0"
        return emit(action, who)

    if fn == "DevItemMenu":
        # s10/s14: [5]呪いアイテム全入手 → [0]戻る
        seq = st.get("item_seq", None)
        if seq is None:
            if scenario in ("s10", "s14"):
                st["item_seq"] = ["5", "0"]
            else:
                st["item_seq"] = ["0"]
        action = st["item_seq"].pop(0) if st["item_seq"] else "0"
        return emit(action, who)

    if fn == "DevDebugInfo":
        # 何かキーで戻る
        return emit(".", who)

    if fn == "DevSlotMenu":
        # s15: [1]totalSpins設定 → [0]戻る
        seq = st.get("slotmenu_seq", None)
        if seq is None:
            if scenario == "s15":
                st["slotmenu_seq"] = ["1", "0"]
            else:
                st["slotmenu_seq"] = ["0"]
        action = st["slotmenu_seq"].pop(0) if st["slotmenu_seq"] else "0"
        return emit(action, who)

    if fn == "DevTimeMenu":
        # s12: [3]夢カジノクリア層=1 → [0]戻る
        # s15: [1]借金ターン設定 → [0]戻る
        seq = st.get("timemenu_seq", None)
        if seq is None:
            if scenario == "s12":
                st["timemenu_seq"] = ["3", "0"]
            elif scenario == "s15":
                st["timemenu_seq"] = ["1", "0"]
            else:
                st["timemenu_seq"] = ["0"]
        action = st["timemenu_seq"].pop(0) if st["timemenu_seq"] else "0"
        return emit(action, who)

    if fn == "DevResetAll":
        # 全リセット確認 [Y/N]
        return emit("y", who)

    if fn == "DevEventGallery":
        # Line 634: イベント終了後の「何かキー」 → "." で戻る
        if ln == 634:
            return emit(".", who)
        # main menu
        seq = st.get("gallery_seq", None)
        if seq is None:
            if scenario == "s6":
                # 1=Chapter1(ReadKey後あり), 2=Floor1(continueで戻る), 3=Floor2(continueで戻る), 0=終了
                st["gallery_seq"] = ["1", "2", "3", "0"]
            elif scenario == "s7":
                # 1=Chapter1, 2=Floor1, 0=終了
                st["gallery_seq"] = ["1", "2", "0"]
            elif scenario == "s9":
                # "2"=Floor1フラグ設定(continue後DevGalleryFloor1で"0"exit), "0"=終了
                st["gallery_seq"] = ["2", "0"]
            elif scenario == "s13":
                # 4=3階, 5=地下室(時計必要), 6=exitEvent, 7=endingA, 8=endingB, 0=終了
                st["gallery_seq"] = ["4", "5", "6", "7", "8", "0"]
            elif scenario == "s15":
                # 9=BuyExchangedMoney, A=InnocentGemFound, B=ShopHiddenPage, 0=終了
                st["gallery_seq"] = ["9", "A", "B", "0"]
            else:
                st["gallery_seq"] = ["0"]
        action = st["gallery_seq"].pop(0) if st["gallery_seq"] else "0"
        return emit(action, who)

    if fn == "DevGalleryFloor1":
        # s6/s7: [1]部屋A(menu) → Room1F_A が ReadKey("1") → DevGalleryFloor1がReadKey("."): イベント終了 → [0]戻る
        # s9: [0]すぐ戻る (フラグだけ設定してgallery exitへ)
        seq = st.get("gf1_seq", None)
        if seq is None:
            if scenario == "s9":
                st["gf1_seq"] = ["0"]  # すぐ exit, flags already set by DevEventGallery
            else:
                st["gf1_seq"] = ["1", ".", "0"]
        action = st["gf1_seq"].pop(0) if st["gf1_seq"] else "0"
        return emit(action, who)

    if fn == "DevGalleryFloor2":
        # [1]部屋A(menu) → Room2F_A が ReadKey("1") → DevGalleryFloor2がReadKey("."): イベント終了 → [0]戻る
        seq = st.get("gf2_seq", None)
        if seq is None:
            st["gf2_seq"] = ["1", ".", "0"]
        action = st["gf2_seq"].pop(0) if st["gf2_seq"] else "0"
        return emit(action, who)

    if fn == "DevGalleryFloor3":
        # s13: 全部屋 + 最終部屋 を順番に巡る
        # [1]=Room3F_A, [2]=Room3F_B, [3]=Room3F_C, [4]=Room3F_D, [5]=Room3F_Final, [0]=戻る
        seq = st.get("gf3_seq", None)
        if seq is None:
            if scenario == "s13":
                st["gf3_seq"] = ["1", ".", "2", ".", "3", ".", "4", ".", "5", ".", "0"]
            else:
                st["gf3_seq"] = ["1", ".", "0"]
        action = st["gf3_seq"].pop(0) if st["gf3_seq"] else "0"
        return emit(action, who)

    # ギャラリーイベント後の「何かキー → ギャラリーに戻る」
    # DevEventGallery 内の ReadKey (ln=634)
    if fn == "DevMsg":
        return emit(".", who)  # DevMsg 自体は ReadKey しないが念のため

    # ===== VIPRoomLoop (s4) =====
    if fn == "VIPRoomLoop":
        if ln == VIP_MENU_LINE:
            return emit(vip_menu_choice(cs), who)
        if VIP_DISMISS_LINE > 0 and ln == VIP_DISMISS_LINE:
            return emit(".", who)
        return emit(".", who)

    if fn == "VIPDoubleUpChallenge":
        return emit("n", who)

    if fn == "VIPSpin":
        # 借金を返済しますか？[Y/N]  (winAmount>0 かつ debt>0 のとき)
        return emit("n", who)

    # ===== UndergroundLoop (s5) =====
    if fn == "UndergroundLoop":
        if ln == UG_MENU_LINE:
            return emit(ug_menu_choice(cs), who)
        if UG_DISMISS_LINE > 0 and ln == UG_DISMISS_LINE:
            return emit(".", who)
        # x の確認 [Y/N]
        if UG_CONFIRM_X_LINE > 0 and ln == UG_CONFIRM_X_LINE:
            return emit("y", who)
        # 全財産確認 [Y/N]
        return emit("y", who)

    if fn == "UndergroundSpin":
        # 借金を返済しますか？[Y/N]
        return emit("n", who)

    # ===== Abandoned Casino rooms (s6/s7 via DevEventGallery) =====
    if fn == "Room1F_A":
        # [1] 絵をよく見る / [0] 戻る
        return emit("1", who)

    if fn == "Room2F_A":
        # [1] コートをよく見る / [0] 戻る
        return emit("1", who)

    # Chapter1 / InnocentGemFound / AbandonedCasinoExitEvent 等
    # (BasementDoorFound は [1]降りる の選択があるため下の専用ハンドラで処理)
    if fn in ("Chapter1_FirstConversation", "InnocentGemFound", "AbandonedCasinoExitEvent",
              "EndingRouteA_Owner", "EndingRouteB_Bell",
              "BuyExchangedMoney", "ShopHiddenPage"):
        return emit(".", who)

    # DevEventGallery の「イベント終了 → 何かキー」の ReadKey (ln=634)
    # これは DevEventGallery 内の Console.ReadKey 呼び出し
    # MushroomManFirstMeet の ReadLine (dream)
    if fn == "MushroomManFirstMeet":
        return emit(".", who)

    # OverflowHiddenEnding の ReadKey (ln=140)
    if fn == "OverflowHiddenEnding":
        return emit(".", who)

    # TrueEnding の ReadKey (fn=TrueEnding, ln=933)
    if fn == "TrueEnding":
        return emit(".", who)

    # ===== s8: Dream Casino =====
    # MushroomManFirstMeet の ReadKey (2回のReadLine + 最後の演出)
    # → fake_readline が処理するため、ここではフォールスルー

    # ===== s9: Abandoned Casino =====
    if fn == "AbandonedCasinoFloor1":
        seq = st.get("floor1_seq", None)
        if seq is None:
            # 1=Room A, 2=Room B, 3=Room C, 4=Room D, 5=Final, 6=GoToFloor2, 0=exit
            st["floor1_seq"] = ["1", "2", "3", "4", "5", "6", "0"]
        action = st["floor1_seq"].pop(0) if st["floor1_seq"] else "0"
        return emit(action, who)

    if fn == "AbandonedCasinoFloor2":
        seq = st.get("floor2_seq", None)
        if seq is None:
            # 1〜4=各部屋, 5=最奥(Room2F_Final), 7=階段(GoToFloor3), 以降は "0"=exit
            st["floor2_seq"] = ["1", "2", "3", "4", "5", "7"]
        action = st["floor2_seq"].pop(0) if st["floor2_seq"] else "0"
        return emit(action, who)

    if fn == "AbandonedCasinoFloor3":
        seq = st.get("floor3_seq", None)
        if seq is None:
            # 1〜4=各部屋, 5=最奥(Room3F_Final), 7=出口(AbandonedCasinoExit), 以降は "0"=exit
            st["floor3_seq"] = ["1", "2", "3", "4", "5", "7"]
        action = st["floor3_seq"].pop(0) if st["floor3_seq"] else "0"
        return emit(action, who)

    if fn in ("Room1F_B", "Room1F_C", "Room1F_D"):
        # [1] 詳しく見る
        return emit("1", who)

    if fn in ("Room2F_B", "Room2F_C", "Room2F_D"):
        return emit("1", who)

    if fn in ("Room3F_A", "Room3F_B", "Room3F_C"):
        return emit("1", who)

    if fn == "Room3F_D":
        # [1] 天井を見る (最初の ReadKey は "1", その後の天井ReadKeyもあるかも)
        return emit("1", who)

    if fn == "Room3F_Final":
        # [1] 引き出しを開ける → 手紙読む
        return emit("1", who)

    # s13: BasementDoorFound の [1] 降りる / [0] 戻る
    if fn == "BasementDoorFound":
        return emit("1", who)

    # s13: BasementEvent の [1] 布をめくる / [0] やめる
    if fn == "BasementEvent":
        return emit("1", who)

    # s13: BlackSuitFinalConfrontation → [1] EndingRouteA_Owner
    if fn == "BlackSuitFinalConfrontation":
        return emit("1", who)

    # ===== s10: Devil Contract + Equipment =====
    if fn == "DevilContractMenu":
        seq = st.get("contract_seq", None)
        if seq is None:
            # "1" = 契約1を選ぶ → "y" = 確認
            st["contract_seq"] = ["1", "y"]
        action = st["contract_seq"].pop(0) if st["contract_seq"] else "0"
        return emit(action, who)

    if fn == "EquipmentMenu":
        seq = st.get("equip_seq", None)
        if seq is None:
            if scenario == "s10":
                # [4]血塗られたお守り装備 → [4]血塗られたお守り解除 → [0]戻る
                st["equip_seq"] = ["4", "4", "0"]
            elif scenario == "s14":
                # 全呪いアイテム操作: 悪魔のコイン使用[3,y], 血塗り装備[4,y], 死神装備[5,y],
                # 時計装備[6,y], 水晶玉使用[7,y], 全解除[9], リハビリ券[8,y], 戻る[0]
                st["equip_seq"] = ["3", "4", "5", "6", "7", "9", "8", "0"]
            else:
                st["equip_seq"] = ["0"]
        action = st["equip_seq"].pop(0) if st["equip_seq"] else "0"
        return emit(action, who)

    # s14: 各アイテム使用時の確認 [Y/N]
    if fn in ("UseDevilCoin", "ToggleBloodAmulet", "ToggleDeathRing", "ToggleTimeClock",
              "UseOracleBall", "UseRehabTicket", "UnequipAll"):
        # UseDevilCoin/Toggle*/UseOracleBall の Y/N 確認
        return emit("y", who)

    # s11: SaveMenu → スロット選択 (slot 1 は空なので確認なし → SaveGame → break)
    if fn == "SaveMenu":
        seq = st.get("savemenu_seq", None)
        if seq is None:
            if scenario == "s11":
                # slot "1" → SaveGame (empty slot, no overwrite confirm)
                st["savemenu_seq"] = ["1"]
            else:
                st["savemenu_seq"] = ["0"]
        action = st["savemenu_seq"].pop(0) if st["savemenu_seq"] else "0"
        return emit(action, who)

    # s11: LoadMenu → スロット1ロード
    if fn == "LoadMenu":
        seq = st.get("loadmenu_seq", None)
        if seq is None:
            if scenario == "s11":
                st["loadmenu_seq"] = ["1"]
            else:
                st["loadmenu_seq"] = ["0"]
        action = st["loadmenu_seq"].pop(0) if st["loadmenu_seq"] else "0"
        return emit(action, who)

    # s11: DeleteSaveMenu → スロット1削除 → confirm Y
    if fn == "DeleteSaveMenu":
        seq = st.get("deletemenu_seq", None)
        if seq is None:
            if scenario == "s11":
                # "1"=スロット選択 → (fn called again for confirm) → "0"=戻る
                st["deletemenu_seq"] = ["1", "y", "0"]
            else:
                st["deletemenu_seq"] = ["0"]
        action = st["deletemenu_seq"].pop(0) if st["deletemenu_seq"] else "0"
        # confirm key: "y" maps to ConsoleKey.Y
        if action == "y":
            return emit("y", who)
        return emit(action, who)

    if fn == "ToggleBloodAmulet":
        # 装備確認 [Y/N]: Y で装備/解除
        return emit("y", who)

    return emit("n", who)


_SENTINEL_F5 = "\x0f"   # Ctrl-O → F5 (SaveMenu)
_SENTINEL_F9 = "\x1c"   # FS    → F9 (LoadMenu in GameLoop)

def fake_read_key_raw():
    ch = policy()
    if ch == _SENTINEL_F5:
        return cs_runtime.ConsoleKeyInfo("\x00", cs_runtime.ConsoleKey.F5)
    if ch == _SENTINEL_F9:
        return cs_runtime.ConsoleKeyInfo("\x00", cs_runtime.ConsoleKey.F9)
    return cs_runtime._make_keyinfo(ch)


def fake_readline():
    fn, ln = caller()
    who = "%s:%d" % (fn, ln)

    # DevModeEntry: パスワード入力
    if fn == "DevModeEntry":
        name = "youmukawaii"
        for c in name:
            rec.append(c)
        rec.append("\n")
        trace.append((who, repr(name + "\\n")))
        return name

    # DevStatusMenu: 所持金/中毒度入力
    if fn == "DevStatusMenu":
        seq = st.get("status_input_seq", None)
        if seq is None:
            if scenario == "s4":
                st["status_input_seq"] = ["50000"]
            elif scenario == "s5":
                st["status_input_seq"] = ["10000"]
            elif scenario in ("s8", "s12"):
                # 1=所持金50000, 3=中毒度50 の順で入力
                st["status_input_seq"] = ["50000", "50"]
            elif scenario == "s14":
                # 1=所持金50000, 3=中毒度90
                st["status_input_seq"] = ["50000", "90"]
            elif scenario == "s13":
                st["status_input_seq"] = ["100000"]
            elif scenario in ("s9", "s10", "s11"):
                st["status_input_seq"] = ["50000"]
            elif scenario == "s15":
                # DevSlotMenu: totalSpins入力
                st["status_input_seq"] = ["10"]
            else:
                st["status_input_seq"] = ["10000"]
        val = st["status_input_seq"].pop(0) if st["status_input_seq"] else "0"
        for c in val:
            rec.append(c)
        rec.append("\n")
        trace.append((who, repr(val + "\\n")))
        return val

    # DevSlotMenu/DevTimeMenu の ReadLine 入力
    if fn in ("DevSlotMenu", "DevTimeMenu"):
        seq = st.get("devmenu_input_seq", None)
        if seq is None:
            if scenario == "s12":
                # DevTimeMenu: dreamLayerCleared = 1
                st["devmenu_input_seq"] = ["1"]
            elif scenario == "s15":
                # DevSlotMenu totalSpins=50, DevTimeMenu debtTurns=5
                st["devmenu_input_seq"] = ["50", "5"]
            else:
                st["devmenu_input_seq"] = ["0"]
        val = st["devmenu_input_seq"].pop(0) if st["devmenu_input_seq"] else "0"
        for c in val:
            rec.append(c)
        rec.append("\n")
        trace.append((who, repr(val + "\\n")))
        return val

    # MushroomManFirstMeet: 選択入力 → "1"
    if fn == "MushroomManFirstMeet":
        rec.append("1")
        rec.append("\n")
        trace.append((who, repr("1\\n")))
        return "1"

    # デフォルト: 名前入力
    name = "Tester"
    for c in name:
        rec.append(c)
    rec.append("\n")
    trace.append(("%s:%d" % (fn, ln), repr(name + "\\n")))
    return name


cs_runtime._read_key_raw = fake_read_key_raw

import casino_slot
casino_slot.rand._r.seed(12345)
cs_runtime.Console.ReadLine = fake_readline


class Null:
    def write(self, *a):
        pass
    def flush(self):
        pass


sys.stdout = Null()
status = "clean-exit"
try:
    casino_slot.Main()
except Overflow:
    status = "OVERFLOW (policy loop?)"
except (KeyboardInterrupt, EOFError):
    status = "exit-exc"
except SystemExit:
    status = "clean-exit"
except Exception as e:
    import traceback
    status = "ERROR %s: %s\n%s" % (type(e).__name__, e, traceback.format_exc())
sys.stdout = sys.__stdout__

out = os.path.join(repo, "tests/scenarios/%s.keys" % scenario)
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("".join(rec))
print("STATUS:", status)
print("keys:", len(rec), "->", out)
from collections import Counter
print(Counter(w for w, _ in trace))
try:
    import casino.state as _st
except ImportError:
    _st = casino_slot
print("totalSpins=%s money=%s shopVisits=%s save0=%s" % (
    _st.totalSpins, _st.money, _st.shopVisitCount,
    os.path.exists(os.path.join(wd, "saves/save_0.json"))))
