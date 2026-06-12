# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — ショップ (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st
from . import ui as ui_mod
from . import dream

        # ShowEnding が終わったらループ先頭に戻り、タイトルへ

def GetBellGreeting():
    hour = DateTimeNS.Now.Hour
    # 初回
    if not st.bellMetFirst:
        st.bellMetFirst = True
        return "あら、いらっしゃい♪\n    待ってたわよ？ここには素敵なものが揃ってるから、ゆっくり見ていってね"
    # 中毒度MAX — 素が出る
    if st.addictionLevel >= 90:
        maxAddicted = [ "…また来たの。\n    …もう、止めてって言っても聞かないわよね。わかってる♪", "顔…ひどいわよ？\n    …でも、来てくれるのは嬉しい。複雑だわ♪", "あなたのこと…心配してるわけじゃないけど\n    …心配してる。うん、してる♪", "…お金なくなっても、来ていいのよ？\n    …ここにいると、安心でしょ？", "…あなたが来ないと、なんか…落ち着かないの\n    …変よね♪ 私", "また来たのね♪\n    …来るって、わかってた。ずっと待ってたから", ]
        return maxAddicted[st.rand.Next(len(maxAddicted))]
    # 中毒度高め
    if st.addictionLevel >= 50:
        addicted = [ "…また来たの\n    …いつ寝てるの？♪", "顔色…大丈夫？\n    まあ、来てくれるのは嬉しいけど♪", "少し休んだら？\n    …なんて、言っても無駄よね♪", "…リハビリ、考えてみる？\n    …本気で言ってるの。ふざけてないわよ", ]
        return addicted[st.rand.Next(len(addicted))]
    # 悪魔契約中
    if st.devilContractActive:
        contract = [ "…なんか、空気が重い気がするわ\n    気のせいかしら♪", "…あなた、何かした？\n    聞かなくてもわかるけど♪", "最近ツいてるじゃない♪\n    …でも、なんか怖いわね", ]
        return contract[st.rand.Next(len(contract))]
    # 借金が高額
    if st.debt >= 10000:
        bigDebt = [ "…借金、増えてるじゃない\n    …大丈夫なの？本当に？", "顔色悪いわよ。ここに来てる場合じゃないんじゃない？\n    …まあ、来てくれたけど♪", "…ねえ、少しだけ話せる？\n    …なんでもないわ、いらっしゃい♪", ]
        return bigDebt[st.rand.Next(len(bigDebt))]
    # 地下カジノ解放後（2回に1回）
    if st.undergroundUnlocked and st.rand.Next(2) == 0:
        underground = [ "…地下にも行ってるの？\n    気をつけてね♪ …本当に", "あっちには近づかない方がいいと思うけど\n    …まあ、止めないわ♪", "帰ってきたのね♪\n    …無事でよかった。本当に", "…あそこの人たち、目が怖いわよね\n    あなたはまだ大丈夫そうだけど♪", ]
        return underground[st.rand.Next(len(underground))]
    # VIPルーム解放後（3回に1回）
    if st.vipRoomUnlocked and st.rand.Next(3) == 0:
        vip = [ "VIPルームにも行くのね♪\n    …どっちが好き？", "最近羽振りがいいじゃない♪\n    …うらやましいわ", "VIPの常連さんになったの？\n    …私のことも忘れないでね♪", "向こうのディーラー、綺麗よね♪\n    …なんでもない。いらっしゃい", ]
        return vip[st.rand.Next(len(vip))]
    # 777を複数回
    if st.total777Count >= 5:
        veryLucky = [ "777、また揃えたの？\n    …もうあなた、普通じゃないわよ♪", "神様に愛されてるのかしら\n    …それとも悪魔に？♪", ]
        if st.rand.Next(2) == 0:
            return veryLucky[st.rand.Next(len(veryLucky))]
    if st.total777Count >= 3:
        lucky = [ "777、また揃えたの？\n    …化け物ね♪", "運がいいのね♪\n    …それとも、何か持ってる？", "三度目の777…\n    …本物のギャンブラーね♪", ]
        if st.rand.Next(2) == 0:
            return lucky[st.rand.Next(len(lucky))]
    # 連敗中
    if st.consecutiveLosses >= 10:
        bigLosing = [ "…10連敗…？\n    …少し、休もっか♪", "顔が死んでるわよ？\n    …まあ、ここに来てくれる分にはいいけど♪", "ねえ、少し笑って？\n    …ダメ？ そうよね♪", ]
        return bigLosing[st.rand.Next(len(bigLosing))]
    if st.consecutiveWins == 0 and st.totalLoses > 0 and st.totalLoses % 5 == 0:
        losing = [ "…今日は運が悪いわね\n    明日にしたら？♪", "負けが続いてるじゃない\n    …大丈夫？♪", "ここに来ると少し落ち着く？\n    …それならいいけど♪", ]
        return losing[st.rand.Next(len(losing))]
    # 深夜 × 中毒度高い → 素が出る
    if (hour >= 22 or hour < 5) and st.addictionLevel >= 60:
        lateAddicted = [ "こんな時間に…\n    …でも来てくれた♪ 嬉しい。本当に", "眠れないの？\n    …ここにいれば、眠くなるまで付き合うわよ♪", "…ねえ、家族とか、友達は？\n    …余計なこと聞いたわね。ごめん♪", "こんな時間まで…\n    …あなた以外、誰もいないのよここ。だから嬉しい♪", ]
        return lateAddicted[st.rand.Next(len(lateAddicted))]
    # 深夜（通常）
    if hour >= 22 or hour < 5:
        lateNight = [ "こんな時間に来るなんて…\n    …大丈夫？ まあ、大丈夫じゃないわよね♪", "眠れないの？\n    …私もよ。だから待ってたけど♪", "こんな時間まで…\n    …まあ、会えたから嬉しいけど♪", ]
        return lateNight[st.rand.Next(len(lateNight))]
    # リッチ
    if st.money >= 20000:
        veryRich = [ "…すごいわね。ほんとに♪\n    そのお金、夢みたい", "大金持ちのお客様♪\n    …でも、ここに来てくれてるのね", ]
        if st.rand.Next(2) == 0:
            return veryRich[st.rand.Next(len(veryRich))]
    if st.money >= 5000:
        rich = [ "随分稼いでるじゃない。すごいわね♪\n    …そのお金、大事にしてね？", "また来たのね♪ お金持ちのお客様は大歓迎よ", "調子いいじゃない♪\n    …羨ましいわ、少し", ]
        return rich[st.rand.Next(len(rich))]
    # 借金あり
    if st.debt > 0:
        inDebt = [ "…顔色悪いわよ？\n    まあ、私には関係ないけど♪", "借金があっても来てくれるのね。…うれしい♪", "…返せそう？\n    …余計なお世話よね。ごめん♪", "大変そうね…\n    …でも、ここに来るのはやめないのね♪", ]
        return inDebt[st.rand.Next(len(inDebt))]
    # よく来るお客様
    if st.shopVisitCount >= 20:
        regular = [ f"…{st.shopVisitCount}回目よ、もう♪\n    顔覚えちゃったわ", "また来たわね♪\n    …もう常連さんね。嬉しいわ、本当に", "いつもありがとう♪\n    …なんか、いてくれると安心するわ", ]
        if st.rand.Next(3) == 0:
            return regular[st.rand.Next(len(regular))]
    # 何も買わずに来た回数
    if st.shopCloseWithoutBuyCount >= 3:
        return f"また来たのね。{st.shopCloseWithoutBuyCount}回目よ♪\n    …今日こそ買うの？"
    # 通常
    normal = [ "また来たのね♪ やっぱり来ると思ってた", "いらっしゃい♪ 今日は何にする？", "来てくれると思ってたわ♪", "あら♪ また会えたわね", "待ってたわよ♪\n    …嘘じゃないの", "いらっしゃい♪\n    …来るの、わかってたわよ？", ]
    return normal[st.rand.Next(len(normal))]

def GetBellPurchaseComment(itemName):
    if itemName == "悪魔のコイン" or itemName == "血塗られたお守り" or itemName == "死神の指輪" or itemName == "時を刻む懐中時計" or itemName == "禁断の水晶玉":
        cursed = [ "…本当にいいの？ まあ、あなたが選んだことだから♪", "似合いそう。すごく♪", "…止めませんよ。止める権利もないので♪", ]
        return cursed[st.rand.Next(len(cursed))]
    # 悪魔契約中の購入コメント
    if st.devilContractActive:
        contractBuy = [ "…本当にそれが必要？\n    まあ、いいけど♪", "急いでるのに、買い物してるの？\n    …余裕あるのね♪", "…なんか、見えない何かがいる気がする\n    気にしないで♪", ]
        return contractBuy[st.rand.Next(len(contractBuy))]
    normal = [ "さすが、目の付け所がいいわね♪", "これを選ぶなんて…センスあるじゃない♪", "ありがとう♪ また来てね", ]
    return normal[st.rand.Next(len(normal))]

def GetBellFarewell():
    # 悪魔契約中
    if st.devilContractActive:
        if st.devilContractType == 1:
            contract1 = [ "…なんか、雰囲気変わったわね♪\n    気のせいかしら…", "…その指、何か巻いてる？\n    …別に、気にしてないけど♪", "最近ツいてるじゃない♪\n    …でも、なんか怖いわね", "10回…ちゃんと数えてる？\n    …まあ、いいけど♪", ]
            return contract1[st.rand.Next(len(contract1))]
        if st.devilContractType == 2:
            contract2 = [ "…急いでるの？\n    顔色悪いわよ♪", "時間、大丈夫？\n    …なんとなく聞いてみただけ♪", "…何かに追われてる感じがするわ\n    …私だけ？♪", "…ねえ、間に合うの？\n    …余計なこと言ったわね。行って♪", ]
            return contract2[st.rand.Next(len(contract2))]
        if st.devilContractType == 3:
            contract3 = [ "…あなた、前に会ったことある？\n    なんか、初めて会った気がしないのよね♪", "なんか…覚えてないことがあるって怖いわよね\n    …ふふ♪", "…私のこと、ちゃんと覚えてる？\n    …覚えててね。お願い♪", ]
            return contract3[st.rand.Next(len(contract3))]
    # 中毒度高い
    if st.addictionLevel >= 70:
        addicted = [ "…また来てね♪\n    …来るって、わかってるけど", "ゆっくり休んでね♪\n    …嘘。来るって信じてるわ", "…次来た時、顔色よくなってたら嬉しいわ♪", ]
        return addicted[st.rand.Next(len(addicted))]
    # 借金高い
    if st.debt >= 10000:
        bigDebt = [ "…気をつけてね♪\n    …本当に", "また来てね♪\n    …でも、無理しないで", "…待ってるから♪\n    借金、なんとかなるといいわね", ]
        return bigDebt[st.rand.Next(len(bigDebt))]
    # 777達成後
    if st.total777Count >= 3 and st.rand.Next(3) == 0:
        after777 = [ "またやっちゃうの？♪\n    …777、もう一回見たいわ", "また来てね♪\n    …次も揃えてみせて？", ]
        return after777[st.rand.Next(len(after777))]
    # 常連（何も買わずに帰る回数）
    st.shopCloseWithoutBuyCount += 1
    if st.shopCloseWithoutBuyCount == 5:
        return "ねえ、もしかして私に会いに来てる？\n    …正解♪"
    if st.shopCloseWithoutBuyCount == 10:
        return "10回目ね♪\n    …数えてたの。内緒よ？"
    if st.shopCloseWithoutBuyCount == 20:
        return "20回目♪\n    …もう、ここが居場所になってるんじゃないの？"
    if st.shopCloseWithoutBuyCount == 30:
        return "30回よ♪\n    …あなた、私なしじゃ無理でしょ。わかってる"
    if st.shopCloseWithoutBuyCount >= 3:
        repeat = [ "…また来てね♪ 待ってるから", "いつでも来てね♪\n    …本当に、待ってるから", "またいつでも♪\n    …来るの、わかってるけど言いたかった", "…行かないで\n    …なんでもない♪ またね", "また来てね♪\n    …来なかったら、探しに行くわよ？", "…帰るの？\n    …そう。また来てね♪ 絶対に", ]
        return repeat[st.rand.Next(len(repeat))]
    normal = [ "またいつでも来てね♪", "待ってるわよ♪", "いつでもどうぞ♪", "またね♪\n    …来てくれると思ってる", "気をつけてね♪", ]
    return normal[st.rand.Next(len(normal))]
# ========== ショップメニュー ==========

def ShopMenu():
    st.shopVisitCount += 1
    boughtSomething = False
    if st.dreamCasinoUnlocked and dream.CanEnterDream():
        if not st.mushroomManMet:
            dream.MushroomManFirstMeet()
        else:
            dream.MushroomManWaiting()
    # ベルの挨拶
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Magenta
    Console.WriteLine("\n\n\n")
    Console.WriteLine("    ベル「" + GetBellGreeting() + "」")
    Console.ResetColor()
    Thread.Sleep(2500)
    while True:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine("╔═══════════════════════════════════╗")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("║          ♦ ショップ ♦             ║")
        Console.WriteLine("║                                   ║")
        Console.WriteLine("╚═══════════════════════════════════╝")
        Console.ResetColor()
        Console.WriteLine(f"\n所持金: {st.money}G\n")
        Console.WriteLine("【通常アイテム】\n")
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"  [1] お守り (200G) - 当たりやすくなる（永続）")
        Console.WriteLine(f"      所持数: {st.itemInventory['お守り']}個")
        if st.itemInventory["お守り"] > 0:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine("      ※購入済み")
            Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"\n  [2] 幸運のコイン (500G) - 次回1回だけ大幅UP（消費）")
        Console.WriteLine(f"      所持数: {st.itemInventory['幸運のコイン']}個")
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine(f"      累計購入数: {st.totalLuckyCoinsPurchased}個")
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"\n  [3] 返済猶予券/リハビリ券 (1000G)")
        Console.WriteLine(f"      借金期限+10回 / 中毒度-50")
        Console.WriteLine(f"      所持数: {st.itemInventory['返済猶予券']}個")
        Console.ResetColor()
        Console.WriteLine("\n【呪いのアイテム】\n")
        # 悪魔のコイン
        if st.totalLoses >= 20:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  [4] 悪魔のコイン (800G)")
            Console.WriteLine(f"      効果: 次回100%勝利 / 呪い: その後5回100%敗北")
            Console.WriteLine(f"      所持数: {(('1個' if st.hasDevilCoin else '0個'))}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  [4] ??? (条件: 累計負け20回以上)")
            Console.WriteLine(f"      残り: あと{20 - st.totalLoses}回負けると解放")
        # 血塗られたお守り
        Console.WriteLine()
        if st.hasEverBorrowedMoney and st.totalSpins >= 30:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  [5] 血塗られたお守り (1000G)")
            Console.WriteLine(f"      効果: 当たり確率2倍 / 呪い: 3敗でBAD END")
            Console.WriteLine(f"      所持数: {(('1個' if st.hasBloodAmulet else '0個'))}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  [5] ??? (条件: 借金経験あり かつ 総回転数30回以上)")
            if not st.hasEverBorrowedMoney:
                Console.WriteLine(f"      借金をまだ経験していない...")
            else:
                Console.WriteLine(f"      残り: あと{Math.Max(0, 30 - st.totalSpins)}回転で解放")
        # 死神の指輪
        Console.WriteLine()
        if st.vip777Count >= 1:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  [6] 死神の指輪 (3000G)")
            Console.WriteLine(f"      効果: 勝ち×10倍 / 呪い: 負け-1000G")
            Console.WriteLine(f"      所持数: {(('1個' if st.hasDeathRing else '0個'))}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  [6] ??? (条件: VIPルームで777を1回揃える)")
            if not st.vipRoomUnlocked:
                Console.WriteLine(f"      VIPルームがまだ解放されていない...")
            else:
                Console.WriteLine(f"      VIPルームで777を狙え...")
        # 時を刻む懐中時計
        Console.WriteLine()
        if st.godModeActivateCount >= 2:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  [7] 時を刻む懐中時計 (1500G)")
            Console.WriteLine(f"      効果: GOD MODE+5回 / 呪い: 1回転3秒制限")
            Console.WriteLine(f"      所持数: {(('1個' if st.hasTimeClock else '0個'))}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  [7] ??? (条件: GOD MODEを2回以上発動)")
            Console.WriteLine(f"      GOD MODE発動回数: {st.godModeActivateCount}/2回")
        # 禁断の水晶玉
        Console.WriteLine()
        if st.undergroundVisits >= 3:
            Console.ForegroundColor = ConsoleColor.Red
            Console.WriteLine(f"  [8] 🔮 禁断の水晶玉 (2000G)")
            Console.WriteLine(f"      効果: 次回出目予知 / 50%没収")
            Console.WriteLine(f"      所持数: {(('1個' if st.hasOracleBall else '0個'))}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  [8] ??? (条件: 地下カジノに3回以上訪問)")
            if not st.undergroundUnlocked:
                Console.WriteLine(f"      地下カジノがまだ解放されていない...")
            else:
                Console.WriteLine(f"      地下訪問回数: {st.undergroundVisits}/3回")
        Console.ResetColor()
        Console.ResetColor()
        # 換金したお金（無垢な宝石所持中）
        if st.hasInnocentGem and not st.hasExchangedMoney:
            Console.ForegroundColor = ConsoleColor.DarkYellow
            Console.WriteLine("\n  ─────────────────────────────────")
            Console.WriteLine("  換金したお金　　　　　　　5000G")
            Console.WriteLine("  ─────────────────────────────────")
            Console.ResetColor()
        # 隠しページ（チャプター1クリア後）
        if st.chapter1Seen and not st.vanityKeyPurchased:
            Console.ForegroundColor = ConsoleColor.DarkMagenta
            Console.WriteLine("\n  [H] .........")
            Console.ResetColor()
        Console.WriteLine("\n  [0] 戻る")
        Console.Write("\n選択 > ")
        key = Console.ReadKey(True)
        if key.KeyChar == "0":
            if not boughtSomething:
                Console.ForegroundColor = ConsoleColor.Magenta
                Console.WriteLine(f"\n    ベル「{GetBellFarewell()}」")
                Console.ResetColor()
                Thread.Sleep(2000)
                # 優柔不断ミッション達成チェック
                if st.shopCloseWithoutBuyCount == 5:
                    Console.clear()
                    Console.ForegroundColor = ConsoleColor.DarkMagenta
                    Console.WriteLine("\n\n\n")
                    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
                    Console.WriteLine("         隠しミッション発見！")
                    Console.WriteLine("         「優柔不断」")
                    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
                    Console.WriteLine("\n    迷うことも、ひとつの選択だ")
                    Console.ResetColor()
                    Thread.Sleep(3000)
            break
        # 換金したお金
        if (key.KeyChar == "e" or key.KeyChar == "E") and st.hasInnocentGem and not st.hasExchangedMoney:
            BuyExchangedMoney()
            break
        # 隠しページ
        if (key.KeyChar == "h" or key.KeyChar == "H") and st.chapter1Seen and not st.vanityKeyPurchased:
            ShopHiddenPage()
            continue
        _sw3 = key.KeyChar
        if _sw3 == "1":
            if st.itemInventory["お守り"] > 0:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\nお守りは既に購入済みです")
                Console.ResetColor()
                Thread.Sleep(1500)
            elif st.money >= 200:
                st.money -= 200
                st.itemInventory["お守り"] += 1
                boughtSomething = True
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("\n\nお守りを購入しました！")
                Console.ForegroundColor = ConsoleColor.Magenta
                Console.WriteLine(f"\n    ベル「{GetBellPurchaseComment('お守り')}」")
                Console.ResetColor()
                Thread.Sleep(2000)
            else:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n所持金が足りません...")
                Console.ResetColor()
                Thread.Sleep(1500)
        elif _sw3 == "2":
            if st.money >= 500:
                st.money -= 500
                st.itemInventory["幸運のコイン"] += 1
                st.totalLuckyCoinsPurchased += 1
                st.luckyCoinsTotal += 1
                if st.luckyCoinsTotal >= 10 and not st.dreamCasinoUnlocked:
                    st.dreamCasinoUnlocked = True
                boughtSomething = True
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("\n\n幸運のコインを購入しました！")
                Console.WriteLine(f"累計購入数: {st.totalLuckyCoinsPurchased}個")
                Console.ForegroundColor = ConsoleColor.Magenta
                Console.WriteLine(f"\n    ベル「{GetBellPurchaseComment('幸運のコイン')}」")
                Console.ResetColor()
                Thread.Sleep(2000)
            else:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n所持金が足りません...")
                Console.ResetColor()
                Thread.Sleep(1500)
        elif _sw3 == "3":
            if st.money >= 1000:
                st.money -= 1000
                st.itemInventory["返済猶予券"] += 1
                boughtSomething = True
                Console.ForegroundColor = ConsoleColor.Green
                Console.WriteLine("\n\n返済猶予券を購入しました！")
                Console.ForegroundColor = ConsoleColor.Magenta
                Console.WriteLine(f"\n    ベル「{GetBellPurchaseComment('返済猶予券')}」")
                Console.ResetColor()
                Thread.Sleep(2000)
            else:
                Console.ForegroundColor = ConsoleColor.Red
                Console.WriteLine("\n\n所持金が足りません...")
                Console.ResetColor()
                Thread.Sleep(1500)
        elif _sw3 == "4":
            if PurchaseCursedItemWithBell("悪魔のコイン", 800, "hasDevilCoin"):
                boughtSomething = True
        elif _sw3 == "5":
            if PurchaseCursedItemWithBell("血塗られたお守り", 1000, "hasBloodAmulet"):
                boughtSomething = True
        elif _sw3 == "6":
            if PurchaseCursedItemWithBell("死神の指輪", 3000, "hasDeathRing"):
                boughtSomething = True
        elif _sw3 == "7":
            if PurchaseCursedItemWithBell("時を刻む懐中時計", 1500, "hasTimeClock"):
                boughtSomething = True
        elif _sw3 == "8":
            if PurchaseCursedItemWithBell("禁断の水晶玉", 2000, "hasOracleBall"):
                boughtSomething = True
        else:
            Console.WriteLine("\n\n正しい番号を選択してください")
            Thread.Sleep(1000)

def PurchaseCursedItemWithBell(itemName, price, hasItemName):
    if st.py_getflag(hasItemName):
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine(f"\n\n{itemName}は既に所持しています")
        Console.ResetColor()
        Thread.Sleep(1500)
        return False
    if st.money < price:
        Console.ForegroundColor = ConsoleColor.Red
        Console.WriteLine("\n\n所持金が足りません...")
        Console.ResetColor()
        Thread.Sleep(1500)
        return False
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("\n\n⚠⚠⚠ 警告 ⚠⚠⚠\n")
    Console.WriteLine(f"{itemName}を購入しますか？\n")
    Console.WriteLine("これは呪われたアイテムです")
    Console.WriteLine("強力な効果と引き換えに恐ろしい代償を払います")
    Console.WriteLine("\n本当に購入しますか？ [Y/N]")
    Console.ResetColor()
    confirm = Console.ReadKey(True)
    if confirm.Key == ConsoleKey.Y:
        st.money -= price
        st.py_setflag(hasItemName, True)
        st.cursedItemCount += 1
        Console.clear()
        for i in range(0, 5):
            Console.BackgroundColor =(ConsoleColor.DarkRed if i % 2 == 0 else ConsoleColor.Black)
            Console.ForegroundColor =(ConsoleColor.Black if i % 2 == 0 else ConsoleColor.Red)
            Console.clear()
            Console.WriteLine("\n\n\n")
            Console.WriteLine(f"    {itemName}を手に入れた...")
            Console.WriteLine("\n    呪いのオーラを感じる...")
            Thread.Sleep(300)
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.Green
        Console.WriteLine(f"\n\n{itemName}を購入しました！")
        Console.WriteLine("\n※装備管理[E]から装備できます")
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n    ベル「{GetBellPurchaseComment(itemName)}」")
        Console.ResetColor()
        Thread.Sleep(2500)
        if not (f"{itemName}入手" in st.unlockedEvents):
            st.unlockedEvents.append(f"{itemName}入手")
        return True
    return False

def ShopHiddenPage():
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ページをめくると", 45)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    そこだけ　少し空気が違った", 45)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n    ╔═══════════════════════════════╗")
    Console.WriteLine("    ║        ？？？ページ           ║")
    Console.WriteLine("    ╚═══════════════════════════════╝")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("\n\n    ┌─────────────────────────┐")
    Console.WriteLine("    │  虚栄のカギ              │")
    Console.WriteLine("    │  価格：3000G             │")
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("    │  夢も希望もない場所への  │")
    Console.WriteLine("    │  一歩。どこか冷たい鍵。  │")
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("    └─────────────────────────┘")
    Console.WriteLine("\n    [1] 購入する（3000G）")
    Console.WriteLine("    [0] 戻る")
    Console.Write("\n    > ")
    Console.ResetColor()
    key = Console.ReadKey(True)
    if key.KeyChar != "1":
        return
    if st.money < 3000:
        Console.clear()
        Console.ForegroundColor = ConsoleColor.Red
        ui_mod.TypewriterEffect("\n\n    所持金が足りない...", 40)
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    st.money -= 3000
    st.vanityKeyPurchased = True
    st.abandonedCasinoUnlocked = True
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    会計をしようとすると", 40)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n    ベルがそのカギをじっと見た", 40)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...こんなの　店に出した覚えないけど」", 42)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「どこから出てきたんだろ　これ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    少し間があった", 40)
    Thread.Sleep(1800)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...ねえ」", 45)
    Thread.Sleep(1500)
    ui_mod.TypewriterEffect("\n\n    ベル「そのカギ　どこに繋がってるか　確かめてみたくない？」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「一緒に行ってみようよ♪」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect(f"\n\n    {st.playerName}「...どこ行くんだよ」", 42)
    Thread.Sleep(1800)
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「わかんない♪　でもなんか　知ってる気がするんだよね」", 40)
    Thread.Sleep(2500)
    ui_mod.TypewriterEffect("\n\n    ベル「...不思議でしょ」", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkMagenta
    Console.WriteLine("\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         虚栄のカギ　入手")
    Console.WriteLine("         廃娯楽施設が解放された")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(3500)
    if not ("廃娯楽施設解放" in st.unlockedEvents):
        st.unlockedEvents.append("廃娯楽施設解放")

def BuyExchangedMoney():
    Console.clear()
    Thread.Sleep(500)
    if st.money < 5000:
        Console.ForegroundColor = ConsoleColor.Red
        ui_mod.TypewriterEffect("\n\n    所持金が足りない...", 40)
        Console.ResetColor()
        Thread.Sleep(1500)
        return
    Console.ForegroundColor = ConsoleColor.DarkYellow
    Console.WriteLine("\n\n    ┌─────────────────────────┐")
    Console.WriteLine("    │  換金したお金            │")
    Console.WriteLine("    │  価格：5000G             │")
    Console.ForegroundColor = ConsoleColor.DarkGray
    Console.WriteLine("    │  見たことない額のお金。  │")
    Console.ForegroundColor = ConsoleColor.DarkYellow
    Console.WriteLine("    └─────────────────────────┘")
    Console.ResetColor()
    Console.WriteLine("\n    [1] 購入する")
    Console.WriteLine("    [0] やめる")
    Console.Write("\n    > ")
    key = Console.ReadKey(True)
    if key.KeyChar != "1":
        return
    st.money -= 5000
    st.hasExchangedMoney = True
    Console.clear()
    Thread.Sleep(500)
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    お金を受け取った", 42)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    見たことない額だった", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.White
    ui_mod.TypewriterEffect("\n\n    これでカジノは　俺のものだ", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    そう思った瞬間", 42)
    Thread.Sleep(1800)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    ベルが　こちらを見ていた", 42)
    Thread.Sleep(2000)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    ui_mod.TypewriterEffect("\n\n    ベル「...そっか」", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    ベル「そういう人だったんだ」", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    ベルが　カウンターの奥に引っ込んだ", 40)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n    それ以上　何も言わなかった", 42)
    Thread.Sleep(2500)
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.WriteLine("\n\n\n    ━━━━━━━━━━━━━━━━━━━━")
    Console.WriteLine("         BAD END")
    Console.WriteLine("         「そういう人だったんだ」")
    Console.WriteLine("    ━━━━━━━━━━━━━━━━━━━━")
    Console.ResetColor()
    Thread.Sleep(4000)
    if not ("バッドエンド:カジノを乗っ取る" in st.unlockedEvents):
        st.unlockedEvents.append("バッドエンド:カジノを乗っ取る")
    Console.clear()
    Console.ForegroundColor = ConsoleColor.DarkGray
    ui_mod.TypewriterEffect("\n\n    気づくと　自分が黒服を着ていた", 40)
    Thread.Sleep(2000)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    カジノのオーナーになった", 42)
    Thread.Sleep(2000)
    ui_mod.TypewriterEffect("\n\n    でも　何も変わらなかった", 42)
    Thread.Sleep(2200)
    Console.clear()
    ui_mod.TypewriterEffect("\n\n    スロットの音だけが　鳴り続けていた", 40)
    Thread.Sleep(2500)
    Console.clear()
    Console.ResetColor()
