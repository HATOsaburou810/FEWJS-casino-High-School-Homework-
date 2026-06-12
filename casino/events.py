# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — ランダム・ストーリーイベント (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod
from . import endings


def BlackSuitArrival():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("              コツ...")
    Console.WriteLine("              コツ...")
    Thread.Sleep(1500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n    黒服の男たちが現れた...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「金に困ってるようだな...」")
    Thread.Sleep(1500)
    Console.WriteLine("\n    「500G貸してやるよ」")
    Thread.Sleep(1500)
    Console.WriteLine("\n    「...ただし、20回転以内に返せよ」")
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    500Gを受け取った...")
    Console.ResetColor()
    Thread.Sleep(2000)

def RandomConversationEvent():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n謎のおじさんが話しかけてきた...\n")
    Thread.Sleep(1500)
    messages = [ "「このスロット、実は設定というものがあってな...」", "「777を3回揃えると、黒服が来るって噂だぜ」", "「100Gを20回連続で賭けると...何かが起きるらしい」", "「借金は怖いぞ...返せなくなったら...」", "「強欲の指輪って...知ってるか？...知らないなら別にいい...」", ]
    Console.WriteLine(f"    {messages[st.rand.Next(len(messages))]}")
    Thread.Sleep(3000)
    Console.WriteLine("\n    おじさんは去っていった...")
    Thread.Sleep(2000)

def MysteriousWomanEvent():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n\n    美しい女性が近づいてきた...", 55)
    Thread.Sleep(1800)
    # 状況によって登場セリフを変える
    greeting = ""
    if st.addictionLevel >= 70:
        greeting = "    「...また来てたのね」"
    elif st.debt >= 5000:
        greeting = "    「大変そうね...受け取って」"
    elif st.total777Count >= 3:
        greeting = "    「あなた...何かを持ってるわね」"
    else:
        greeting = "    「あなた...運が良さそうね」"
    Console.ForegroundColor = ConsoleColor.Magenta
    ui_mod.TypewriterEffect("\n" + greeting, 55)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    「これを...受け取って」", 55)
    Thread.Sleep(1500)
    # ========== お小遣いをピンキリに ==========
    # 状況・運次第で大きく変わる
    bonus = 0
    bonusComment = ""
    roll = st.rand.Next(100)
    if roll < 5:
        # 超レア: 大金
        bonus = st.rand.Next(3000, 8001)
        bonusComment = "    ...思いがけない大金だった"
    elif roll < 15:
        # レア: まとまった額
        bonus = st.rand.Next(800, 2001)
        bonusComment = "    ...かなりの額だった"
    elif roll < 40:
        # やや多め
        bonus = st.rand.Next(300, 801)
        bonusComment = "    ...そこそこの額だった"
    elif roll < 70:
        # 普通
        bonus = st.rand.Next(100, 301)
        bonusComment = ""
    elif roll < 88:
        # 少ない
        bonus = st.rand.Next(20, 101)
        bonusComment = "    ...少し、拍子抜けした"
    elif roll < 96:
        # ほぼ意味なし
        bonus = st.rand.Next(1, 20)
        bonusComment = "    ...気持ちだけ受け取った"
    else:
        # 借金中毒状態だと1Gもあり得る
        bonus = 1
        bonusComment = "    ...1Gだった"
    # 借金が多いとボーナス増加傾向
    if st.debt >= 10000:
        bonus = int(bonus * 1.5)
    # 中毒度が高いと減少傾向
    if st.addictionLevel >= 80:
        bonus = Math.Max(1, bonus // 2)
    st.money += bonus
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine(f"\n\n    {bonus:,}G を受け取った！")
    Console.ResetColor()
    if bonusComment != "":
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine(bonusComment)
        Console.ResetColor()
    Thread.Sleep(1800)
    # ========== ヒントセリフ（内容もピンキリ） ==========
    hints = [ "    「この下には、黒服がいる...気をつけて」", "    「監視されている...」", "    「強欲の指輪には気をつけて...」", "    「幸運のコインは...本当に幸運を呼ぶのかしら...」", "    「借金は...あなたを壊すわ...」", "    「夢と現実の境目が、薄くなってるわ...」", "    「悪魔と取引してはダメ...絶対に」", "    「あの店の子...あなたのことを待ってるわよ」", "    「777は...偶然じゃないことがある」", "    「...次、いつ来るの？」",  "    「...」",  ]
    hint = hints[st.rand.Next(len(hints))]
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    ui_mod.TypewriterEffect("\n" + hint, 55)
    Thread.Sleep(2500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    女性は微笑んで去っていった...", 55)
    Console.ResetColor()
    Thread.Sleep(2000)
    if not ("謎の女性" in st.unlockedEvents):
        st.unlockedEvents.append("謎の女性")

def Devilmonster():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         悪魔の怪物 現る！")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    画面に悪魔の怪物が映し出された...")
    Thread.Sleep(2000)
    Console.WriteLine("\n    「お前の魂を賭けろ...」")
    Thread.Sleep(2000)
    penalty = st.money // 2
    st.money -= penalty
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine(f"\n    悪魔の怪物に魂を奪われ、所持金が半分に減った... -{penalty}G")
    Console.ResetColor()
    Thread.Sleep(3000)

def BlackSuitWarningEvent():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n\n")
    Console.WriteLine("              コツ...")
    Console.WriteLine("              コツ...")
    Thread.Sleep(1000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n        _______________\n       |  ___________  |\n       | |           | |\n       | |  黒服が   | |\n       | |  近づく   | |\n       | |___________| |\n       |_______________|\n\n             ■■■\n            ■■■■■\n           ■■■■■■\n            ■■■■■\n           ■  ■  ■\n          ■■■■■■■\n         ■■■■■■■■■\n            ■■■■■\n            ■■  ■■\n            ■■  ■■\n           ■■■ ■■■")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n       「調子に乗るなよ...」")
    Thread.Sleep(2000)
    Console.WriteLine("\n       黒服たちは去っていった...")
    Thread.Sleep(2000)

def DebtCollectionEvent():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ================================")
    Console.WriteLine("         借金取り立て発生！")
    Console.WriteLine("    ================================")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n    黒服たちがやってきた...")
    Thread.Sleep(2000)
    if st.itemInventory["返済猶予券"] > 0:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine("\n\n    返済猶予券を使用しますか？ [Y/N]")
        Console.ResetColor()
        useTicket = Console.ReadKey(True)
        if useTicket.Key == ConsoleKey.Y:
            st.itemInventory["返済猶予券"] -= 1
            st.debtTurnsRemaining = 10
            st.money += 100
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine("\n\n    返済猶予券を使用した！")
            Console.WriteLine("    期限が10回延長され、100G獲得した！")
            Console.ResetColor()
            Thread.Sleep(3000)
            return
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("\n\n    [1] 過酷な労働で返済")
    Console.WriteLine("    [2] 楽に終わらせる")
    Console.ResetColor()
    Console.Write("\n選択 > ")
    choice = Console.ReadKey(True)
    if choice.KeyChar == "1":
        endings.LaborEnding()
    else:
        endings.ExecutionEnding()
# ========== 強欲の指輪関連 ==========

def GreedRingEquipAnimation():
    Console.clear()
    for i in range(0, 5):
        Console.clear()
        Console.BackgroundColor =(ConsoleColor.DarkRed if i % 2 == 0 else ConsoleColor.Black)
        Console.ForegroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.Red)
        Console.WriteLine("\n\n\n")
        Console.WriteLine("    💀💀💀💀💀💀💀💀💀💀💀💀💀")
        Console.WriteLine("    💀                              💀")
        Console.WriteLine("    💀    強欲の指輪 装備！       💀")
        Console.WriteLine("    💀                              💀")
        Console.WriteLine("    💀   邪悪なオーラが纏う...    💀")
        Console.WriteLine("    💀                              💀")
        Console.WriteLine("    💀💀💀💀💀💀💀💀💀💀💀💀💀")
        Console.ResetColor()
        Thread.Sleep(300)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n指輪から黒い霧が溢れ出す...")
    Thread.Sleep(2000)
    Console.WriteLine("\n全身が邪悪なオーラに包まれた！")
    Thread.Sleep(2000)
    Console.WriteLine("\n\n...もっと...もっと賭けろ...")
    Thread.Sleep(2000)
    Console.ResetColor()

def GreedWhisperEvent():
    Console.clear()
    Console.BackgroundColor = ConsoleColor.DarkRed
    Console.ForegroundColor = ConsoleColor.Black
    Console.WriteLine("\n\n\n")
    whispers = [ "...もっと...もっと賭けろ...", "...全てを賭けるのだ...", "...欲望のままに...", "...恐れるな...賭け続けろ...", "...富を...無限の富を..." ]
    Console.WriteLine(f"    {whispers[st.rand.Next(len(whispers))]}")
    Console.ResetColor()
    Thread.Sleep(2500)

def Chapter1_FirstConversation():
    Console.clear()
    Thread.Sleep(800)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n\n    カラン..カランと店の呼び鈴が鳴った", 35)
    Thread.Sleep(1500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    店の中に入り　カウンターにいるベルに目をやる", 35)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}：「来ちゃった」", 40)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「...」", 40)
    Thread.Sleep(1200)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n    {st.playerName}：「...」", 40)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    いつもなら元気のある声が聞こえるはずが　今日はやけに静かだ", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    すると　「はっ！」とした勢いで私の方を見て　思い出したかのように", 35)
    Thread.Sleep(500)
    ui_mod.TypewriterEffect("\n\n    ベル：「..! い、いらっしゃい！！」", 45)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n\n    ベル：「あ、なーんだ。あなただったのですね。」", 40)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    そう言い終えると　また静かになってしまった", 35)
    Thread.Sleep(2200)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}：「どうしたんだ？　いつもとは違って変だけど　何かあったの？」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルは少し考えた様子を見せた後　私に話してくれた", 35)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「実はね　最近ここのオーナーが亡くなったんだ」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル：「でね　これからのオーナーは誰なのか　オーナー争いが始まっちゃったの..」", 38)
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    少しため息交じりに話してくれた", 35)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}：「でも　なんで君が落ち込む必要があるのさ」", 40)
    Thread.Sleep(2200)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「それがね　オーナーは私の..」", 40)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    カランカラン", 60)
    Thread.Sleep(1500)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    入り口を見るとそこには黒服の男が立っていた", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect(f"\n\n    黒服の男：「おい　{st.playerName}!! 確か借金を滞納していたなぁ！！」", 38)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「えぇ；　そうなの？」", 40)
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}：「いやいや！　滞納なんかしたことないし身に覚えもないよ；；」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    と言ってみたものの　実際にあるかもしれない..", 35)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ...何故だ？　なぜ私は逃げようと...", 35)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    なおのこと堂々としていた方がいいのではないのだろうか？", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    ui_mod.TypewriterEffect("\n\n    まずい　このままでは", 35)
    Thread.Sleep(1000)
    ui_mod.TypewriterEffect("\n    最悪な状況だ...", 35)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「..ふっ」", 45)
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ？", 60)
    Thread.Sleep(1500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「ふはははは！　冗談だよ！　冗談！　はははは！」", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「なんなんですか？　冷やかしなら帰ってください！」", 40)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    怒りをあらわにしながら注意をすると　黒服の男は冷静になった", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「すまんな　話が合ってきたんだ」", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「お前たちも知っての通り　このカジノにはオーナーがいない」", 38)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「ならばこの俺が　なってやろうじゃないか！　って話さ」", 38)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    なんとなくこの先が手に取って見える..", 35)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    わかってるよ　俺に入れろよって話だろうな...", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「俺に入れろ！」", 45)
    Thread.Sleep(1500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ほ～ら　やっぱり；；", 35)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}：「嫌と言ったら？」", 45)
    Thread.Sleep(2000)
    Console.ForegroundColor = ConsoleColor.DarkYellow
    ui_mod.TypewriterEffect("\n\n    黒服の男：「俺の口から聞きたいか？」", 40)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    黒服の男：「風のうわさになって聞いた方がいいだろう」", 38)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    といい終わって「じゃ」っといって店をあとにして行った", 35)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル：「はぁ～　やっぱりあの人嫌い」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    なんとなく気まずい空気になってしまって", 35)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    軽くあいさつを交わし　店をあとにした...", 35)
    Thread.Sleep(3000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         Chapter 1")
    Console.WriteLine("         「最初の会話」")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    st.blackSuitIntroduced = True
    if not ("チャプター1完了" in st.unlockedEvents):
        st.unlockedEvents.append("チャプター1完了")

def InnocentGemFound():
    Console.clear()
    Thread.Sleep(800)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    目が覚めると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    足元に　何かが光っていた", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    拾い上げると", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    宝石だった", 44)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    色がない", 44)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    形も　特にない", 42)
    Thread.Sleep(1800)
    ui_mod.TypewriterEffect("\n\n    でも　なんでも取り込んでしまいそうな", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    美しい宝石だった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         アイテム入手！")
    Console.WriteLine("         「無垢な宝石」")
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("\n         それはただの無。")
    Console.WriteLine("         色も形も特にない。")
    Console.WriteLine("         だが、なんでも取り込んでしまいそうな")
    Console.WriteLine("         美しい宝石。")
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(3500)
    st.hasInnocentGem = True
    if not ("無垢な宝石入手" in st.unlockedEvents):
        st.unlockedEvents.append("無垢な宝石入手")
