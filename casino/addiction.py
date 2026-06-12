# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 中毒システム (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st

# ========== 中毒システム強化 ==========

def ShowAddictionMessage():
    if st.addictionLevel >= 21 and st.rand.Next(100) < 30:
        Console.ForegroundColor = ConsoleColor.DarkRed
        Console.WriteLine(f"\n{st.addictionMessages[st.rand.Next(len(st.addictionMessages))]}")
        Console.ResetColor()
        Thread.Sleep(1500)

def AddictionHallucinationEffect():
    if st.addictionLevel >= 61 and st.rand.Next(100) < 20:
        Console.clear()
        Console.CursorVisible = False
        # 中毒度に応じて演出を変化
        if st.addictionLevel >= 90:
            AddictionWaveEffect_Chaos()
        elif st.addictionLevel >= 75:
            AddictionWaveEffect_Break()
        else:
            AddictionWaveEffect_Soft()
        Console.BackgroundColor = ConsoleColor.Black
        Console.ForegroundColor = ConsoleColor.White
        Console.clear()
        Thread.Sleep(300)
        if not ("中毒幻覚" in st.unlockedEvents):
            st.unlockedEvents.append("中毒幻覚")
# ========== 中毒波形演出（61-74%）穏やかな揺れ ==========

def AddictionWaveEffect_Soft():
    width = 60
    height = 12
    speed = 0.18
    frames = 28
    for frame in range(0, frames):
        Console.clear()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n")
        # sinグラフで揺れる波
        for row in range(0, height):
            # 各行のy座標を正規化 (-1.0 〜 1.0)
            y = 1.0 - 2.0 * row / (height - 1)
            # 時間と行に応じてsinカーブ
            for col in range(0, width):
                x = float(col) / width * Math.PI * 4
                wave = Math.Sin(x - frame * speed) * Math.Cos(x * 0.3 + frame * 0.1)
                # 波の山にいるか判定（閾値内なら描画）
                threshold = 0.12 + 0.04 * Math.Sin(frame * 0.2)
                if Math.Abs(wave - y) < threshold:
                    brightness = 1.0 - Math.Abs(wave - y) / threshold
                    Console.ForegroundColor =(ConsoleColor.White if brightness > 0.6 else ConsoleColor.DarkGray)
                    Console.Write("·")
                else:
                    Console.Write(" ")
            Console.WriteLine()
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("\n    ...何かが見える...")
        Console.ResetColor()
        Thread.Sleep(55)
# ========== 中毒波形演出（75-89%）崩れ始める ==========

def AddictionWaveEffect_Break():
    width = 64
    height = 14
    speed = 0.28
    frames = 35
    for frame in range(0, frames):
        Console.clear()
        Console.WriteLine("\n")
        chaos = float(frame) / frames
        # 後半ほど乱れる
        for row in range(0, height):
            y = 1.0 - 2.0 * row / (height - 1)
            for col in range(0, width):
                x = float(col) / width * Math.PI * 6
                # sin + cos の合成波（リサジュー風）
                wave = Math.Sin(x - frame * speed) + 0.4 * Math.Cos(x * 1.7 + frame * 0.15) + 0.2 * Math.Sin(frame * 0.3) * chaos
                wave /= 1.6
                # 正規化
                # 後半はノイズを混入
                if chaos > 0.5 and st.rand.NextDouble() < chaos * 0.08:
                    wave += (st.rand.NextDouble() - 0.5) * 0.8
                threshold = 0.14
                dist = Math.Abs(wave - y)
                if dist < threshold:
                    t = dist / threshold
                    color = None
                    if t < 0.25:
                        color = ConsoleColor.Yellow
                    elif t < 0.6:
                        color = ConsoleColor.DarkYellow
                    else:
                        color = ConsoleColor.DarkGray
                    Console.ForegroundColor = color
                    # 後半は文字が壊れる
                    if chaos > 0.6 and st.rand.NextDouble() < chaos * 0.3:
                        Console.Write(chr(st.rand.Next(0x21, 0x7E)))
                    else:
                        Console.Write("█")
                else:
                    Console.Write(" ")
            Console.WriteLine()
        msgColor = (ConsoleColor.Yellow if chaos < 0.5 else ConsoleColor.Red)
        Console.ForegroundColor = msgColor
        msgs = [ "    ...止められない...", "    ...もっと...", "    ...あと少しで...", "    ...どこかへ消えたい..." ]
        Console.WriteLine(msgs[frame % len(msgs)])
        Console.ResetColor()
        Thread.Sleep(45)
# ========== 中毒波形演出（90%+）完全崩壊 ==========

def AddictionWaveEffect_Chaos():
    width = 70
    height = 16
    frames = 45
    for frame in range(0, frames):
        Console.clear()
        Console.WriteLine()
        t = float(frame) / frames
        amp = 1.0 + t * 1.5
        # 振幅が時間とともに増大
        for row in range(0, height):
            y = 1.0 - 2.0 * row / (height - 1)
            for col in range(0, width):
                x = float(col) / width * Math.PI * 8
                # tanを含む複合波（発散する感じ）
                tanPart = Math.Tan(x * 0.08 + frame * 0.05)
                tanPart = Math.Max(-1.5, Math.Min(1.5, tanPart))
                # クランプ
                wave = (Math.Sin(x - frame * 0.35) * amp + 0.5 * Math.Cos(x * 2.1 - frame * 0.2) + 0.2 * tanPart) / (amp + 0.7)
                # 強いノイズ
                if st.rand.NextDouble() < t * 0.15:
                    wave += (st.rand.NextDouble() - 0.5) * amp
                threshold = 0.16 + t * 0.1
                dist = Math.Abs(wave - y)
                if dist < threshold:
                    brightness = 1.0 - dist / threshold
                    # 色が暴れる
                    colors = [ ConsoleColor.Red, ConsoleColor.DarkRed, ConsoleColor.Magenta, ConsoleColor.DarkMagenta, ConsoleColor.Yellow, ConsoleColor.White ]
                    colorIdx = int(brightness * 3) + ((0 if frame % 2 == 0 else 2))
                    Console.ForegroundColor = colors[Math.Min(colorIdx, len(colors) - 1)]
                    # 文字が崩れる
                    glitchChance = t * 0.6
                    if st.rand.NextDouble() < glitchChance:
                        glitchChars = [ "▓", "▒", "░", "╬", "╪", "╫", "║", "═", "#", "%" ]
                        Console.Write(glitchChars[st.rand.Next(len(glitchChars))])
                    else:
                        Console.Write(("█" if brightness > 0.5 else "▓"))
                elif st.rand.NextDouble() < t * 0.04:
                    # 背景にもノイズ粒子
                    Console.ForegroundColor = ConsoleColor.DarkRed
                    Console.Write("·")
                else:
                    Console.Write(" ")
            Console.WriteLine()
        # メッセージも崩れる
        Console.ForegroundColor =(ConsoleColor.Red if frame % 3 == 0 else ConsoleColor.DarkRed)
        msgs = [ "    声が...聞こえる...", "    誰かが...呼んでいる...", "    これは...夢か...？", "    画面が...歪んで見える...", "    もうやめろ...", "    タスケテ..." ]
        msg = msgs[frame % len(msgs)]
        # 後半はメッセージもノイズ化
        if t > 0.7:
            corrupted = list(msg)
            for i in range(0, len(corrupted)):
                if st.rand.NextDouble() < t * 0.4 and corrupted[i] != " ":
                    corrupted[i] = chr(st.rand.Next(0x21, 0x7E))
            Console.WriteLine("".join(corrupted))
        else:
            Console.WriteLine(msg)
        Console.ResetColor()
        Thread.Sleep(35)
