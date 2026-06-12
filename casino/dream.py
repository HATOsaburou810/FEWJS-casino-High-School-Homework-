# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 夢カジノ (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod
from . import events


def CanEnterDream():
    hour = DateTimeNS.Now.Hour
    isLateNight = hour >= 22 or hour < 5
    _sw4 = st.dreamLayerCleared
    if _sw4 == 0:
        return st.dreamCasinoUnlocked and isLateNight and st.addictionLevel >= 50
    elif _sw4 == 1:
        return isLateNight and st.consecutiveWins == 0 and st.totalLoses >= 3
    elif _sw4 == 2:
        return isLateNight and st.debt > 0
    elif _sw4 == 3:
        return isLateNight and st.money <= 100
    elif _sw4 == 4:
        return isLateNight and st.addictionLevel >= 80
    else:
        return False

def MushroomManFirstMeet():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("    気づくと、見知らぬ男が立っていた")
    Console.WriteLine("    顔が…キノコだった")
    Console.WriteLine("    スーツを着ていた")
    Console.WriteLine("    じっとこちらを見ていた")
    Thread.Sleep(2000)
    Console.WriteLine("\n    男が口を開いた")
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n    「※▲◎♪✦□…」")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("    「…よる…ねむい…▲◎※…」")
    Thread.Sleep(1500)
    Console.WriteLine("\n    意味が分からなかった")
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.Gray
    Console.WriteLine("\n    …これは何かのヒントか？")
    Thread.Sleep(2000)
    Console.WriteLine("\n    [1] 頷く")
    Console.WriteLine("    [2] 首を振る")
    Console.WriteLine("    [3] 無視する")
    Console.WriteLine("    [4] 話しかけてみる")
    Console.ResetColor()
    _choice = coalesce(Console.ReadLine(), "")
    # どれを選んでも同じ
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("    男はゆっくりと頷いた")
    Thread.Sleep(1500)
    Console.WriteLine("    そして振り返り")
    Thread.Sleep(1000)
    Console.WriteLine("    奥の扉の方へ歩き始めた")
    Thread.Sleep(2000)
    Console.WriteLine("\n    [1] ついていく")
    Console.WriteLine("    [2] ついていかない")
    Console.ResetColor()
    _choice = coalesce(Console.ReadLine(), "")
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("    男は扉の前で立ち止まり")
    Thread.Sleep(1000)
    Console.WriteLine("    こちらを見た")
    Thread.Sleep(1000)
    Console.WriteLine("    ただ、待っていた")
    Thread.Sleep(2000)
    Console.ResetColor()
    # 結局入る
    st.mushroomManMet = True
    EnterDreamCasino()

def EnterDreamCasino():
    _sw5 = st.dreamLayerCleared
    if _sw5 == 0:
        DreamLayer1()
    elif _sw5 == 1:
        DreamLayer2()
    elif _sw5 == 2:
        DreamLayer3()
    elif _sw5 == 3:
        DreamLayer4()
    elif _sw5 == 4:
        DreamLayerFinal()

def DreamLayer1():
    Console.clear()
    Thread.Sleep(1000)
    ui_mod.TypeText("    気づいたら、カジノにいた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n    …でも")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    気のせいか")
    ui_mod.TypeText("\n    なんだかここはさっきまでいたカジノではない気がする")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    誰もいない")
    Thread.Sleep(800)
    ui_mod.TypeText("\n    音もない")
    Thread.Sleep(800)
    ui_mod.TypeText("\n    スロットだけが")
    ui_mod.TypeText("\n    ただそこにある")
    Thread.Sleep(2000)
    ui_mod.TypeText("\n\n    …どこからか声が聞こえた")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    BellDreamLine("あら、いらっしゃい♪ 待ってたわよ？")
    BellDreamLine("また来たのね♪ やっぱり来ると思ってた")
    BellDreamLine("さすが、目の付け所がいいわね♪")
    BellDreamLine("またいつでも来てね♪ 待ってるから")
    Thread.Sleep(1500)
    Console.ResetColor()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「ねえ」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…あなたは、どうして来たの？」")
    Thread.Sleep(3000)
    # 暗転
    Console.clear()
    Console.ResetColor()
    Thread.Sleep(1000)
    # 目覚め
    DreamWakeUp(1)

def DreamLayer2():
    Console.clear()
    Thread.Sleep(1000)
    ui_mod.TypeText("    また、カジノにいた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    前より")
    ui_mod.TypeText("\n    少し暗い気がした")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n\n    気のせいかもしれない")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    …でも")
    ui_mod.TypeText("\n    なんとなく")
    ui_mod.TypeText("\n    そう感じた")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    BellDreamLine("…顔色悪いわよ？")
    BellDreamLine("まあ、私には関係ないけど♪")
    BellDreamLine("借金があっても来てくれるのね。…うれしい♪")
    BellDreamLine("無理しなくていいわよ")
    BellDreamLine("…大丈夫？ まあ、大丈夫じゃないわよね♪")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「ねえ」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…大丈夫って」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…誰かに言われたこと、あった？」")
    Thread.Sleep(3000)
    Console.clear()
    Console.ResetColor()
    Thread.Sleep(1000)
    DreamWakeUp(2)

def DreamLayer3():
    Console.clear()
    Thread.Sleep(1000)
    ui_mod.TypeText("    また、カジノにいた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    もっと暗くなっていた")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n\n    スロットの光だけが")
    ui_mod.TypeText("\n    ぼんやりと灯っていた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    …誰かが泣いている気がした")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    気のせいかもしれない")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    BellDreamLine("こんな時間に来るなんて…")
    BellDreamLine("…帰ってきたのね♪")
    BellDreamLine("…無事でよかった。本当に")
    BellDreamLine("また来てね♪ 待ってるから")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「ねえ」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…待ってたら」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…来てくれると思ってた？」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypeText("\n\n    ベル「…私は」")
    Thread.Sleep(3000)
    Console.clear()
    Console.ResetColor()
    Thread.Sleep(1000)
    DreamWakeUp(3)

def DreamLayer4():
    Console.clear()
    Thread.Sleep(1000)
    ui_mod.TypeText("    また、カジノにいた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    光がほとんどなかった")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n\n    遠くに")
    ui_mod.TypeText("\n    ぼんやりとした明かりだけが見えた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    …さっきの声が")
    ui_mod.TypeText("\n    まだ耳に残っていた")
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkCyan
    BellDreamLine("…ねえ、覚えてる？")
    BellDreamLine("…あなたは、どうして来たの？")
    BellDreamLine("…大丈夫って、誰かに言われたこと、あった？")
    BellDreamLine("…待ってたら、来てくれると思ってた？")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n    …長い沈黙…")
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkCyan
    ui_mod.TypeText("\n\n    ベル「…私は」")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n    ベル「…ずっと待ってたのよ」")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n    ベル「…誰かが来てくれると思って」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkCyan
    ui_mod.TypeText("\n\n    ベル「でも」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkCyan
    ui_mod.TypeText("\n\n    ベル「…誰も」")
    Thread.Sleep(3000)
    Console.clear()
    Console.ResetColor()
    Thread.Sleep(1000)
    DreamWakeUp(4)

def DreamLayerFinal():
    Console.clear()
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("    真っ暗だった")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    光が")
    ui_mod.TypeText("\n    一切なかった")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    声だけが聞こえた")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    あの声だった")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    でも")
    ui_mod.TypeText("\n    笑っていなかった")
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(1000)
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「…ずっと、ひとりだった」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「生まれた時から」")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    「たぶん、ずっと」")
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「泣いたこともあった」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「でも誰も来なかった」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「だから泣くのをやめた」")
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …長い沈黙…")
    Thread.Sleep(3000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「居場所ができたと思った」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「それだけでよかった」")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    「それだけで」")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    「十分だったのに」")
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …長い沈黙…")
    Thread.Sleep(3000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「…なんで」")
    Thread.Sleep(4000)
    Console.clear()
    Thread.Sleep(1000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    ui_mod.TypeText("\n\n    暗闇の中に")
    ui_mod.TypeText("\n    指輪だけが光っていた")
    Thread.Sleep(3000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「持っていって」")
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("\n\n    …沈黙…")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypeText("\n\n    「お願い」")
    Thread.Sleep(4000)
    # 暗転
    Console.clear()
    Console.ResetColor()
    Thread.Sleep(2000)
    # 強欲の指輪入手
    st.hasGreedRing = True
    st.dreamLayerCleared = 5
    DreamWakeUpFinal()

def DreamWakeUp(layer):
    st.dreamLayerCleared = layer
    Console.ForegroundColor = ConsoleColor.DarkGray
    hint = ""
    if layer == 1:
        hint = "…まけ…つづける…"
    elif layer == 2:
        hint = "…かりた…かえせない…"
    elif layer == 3:
        hint = "…なにも…ない…"
    elif layer == 4:
        hint = "…もどれない…"
    ui_mod.TypeText("    目が覚めた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    耳の奥に声が残っていた")
    Thread.Sleep(1000)
    ui_mod.TypeText(f"\n\n    「{hint}」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Gray
    ui_mod.TypeText("\n\n    …これは何かのヒントか？")
    Thread.Sleep(3000)
    Console.ResetColor()
    # 3層クリア後：無垢な宝石が出現
    if layer == 3 and not st.hasInnocentGem:
        events.InnocentGemFound()

def DreamWakeUpFinal():
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypeText("    目が覚めた")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n    手の中に…指輪がある")
    Thread.Sleep(2000)
    ui_mod.TypeText("\n\n    夢だったのか")
    Thread.Sleep(1000)
    ui_mod.TypeText("\n    それとも")
    Thread.Sleep(3000)
    Console.clear()
    Thread.Sleep(500)
    ui_mod.TypeText("\n\n    その時")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    一瞬だけ")
    ui_mod.TypeText("\n    見えた気がした")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    顔がキノコの")
    ui_mod.TypeText("\n    スーツ姿の男")
    Thread.Sleep(1500)
    ui_mod.TypeText("\n\n    ショップの方を")
    ui_mod.TypeText("\n    ただ、見ていた")
    Thread.Sleep(2000)
    ui_mod.TypeText("\n\n    瞬きをしたら")
    ui_mod.TypeText("\n    もういなかった")
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Gray
    ui_mod.TypeText("\n\n    足が自然と")
    ui_mod.TypeText("\n    ショップに向いていた")
    Thread.Sleep(3000)
    Console.ResetColor()

def MushroomManWaiting():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("    キノコの男が立っていた")
    Thread.Sleep(1500)
    Console.WriteLine("    何も言わなかった")
    Thread.Sleep(1000)
    Console.WriteLine("    ただ、こちらを見ていた")
    Thread.Sleep(2000)
    Console.ResetColor()
    EnterDreamCasino()

def BellDreamLine(line):
    Thread.Sleep(800)
    Console.WriteLine(f"\n    ベル「{line}」")
    Thread.Sleep(1200)
