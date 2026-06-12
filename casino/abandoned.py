# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 廃娯楽施設 (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod


def EnterAbandonedCasino():
    if not st.hasInnocentGem:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    カギを差し込んだが", 42)
        Thread.Sleep(1800)
        ui_mod.TypewriterEffect("\n\n    扉は　開かなかった", 42)
        Thread.Sleep(2000)
        Console.clear()
        Console.ResetColor()
        return
    Console.clear()
    Thread.Sleep(500)
    if not st.abandonedCasinoEntered:
        st.abandonedCasinoEntered = True
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n\n    カギを使うと", 45)
        Thread.Sleep(1500)
        ui_mod.TypewriterEffect("\n    重い扉が　ゆっくりと開いた", 45)
        Thread.Sleep(2000)
        Console.clear()
        ui_mod.TypewriterEffect("\n\n    埃っぽい空気が　流れてきた", 45)
        Thread.Sleep(2000)
        ui_mod.TypewriterEffect("\n\n    古い照明が　かろうじて灯っている", 45)
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("\n\n    ベル「...わあ」", 48)
        Thread.Sleep(1800)
        ui_mod.TypewriterEffect("\n\n    ベル「すごいね　こんな場所あったんだ」", 42)
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    錆びたスロットマシンが並んでいる", 42)
        Thread.Sleep(1800)
        ui_mod.TypewriterEffect("\n    天井の蛍光灯が　ひとつ　点滅している", 42)
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("\n\n    ベル「なんか...懐かしい気がする」", 42)
        Thread.Sleep(2000)
        ui_mod.TypewriterEffect("\n\n    ベル「来たことないはずなのに」", 42)
        Thread.Sleep(2200)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.White
        ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「大丈夫か？」", 42)
        Thread.Sleep(1800)
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("\n\n    ベル「うん♪　大丈夫　なんか　面白いじゃん」", 40)
        Thread.Sleep(2200)
        ui_mod.TypewriterEffect("\n\n    ベル「行ってみようよ」", 42)
        Thread.Sleep(2000)
        Console.clear()
        Console.ResetColor()
    AbandonedCasinoFloor1()

def PrintRoomOption(num, name, cost, opened):
    if opened:
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine(f"  [{num}] {name:<16}… 開放済み")
    else:
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine(f"  [{num}] {name:<16}… {cost}G")
    Console.ResetColor()

def OpenRoom(floor, room, cost, roomEvent):
    if len(st.roomsOpened[floor]) <= room:
        newArr = py_extend_bools(st.roomsOpened[floor], room + 1)
        st.roomsOpened[floor] = newArr
    if st.roomsOpened[floor][room]:
        roomEvent()
        return
    if cost > 0 and st.money < cost:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        ui_mod.TypewriterEffect("\n\n    お金が足りない...", 40)
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    if cost > 0:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect(f"\n\n    {cost}G　支払った", 40)
        Thread.Sleep(1500)
        st.money -= cost
    st.roomsOpened[floor][room] = True
    roomEvent()

def ExitAbandonedCasino():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「また来ようね♪」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    重い扉が　閉まった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ResetColor()

def AbandonedCasinoFloor1():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n\n    ══════════════════════════════")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("          廃娯楽施設　1階")
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("    ══════════════════════════════")
        Console.ResetColor()
        Console.WriteLine(f"\n    所持金：{st.money:,}G\n")
        r0 = len(st.roomsOpened[0]) > 0 and st.roomsOpened[0][0]
        r1 = len(st.roomsOpened[0]) > 1 and st.roomsOpened[0][1]
        r2 = len(st.roomsOpened[0]) > 2 and st.roomsOpened[0][2]
        r3 = len(st.roomsOpened[0]) > 3 and st.roomsOpened[0][3]
        r4 = len(st.roomsOpened[0]) > 4 and st.roomsOpened[0][4]
        allOpened = r0 and r1 and r2 and r3
        PrintRoomOption(1, "錆びた扉の先", 1500, r0)
        PrintRoomOption(2, "薄暗い通路", 500, r1)
        PrintRoomOption(3, "古い休憩室", 500, r2)
        PrintRoomOption(4, "奥の部屋", 500, r3)
        if allOpened:
            PrintRoomOption(5, "最奥の扉", 800, r4)
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???")
            Console.ResetColor()
        if r4:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("  [6] 階段（2階へ）　　　　　… 1500G")
            Console.ResetColor()
        Console.WriteLine("\n  [0] 廃娯楽施設を出る")
        Console.Write("\n  > ")
        key = Console.ReadKey(True)
        _sw17 = key.KeyChar
        if _sw17 == "1":
            OpenRoom(0, 0, 1500, Room1F_A)
        elif _sw17 == "2":
            OpenRoom(0, 1, 500, Room1F_B)
        elif _sw17 == "3":
            OpenRoom(0, 2, 500, Room1F_C)
        elif _sw17 == "4":
            OpenRoom(0, 3, 500, Room1F_D)
        elif _sw17 == "5":
            if allOpened:
                OpenRoom(0, 4, 800, Room1F_Final)
        elif _sw17 == "6":
            if r4:
                if st.money < 1500:
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.Red
                    ui_mod.TypewriterEffect("\n\n    お金が足りない...", 40)
                    Console.ResetColor()
                    Thread.Sleep(1500)
                else:
                    st.money -= 1500
                    GoToFloor2()
        elif _sw17 == "0":
            ExitAbandonedCasino()
            return

def Room1F_A():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    埃っぽい小部屋だった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    壁に　何かが貼ってある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「あ　なんか貼ってある♪」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「絵じゃん　子供が描いたやつ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    クレヨンで描かれた絵だ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    小さな女の子が　一人で立っている", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    周りには　誰もいない", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    でも　女の子は笑っている", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    足元に　小さな鈴が描いてある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...笑ってるんだ　その子」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「ああ　めちゃくちゃ笑ってる」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「一人なのに？」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「一人なのに」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...なんか　わかる気がする」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「一人でも　別に　さみしくなかった時期ってあるじゃん」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...お前の話か？」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「さあ♪　どうだろ」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「でも　なんか　懐かしい感じがする」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが少し笑った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    その絵の女の子みたいに", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片A入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片A入手")

def Room1F_B():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    薄暗い通路の奥に　小部屋があった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    床に　何かが落ちている", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 拾って見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    小さな靴だ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    子供用の　片方だけ", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    もう片方は　どこにもない", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「片方だけ？」", 42)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「ああ　もう片方はない」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...どこ行ったんだろ　もう片方」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが靴を受け取って　じっと見た", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「捨てた側か　なくした側かで　全然違う話だよね」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルがその靴を　元あった場所に　そっと戻した", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...なんか　置いてかれた感じがするね　この靴」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「まあ　いっか♪　次行こ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ResetColor()
    if not ("断片B入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片B入手")

def Room1F_C():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    古い休憩室だった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    テーブルが一つ　椅子が二つ", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    壁に　また絵が貼ってある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    手が二つ　描いてある", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    大きい手と　小さい手が　繋がっている", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    絵の下に　小さく文字が書いてある", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    「あたたかかった」", 48)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...あたたかかった」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「誰かに手を引いてもらったんだろうな」", 40)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...その人　好きだったんだと思う　この子」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「今もいるのかな　その人」", 42)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「いないんじゃないかな」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　椅子に少し寄りかかった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でも　あたたかかったって　覚えてるんだよ　この子」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「それって　いいことじゃん♪」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...強いな　お前」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「え♪　急に何」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「この子の話してるんだけど」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが笑った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    でも　少しだけ　目が笑ってなかった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片C入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片C入手")

def Room1F_D():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    奥の部屋は　他より少し広かった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    何もない部屋だ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    でも　床の真ん中に　一枚だけ紙が落ちている", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 紙を拾って読む\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    古い紙だ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    文字が書いてある", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    「ベル」", 55)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    それだけだ", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ベル？」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「お前と同じ名前だな」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「誰かがこの名前を　誰かのために書いたんだ」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　その紙を　大事そうに折りたたんだ", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「もらっていい？　これ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「ここのものだろ　お前が持ってていいんじゃないか」", 38)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん♪」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ResetColor()
    if not ("断片D入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片D入手")

def Room1F_Final():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    最奥の扉を開けると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    壁一面に　絵が貼ってある", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    さっきの絵が　ここにもある", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    笑ってる女の子", 42)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    大きな手と小さな手", 42)
    Thread.Sleep(1500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    床には　あの靴が　今度は両方揃って置いてある", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n    隣に　小さな鈴が一つ", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    壁の真ん中に　大きな紙が貼ってある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect("\n\n    「ベルへ", 48)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n\n     あなたが笑っていられますように", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n     どこにいても　あなたはベルだから」", 42)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...あ」", 52)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「これ」", 48)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「全部　私のだ」", 46)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...知ってたか？」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「知らなかった」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「でも　なんか　わかった気がする」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「誰かが　私のことを　思ってくれてたってこと」", 38)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「捨てられたって思ってたけど」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「...ちゃんと　思われてたんだ　私」", 40)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　鈴を一つ　そっと拾った", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「これ　持って帰っていい？」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「お前のもんだろ」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん♪」", 44)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが笑った", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    さっきより　少し　違う笑い方で", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         廃娯楽施設　1階")
    Console.WriteLine("         「ベルへ」　解放")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    st.memoryFragmentsCleared = True
    if not ("廃娯楽施設1階クリア" in st.unlockedEvents):
        st.unlockedEvents.append("廃娯楽施設1階クリア")

def GoToFloor2():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    階段を上ると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    2階は　1階より静かだった", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    空気が　少し重い", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「なんか　1階より緊張する」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「やめるか？」", 42)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「ううん♪　行く」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「...なんか　知らないといけない気がして」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    AbandonedCasinoFloor2()

def AbandonedCasinoFloor2():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n\n    ══════════════════════════════")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("          廃娯楽施設　2階")
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("    ══════════════════════════════")
        Console.ResetColor()
        Console.WriteLine(f"\n    所持金：{st.money:,}G\n")
        r0 = len(st.roomsOpened[1]) > 0 and st.roomsOpened[1][0]
        r1 = len(st.roomsOpened[1]) > 1 and st.roomsOpened[1][1]
        r2 = len(st.roomsOpened[1]) > 2 and st.roomsOpened[1][2]
        r3 = len(st.roomsOpened[1]) > 3 and st.roomsOpened[1][3]
        r4 = len(st.roomsOpened[1]) > 4 and st.roomsOpened[1][4]
        allOpened = r0 and r1 and r2 and r3
        PrintRoomOption(1, "重い扉", 2000, r0)
        PrintRoomOption(2, "細い廊下の先", 800, r1)
        PrintRoomOption(3, "窓のある小部屋", 800, r2)
        PrintRoomOption(4, "突き当たりの部屋", 800, r3)
        if allOpened:
            PrintRoomOption(5, "最奥の扉", 1200, r4)
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???")
            Console.ResetColor()
        if r4:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("  [7] 階段（3階へ）　　　　　… 2000G")
            Console.ResetColor()
        Console.WriteLine("  [6] 1階に戻る")
        Console.WriteLine("  [0] 廃娯楽施設を出る")
        Console.Write("\n  > ")
        key = Console.ReadKey(True)
        _sw18 = key.KeyChar
        if _sw18 == "1":
            OpenRoom(1, 0, 2000, Room2F_A)
        elif _sw18 == "2":
            OpenRoom(1, 1, 800, Room2F_B)
        elif _sw18 == "3":
            OpenRoom(1, 2, 800, Room2F_C)
        elif _sw18 == "4":
            OpenRoom(1, 3, 800, Room2F_D)
        elif _sw18 == "5":
            if allOpened:
                OpenRoom(1, 4, 1200, Room2F_Final)
        elif _sw18 == "6":
            AbandonedCasinoFloor1()
            return
        elif _sw18 == "7":
            if r4:
                if st.money < 2000:
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.Red
                    ui_mod.TypewriterEffect("\n\n    お金が足りない...", 40)
                    Console.ResetColor()
                    Thread.Sleep(1500)
                else:
                    st.money -= 2000
                    GoToFloor3()
        elif _sw18 == "0":
            ExitAbandonedCasino()
            return

def Room2F_A():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    重い扉を開けると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ハンガーが一本　立っている", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    そこに　コートがかかっていた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] コートをよく見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    古いコートだ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    子供用の小さいサイズだ", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ポケットに小さな飴玉が一つ　包み紙ごと", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...飴」", 48)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「ポケットに入ってた」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...あ」", 48)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「思い出した」", 44)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　少し遠くを見た", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「雨の日だった」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「外で　ずっと座ってたら」", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「でかいコートの人が来て　これくれたんだ」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「その人が　拾ってくれたのか」", 40)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「何も言わずに　ただ飴だけくれて」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「それで　手を引いて歩いてくれた」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　飴玉をそっとポケットに戻した", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「このコート　あの人のだ　きっと」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片2A入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片2A入手")

def Room2F_B():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    小さな部屋があった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    壁に絵が一枚　貼ってある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    テーブルを挟んで　二人が向き合って座っている絵だ", 38)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    一人は小さな子供　もう一人は大きな人", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    二人とも　笑っている", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ふふ」", 44)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「笑ってる」", 42)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「毎日ご飯作ってくれたんだよね　あの人」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「うまかったか？」", 42)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「おいしかった♪」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「全部おいしかった」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　絵の大きい人の方を指でなぞった", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「怒ったとこ　一回も見たことなかったな」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「ずっと笑ってた」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「いい人だったんだな」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「すごくいい人だった」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片2B入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片2B入手")

def Room2F_C():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    窓のある小部屋だった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    棚の上に　本が一冊置いてある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 本を手に取る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    古い本だ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ページを開くと　しおりが挟んである", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    ちょうど　半分あたりのページ", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    しおりの代わりに　小さなメモが挟んであった", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    「続きはまた今度」", 48)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...毎晩ね　眠くなるまで　読んでくれてた」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「半分で止まってる」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「ある朝　起きたら　いなかった」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「何も言わずに」", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「この本も　置いてったんだ」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「続き　読めないまま」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルの声が　いつもより少しだけ　低かった", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でも　まあ♪」", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ベル「読んでもらえた分だけ　よかったんだと思う」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片2C入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片2C入手")

def Room2F_D():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    突き当たりの部屋は　他より狭かった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    壁に　絵が一枚", 42)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 絵をよく見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    椅子が一つ　描いてある", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    誰も座っていない", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    椅子だけが　真ん中に　ぽつんとある", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    絵の下に　文字が書いてある", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    「いなくなった」", 48)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...」", 52)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「描いたのか　自分で」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...たぶん」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「さみしかったんだろうな　その子」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...お前じゃないのか」", 42)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「さあ♪」", 44)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ベル「でも　この椅子　誰かのために取っといたんだと思う」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「また来るかもって」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「来なかったけどね」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　小さく息を吐いた", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でも　いい人だったから　いっか♪」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「次行こ」", 44)
    Thread.Sleep(1800)
    Console.clear()
    Console.ResetColor()
    if not ("断片2D入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片2D入手")

def Room2F_Final():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    最奥の扉を開けると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    部屋の中に　テーブルが一つあった", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    あのコートが　椅子の背にかかっている", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    テーブルに　例の本が置いてある", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    テーブルの端に　小さなメモが一枚", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    「また来る　待ってろ」", 48)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...また来る」", 44)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　そのメモをじっと見た", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「待ってたんだ　私」", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「来なかったけど　ずっと待ってた」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...」", 52)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でもさ」", 44)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ベル「書いてくれてたんだよ　ちゃんと」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「また来るって」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「それだけでいいのか」", 42)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...十分じゃん♪」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　コートのポケットを触った", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n    飴玉が　まだそこにあった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「ねえ　これ食べていい？」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「古いだろそれ」", 42)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「いいじゃん別に♪」", 42)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　飴を口に入れた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...あまい」", 44)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「ちゃんと　あまい」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　小さく笑った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    泣いてるのか笑ってるのか　わからない顔で", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         廃娯楽施設　2階")
    Console.WriteLine("         「また来る」　解放")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("廃娯楽施設2階クリア" in st.unlockedEvents):
        st.unlockedEvents.append("廃娯楽施設2階クリア")

def GoToFloor3():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    階段を上ると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    3階は　暗かった", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    照明がほとんど切れている", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    煙草と　何か腐ったものの匂いが　残っていた", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...」", 52)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「知ってる場所か」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　いつもと違う顔をしていた", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n    笑っていない", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...行こ」", 44)
    Thread.Sleep(2000)
    Console.clear()
    Console.ResetColor()
    AbandonedCasinoFloor3()

def AbandonedCasinoFloor3():
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n\n    ══════════════════════════════")
        Console.ForegroundColor = ConsoleColor.White
        Console.WriteLine("          廃娯楽施設　3階")
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("    ══════════════════════════════")
        Console.ResetColor()
        Console.WriteLine(f"\n    所持金：{st.money:,}G\n")
        r0 = len(st.roomsOpened[2]) > 0 and st.roomsOpened[2][0]
        r1 = len(st.roomsOpened[2]) > 1 and st.roomsOpened[2][1]
        r2 = len(st.roomsOpened[2]) > 2 and st.roomsOpened[2][2]
        r3 = len(st.roomsOpened[2]) > 3 and st.roomsOpened[2][3]
        r4 = len(st.roomsOpened[2]) > 4 and st.roomsOpened[2][4]
        allOpened = r0 and r1 and r2 and r3
        PrintRoomOption(1, "鉄扉", 3000, r0)
        PrintRoomOption(2, "廊下の突き当たり", 1000, r1)
        PrintRoomOption(3, "裏の小部屋", 1000, r2)
        PrintRoomOption(4, "通用口の先", 1000, r3)
        if allOpened:
            PrintRoomOption(5, "最奥の扉", 2000, r4)
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("  [5] 最奥の扉　　　　　　　… ???")
            Console.ResetColor()
        if r4:
            Console.ForegroundColor = ConsoleColor.Yellow
            Console.WriteLine("  [7] 出口へ")
            Console.ResetColor()
        Console.WriteLine("  [6] 2階に戻る")
        Console.WriteLine("  [0] 廃娯楽施設を出る")
        Console.Write("\n  > ")
        key = Console.ReadKey(True)
        _sw19 = key.KeyChar
        if _sw19 == "1":
            OpenRoom(2, 0, 3000, Room3F_A)
        elif _sw19 == "2":
            OpenRoom(2, 1, 1000, Room3F_B)
        elif _sw19 == "3":
            OpenRoom(2, 2, 1000, Room3F_C)
        elif _sw19 == "4":
            OpenRoom(2, 3, 1000, Room3F_D)
        elif _sw19 == "5":
            if allOpened:
                OpenRoom(2, 4, 2000, Room3F_Final)
        elif _sw19 == "6":
            AbandonedCasinoFloor2()
            return
        elif _sw19 == "7":
            if r4:
                AbandonedCasinoExit()
                return
        elif _sw19 == "0":
            ExitAbandonedCasino()
            return

def Room3F_A():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    鉄扉の向こうは　フロアだった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    スロットマシンが並んでいる", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    カウンターの内側に　何かが引っかかっている", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 取って見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    エプロンだ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ひどく使い込まれている", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    子供用の小さいサイズだ", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    胸のあたりに　茶色い染みがある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「それ　私のだ」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「子供のころから　ここで働いてたのか」", 38)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「雇ってもらえたから」", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「他に行く場所　なかったし」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「どんな仕事をしてたんだ」", 42)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...なんでも」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「言われたことは　全部やってた」", 40)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「...それだけじゃ　ないこともあったけど」", 36)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　そこで言葉を止めた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「聞かないで」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    静かに言った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    ただ　話せないだけだ　という顔だった", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...次　行こ」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ResetColor()
    if not ("断片3A入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片3A入手")

def Room3F_B():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    廊下の突き当たりに　絵が一枚　貼ってあった", 38)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 絵を見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    小さな子が　トレーを持って立っている絵だ", 38)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    顔のところが　黒いクレヨンで　ぐるぐると塗りつぶされている", 36)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    周りに　大人が何人か描いてある", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    全員　笑っている", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「顔　塗りつぶしてあるね」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「描きたくなかったのか」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...どんな顔してたか　わかんなかったんじゃないかな」", 34)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「自分の顔が　わかんない？」", 40)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「笑えって言われてたから　笑ってたけど」", 36)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「...本当に笑ってたかどうかは　わかんない」", 36)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...今は　わかるか」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...今は」", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「笑ってるときは　笑ってるってわかる」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    それだけ言って　ベルは黙った", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片3B入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片3B入手")

def Room3F_C():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    裏の小部屋は　物置だった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    棚にがらくたが積んである", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    その中に　金属の光るものがあった", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 取り出して見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ネームプレートだ", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    二つに折れている", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    読める部分は「ベ」だけだ", 46)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ああ　これ」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「折られたのか」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「うん」", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「名前なんかいらないって」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「客に名前で呼ばれたら　なれなれしいから」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「じゃあ　なんて呼ばれてたんだ」", 40)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「おい　とか　お前　とか」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「...気に入った客はベルって呼んでくれたけど」", 34)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　そのネームプレートを両手で持った", 38)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「合わせたら　ベルって読めるから」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「...それでよかった」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　折れたネームプレートを　ポケットにしまった", 36)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片3C入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片3C入手")

def Room3F_D():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    通用口の先に　小さな部屋があった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    窓がない", 44)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    鍵穴だけある　外から鍵をかける仕様の扉が一つ", 36)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「ここで　寝てた」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...外から　鍵をかけられるのか　この扉」", 36)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「逃げないようにって」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　淡々と言った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    当たり前のことを言うように", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    部屋の天井に　何かが描いてある", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 天井を見る\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    星だ", 46)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    天井いっぱいに　星が描いてある", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    クレヨンで　一つひとつ　丁寧に", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    窓がない部屋なのに", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    天井だけ　夜空だ", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「暗くて　怖かったから」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「星があれば　外にいる気がするかなって」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...何歳のときだ　これ描いたの」", 38)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...何歳からかな」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　天井を見上げた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「きれいでしょ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    きれいだと思った", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    同時に　胸が痛かった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...ああ　きれいだ」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「でしょ♪」", 44)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　初めて笑った", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    3階に来てから　初めて", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    if not ("断片3D入手" in st.unlockedEvents):
        st.unlockedEvents.append("断片3D入手")

def Room3F_Final():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    最奥の扉を開けると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    オーナー室だった", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    机の上に　ものが並べてある", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    たたまれたエプロン", 42)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    折れたネームプレート", 42)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    誰かが描いた　顔のない絵", 42)
    Thread.Sleep(1800)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    引き出しが　少し開いていた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 引き出しを開ける\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    封筒が一つ入っていた", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    「ベルへ」", 52)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...」", 55)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「開けるか」", 44)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...開けて」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect("\n\n    「ベルへ", 50)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n     俺がお前にしたことは　最低だった", 44)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n     わかっていた　やめなかった", 44)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n     お前がいたから　ここは回っていた", 42)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n     名前を折ったこと　謝る", 44)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n     鍵をかけたこと　謝る", 44)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n     それ以外のことも　全部」", 44)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...」", 55)
    Thread.Sleep(3500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　動かなかった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「謝られても」", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「...もう死んでんじゃん」", 40)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルの声が　震えていた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「許してあげたかったのに」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「直接　言えなかった」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    泣いていた", 44)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...手紙　置いてく」", 42)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「ここのものだから　ここにあっていい」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　手紙を机に戻した", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...来てくれてよかった」", 40)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         廃娯楽施設　3階")
    Console.WriteLine("         「来てくれてよかった」　解放")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("廃娯楽施設3階クリア" in st.unlockedEvents):
        st.unlockedEvents.append("廃娯楽施設3階クリア")

def AbandonedCasinoExit():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    出口へ向かった", 42)
    Thread.Sleep(2000)
    Console.clear()
    if st.timeClockEquipped:
        ui_mod.TypewriterEffect("\n\n    廊下を歩いていると", 42)
        Thread.Sleep(1800)
        ui_mod.TypewriterEffect("\n\n    何かが　引っかかった", 42)
        Thread.Sleep(2000)
        Console.clear()
        ui_mod.TypewriterEffect("\n\n    壁の一部が　他と少し違う", 42)
        Thread.Sleep(2000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Cyan
        ui_mod.TypewriterEffect("\n\n    ベル「...あそこ　なんか変じゃない？」", 40)
        Thread.Sleep(2200)
        Console.clear()
        BasementDoorFound()
        return
    AbandonedCasinoExitEvent()

def AbandonedCasinoExitEvent():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    重い扉を開けると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    外の空気が流れてきた", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    黒服の男が　壁に寄りかかっていた", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「遅かったな」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「全部　見てきたか」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...お前が待ってたのか」", 42)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「当たり前だろ　俺のカジノなんだから」", 36)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「遺言で　私がオーナーって　決まってたのに」", 36)
    Thread.Sleep(2800)
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「だから　消えてもらった」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服が　ゆっくりと近づいてきた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    ui_mod.TypewriterEffect("\n\n    ベル「...っ」", 44)
    Thread.Sleep(1500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    音がした", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベルが　崩れ落ちた", 42)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    playerは　動けなかった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ごめん」", 44)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    それだけ言って", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ベルは　動かなくなった", 42)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         ENDING")
    Console.WriteLine("         「ごめん」")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Thread.Sleep(4000)
    Console.clear()
    Console.ResetColor()
    if not ("バッドエンド:ごめん" in st.unlockedEvents):
        st.unlockedEvents.append("バッドエンド:ごめん")

def BasementDoorFound():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    壁を押すと　重い音がして", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    隠し扉が　開いた", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    階段が　下に続いている", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n    暗い　かなり深い", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...なんだろ　ここ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 降りる\n    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    BasementEvent()

def BasementEvent():
    if not st.hasInnocentGem:
        ExitAbandonedCasino()
        return
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    階段を降りると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    冷たい空気が　体を包んだ", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    広い部屋だった", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    中央に　白い布が　かけられている", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    [1] 布をめくる\n    [0] やめる")
    Console.Write("\n    > ")
    Console.ResetColor()
    if Console.ReadKey(True).KeyChar != "1":
        return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    布の下に　人が横たわっていた", 42)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    小さい", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    よく知っている顔だった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...」", 55)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「これは　お前じゃないか」", 40)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...うん」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「私だ」", 44)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「なんで　お前が殺されなきゃいけなかったんだ」", 34)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「オーナーの遺言で　私がここの次のオーナーって　決まってたから」", 32)
    Thread.Sleep(3000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「あの人　それが嫌だったんだよね」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　笑おうとした", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    笑えなかった", 44)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「なんか　あっけないよね", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「やっと　自分の場所だって思ってたのに」", 36)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルの声が　少し　揺れた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「怖かったんだよ　本当は」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「ずっと　どこかに捨てられるんじゃないかって」", 34)
    Thread.Sleep(3000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「笑ってれば　大丈夫だって思ってたから　笑ってた」", 34)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　亡骸から目を逸らした", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...でも　結局こうなった」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「笑ってても　捨てられた」", 40)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルの声が　震えていた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...悔しい」", 44)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「あなたと一緒にいて　初めて　笑えてた気がしてたのに」", 32)
    Thread.Sleep(3200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「みっともなくない」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    しばらく　何も言わなかった", 42)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ポケットの中が　光った", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    取り出すと　無垢な宝石だった", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...きれいだね」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「お前のものだろ　たぶん」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ねえ", 44)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    ベル「私　ここで終わりたくない」", 40)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「あなたのそばにいたい」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「まだ　一緒にいたい」", 42)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...来い」", 46)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「一生ついてく」", 46)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「どこにいても　ずっと　絶対」", 40)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    宝石が　強く光った", 42)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    for i in range(0, 4):
        Console.clear()
        Console.WriteLine(("\n\n\n\n         ✦" if i % 2 == 0 else "\n\n\n\n      ✦     ✦"))
        Thread.Sleep(300)
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルの姿が　宝石に吸い込まれていった", 38)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    宝石が　指輪に変わった", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「聞こえる？」", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「ちゃんと　ここにいるから」", 40)
    Thread.Sleep(2500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベル「だから　前向いて」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         アイテム入手！")
    Console.WriteLine("         「宝石のついた指輪」")
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n         ベルが宿る指輪。")
    Console.WriteLine("         これで君が救われるのであれば、")
    Console.WriteLine("         僕はすべてを背負う。")
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    st.hasInnocentGem = False
    st.hasJewelRing = True
    if not ("宝石のついた指輪入手" in st.unlockedEvents):
        st.unlockedEvents.append("宝石のついた指輪入手")
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    地下室を出た", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    黒服が　そこにいた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
    BlackSuitFinalConfrontation()

def BlackSuitFinalConfrontation():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「...なんだ　お前」", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「なんでここに　いる」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服が　初めて　動揺した顔をした", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「全部　知ってる」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「...知って　どうする」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「証拠もない　誰も信じない」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    指輪が　光った", 44)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「...私が証拠だよ」", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「な　...っ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「全部　覚えてるから」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect("\n\n    ベル「消えてても　忘れてないから」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服が　後退った", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    どうする")
    Console.WriteLine("\n    [1] このカジノはベルのものだと言う")
    Console.WriteLine("    [2] 黒服を追い詰める")
    Console.Write("\n    > ")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.KeyChar == "1":
        EndingRouteA_Owner()
    else:
        EndingRouteB_Bell()

def EndingRouteA_Owner():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「このカジノは　ベルのものだ」", 40)
    Thread.Sleep(2200)
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「遺言がそう言ってる　お前がなんと言おうと」", 34)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「...証明できるのか」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「できるよ♪」", 44)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「オーナーが書いた遺言書　地下室にあったから」", 34)
    Thread.Sleep(2800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服の顔が　青ざめた", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「...くそっ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服が　その場を去った", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「...やったね♪」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「これからどうする　このカジノ」", 38)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「あなたに任せる♪」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「私は　ここにいるから」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    指輪が　温かかった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Green
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         ENDING　A")
    Console.WriteLine("         「ここにいるから」")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    st.bellRouteACompleted = True
    if not ("エンディングA:ここにいるから" in st.unlockedEvents):
        st.unlockedEvents.append("エンディングA:ここにいるから")

def EndingRouteB_Bell():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「お前がやったことは　消えない」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「だから　なんだ」", 40)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「このカジノは　私のものだった」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「でも　もういらない」", 42)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「ベル？」", 44)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「こんな場所に縛られたくない」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「私は　あなたと行く」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    指輪が　強く光った", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    廃娯楽施設の壁に　ひびが入った", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    天井が　崩れ始めた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「なんだ　なんなんだ　これは！」", 34)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    黒服が　逃げていった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    ベル「行こ♪」", 46)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...ああ」", 44)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    廃娯楽施設が　崩れていった", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    指輪だけが　光っていた", 42)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         ENDING　B")
    Console.WriteLine("         「行こ」")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    st.bellRouteBCompleted = True
    if not ("エンディングB:行こ" in st.unlockedEvents):
        st.unlockedEvents.append("エンディングB:行こ")

def UnknownCoinFlip(bet, multiplier):
    Console.clear()
    Thread.Sleep(300)
    Console.ForegroundColor = ConsoleColor.Yellow
    ui_mod.TypewriterEffect("\n\n    ポケットの中で　何かが動いた", 42)
    Thread.Sleep(1500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    知らない硬貨が　宙に浮いている", 42)
    Thread.Sleep(1800)
    Console.clear()
    frames = [ "  〇", "  ◎", "  ●", "  ◎", "  〇" ]
    for f in frames:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n\n\n" + f)
        Thread.Sleep(200)
    Console.clear()
    Thread.Sleep(500)
    isFront = st.rand.Next(2) == 0
    if isFront:
        Console.ForegroundColor = ConsoleColor.Yellow
        ui_mod.TypewriterEffect("\n\n    表", 60)
        Thread.Sleep(1000)
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    嘘は嘘", 50)
        Thread.Sleep(1000)
        ui_mod.TypewriterEffect("\n\n    それはくるりと　裏返る", 45)
        Thread.Sleep(1500)
        Console.clear()
        winAmount = bet * 2 * multiplier
        st.money += winAmount
        st.totalWinAmount += winAmount
        st.consecutiveWins += 1
        st.consecutiveLosses = 0
        st.unknownCoinFlipCount += 1
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━")
        Console.WriteLine("         外れが　裏返った！")
        Console.WriteLine(f"         +{winAmount:,}G")
        Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
        Console.ResetColor()
        Thread.Sleep(2500)
        if not ("コイントス成功" in st.unlockedEvents):
            st.unlockedEvents.append("コイントス成功")
    else:
        Console.ForegroundColor = ConsoleColor.DarkGray
        ui_mod.TypewriterEffect("\n\n    裏", 60)
        Thread.Sleep(1000)
        Console.clear()
        ui_mod.TypewriterEffect("\n\n    ...今回は　そのまま", 42)
        Thread.Sleep(1500)
        Console.clear()
        Console.ResetColor()
