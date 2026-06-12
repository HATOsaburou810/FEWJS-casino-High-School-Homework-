# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — 共通UI・演出 (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st

# ========== FormatTimeSpan ヘルパー関数（メソッド末尾に追加） ==========

def FormatTimeSpan(ts):
    if ts.TotalMinutes < 1:
        return f"{ts.Seconds}秒"
    elif ts.TotalHours < 1:
        return f"{ts.Minutes}分{ts.Seconds}秒"
    else:
        return f"{ts.Hours}時間{ts.Minutes}分{ts.Seconds}秒"

def GetAddictionBar(level):
    filled = level / 5
    color = (ConsoleColor.Green if level < 40 else (ConsoleColor.Yellow if level < 70 else ConsoleColor.Red))
    Console.ForegroundColor = color
    bar = f"[{(('█' * int(filled) + '█') + '░' * max(0, int(20) - len(('█' * int(filled) + '█'))))}] {level}%"
    Console.ResetColor()
    return bar
# ========== タイプライター効果 ==========

def TypewriterEffect(text, delayMs=50):
    for c in text:
        Console.Write(c)
        Thread.Sleep(delayMs)
# ========== 大きな数字のASCIIアート ==========

def GetBigNumber(num):
    bigDigits = { 0: [ " ██████╗ ", "██╔═████╗", "██║██╔██║", "████╔╝██║", "╚██████╔╝", " ╚═════╝ " ], 1: [ " ██╗", "███║", "╚██║", " ██║", " ██║", " ╚═╝" ], 2: [ "██████╗ ", "╚════██╗", " █████╔╝", "██╔═══╝ ", "███████╗", "╚══════╝" ], 3: [ "██████╗ ", "╚════██╗", " █████╔╝", " ╚═══██╗", "██████╔╝", "╚═════╝ " ], 4: [ "██╗  ██╗", "██║  ██║", "███████║", "╚════██║", "     ██║", "     ╚═╝" ], 5: [ "███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝" ], 6: [ " ██████╗ ", "██╔════╝ ", "███████╗ ", "██╔═══██╗", "╚██████╔╝", " ╚═════╝ " ], 7: [ "███████╗", "╚════██║", "    ██╔╝", "   ██╔╝ ", "   ██║  ", "   ╚═╝  " ], 8: [ " ██████╗ ", "██╔═══██╗", "╚█████╔╝", "██╔═══██╗", "╚██████╔╝", " ╚═════╝ " ], 9: [ " ██████╗ ", "██╔═══██╗", "╚██████╔╝", " ╚═══██║ ", " █████╔╝ ", " ╚════╝  " ], 10: [ " ██╗ ██████╗ ", "███║██╔═████╗", "╚██║██║██╔██║", " ██║████╔╝██║", " ██║╚██████╔╝", " ╚═╝ ╚═════╝ " ] }
    return (bigDigits[num] if (num in bigDigits) else bigDigits[0])

def TypeText(text, delay=40):
    for c in text:
        Console.Write(c)
        Thread.Sleep(delay)
# ========== 描画関連 ==========

def DrawTitle():
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("╔═══════════════════════════════════╗")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("║      FEWJS  CASINO  SLOT!!!        ║")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("╚═══════════════════════════════════╝")
    Console.ResetColor()

def DrawReels(reels):
    Console.ForegroundColor = ConsoleColor.White
    Console.WriteLine("    ┌───────────┬───────────┬───────────┐")
    for row in range(0, 5):
        Console.Write("    │ ")
        for col in range(0, 3):
            Console.Write(st.symbols[reels[col]][row])
            Console.Write(" │ ")
        Console.WriteLine()
    Console.WriteLine("    └───────────┴───────────┴───────────┘")
    Console.ResetColor()

# ========== FlashBlock ヘルパー ==========

def _apply_color(color):
    """Apply a color spec: a ConsoleColor string or (bg, fg) tuple."""
    if isinstance(color, tuple):
        Console.BackgroundColor = color[0]
        Console.ForegroundColor = color[1]
    else:
        Console.ForegroundColor = color

def FlashBlock(lines, loops, colors, final_color, show_ms, gap_ms, clear_width=50):
    """Flash a colored block N times, then draw it solid.

    lines:       list of strings to write each frame.
    loops:       number of flash iterations.
    colors:      list of 2 color specs indexed by i%2 each iteration.
                 each spec is a ConsoleColor string or a (bg, fg) tuple.
    final_color: color spec for the final solid draw.
    show_ms:     milliseconds to show the block per iteration.
    gap_ms:      milliseconds to show blank space per iteration.
    clear_width: width of the blank lines used to erase the block.
    """
    n = len(lines)
    for i in range(0, loops):
        _apply_color(colors[i % 2])
        for line in lines:
            Console.WriteLine(line)
        Thread.Sleep(show_ms)
        Console.SetCursorPosition(0, Console.CursorTop - n)
        for j in range(0, n):
            Console.WriteLine((" " * clear_width))
        Console.SetCursorPosition(0, Console.CursorTop - n)
        Thread.Sleep(gap_ms)
    _apply_color(final_color)
    for line in lines:
        Console.WriteLine(line)
    Console.ResetColor()

# テキストをグリッチさせて表示する

def GlitchText(text, baseColor, cycles=6, delayMs=40):
    chars = list(text)
    rng = st.rand
    flashColors = [ ConsoleColor.Red, ConsoleColor.Cyan, ConsoleColor.Magenta, ConsoleColor.Yellow, ConsoleColor.White, ConsoleColor.DarkRed ]
    left = Console.CursorLeft
    top = Console.CursorTop
    for c in range(0, cycles):
        Console.SetCursorPosition(left, top)
        # 乱れ具合：最初は激しく、後半は落ち着く
        chaos = 1.0 - float(c) / cycles
        Console.ForegroundColor = flashColors[c % len(flashColors)]
        for i in range(0, len(chars)):
            if chars[i] == " ":
                Console.Write(" ")
                continue
            if rng.NextDouble() < chaos * 0.6:
                Console.Write(st.glitchChars[rng.Next(len(st.glitchChars))])
            else:
                Console.Write(chars[i])
        Thread.Sleep(delayMs)
    # 最後は元のテキストに戻す
    Console.SetCursorPosition(left, top)
    Console.ForegroundColor = baseColor
    Console.Write(text)
    Console.ResetColor()
# 画面全体がバグる演出

def ScreenGlitch(intensity=1):
    # intensity: 1=軽め 2=中 3=ガチバグ
    frames = 4 + intensity * 3
    colors = [ ConsoleColor.Red, ConsoleColor.DarkCyan, ConsoleColor.Magenta, ConsoleColor.DarkRed, ConsoleColor.Yellow ]
    noiseLines = [ "▓▒░█▓╬▒░╪▓█░▒╫╬▓▒░█▓▒░╬╪", "╔═╗║╚╝╬╫╪▲▼◆◇★☆※〓■□●○", "!?#%&@$/\\|+-~▓▒░█▓╬╪╫▲▼", "〓■□●○◆◇▲▼╔═╗║╚╝╬╫╪▓▒░", ]
    savedTop = Math.Min(Console.CursorTop, Console.BufferHeight - 1)
    for f in range(0, frames):
        # 画面の一部にノイズラインを挿入
        noiseRow = st.rand.Next(2, Math.Min(Console.WindowHeight - 2, 20))
        try:
            Console.SetCursorPosition(0, noiseRow)
            Console.ForegroundColor = colors[f % len(colors)]
            Console.Write((noiseLines[st.rand.Next(len(noiseLines))]).ljust(int(Console.WindowWidth - 1)))
        except Exception:
            pass
        Thread.Sleep(35 + intensity * 15)
        # ノイズを消す
        try:
            Console.SetCursorPosition(0, noiseRow)
            Console.Write((" " * (Console.WindowWidth - 1)))
        except Exception:
            pass
    Console.ResetColor()
    try:
        Console.SetCursorPosition(0, savedTop)
    except Exception:
        pass
# 777グリッチ：JACKPOTの文字が乱れてから確定する

def JackpotGlitch():
    Console.WriteLine()
    line1 = "    ╔══════════════════════════════╗"
    line2 = "    ║   ★  7  7  7  ★  JACKPOT  ★  ║"
    line3 = "    ╚══════════════════════════════╝"
    # 枠が崩れる
    Console.ForegroundColor = ConsoleColor.DarkRed
    Console.Write(line1)
    GlitchText(line1, ConsoleColor.DarkRed, 5, 50)
    Console.WriteLine()
    Console.Write(line2)
    GlitchText(line2, ConsoleColor.Yellow, 8, 45)
    Console.WriteLine()
    Console.Write(line3)
    GlitchText(line3, ConsoleColor.DarkRed, 5, 50)
    Console.WriteLine()
    Thread.Sleep(200)
    # 画面ノイズ
    ScreenGlitch(2)
    # 最終的にキレイに表示
    Console.WriteLine()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("    ╔══════════════════════════════╗")
    Console.ForegroundColor = ConsoleColor.Red
    Console.WriteLine("    ║   ★  7  7  7  ★  JACKPOT  ★  ║")
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("    ╚══════════════════════════════╝")
    Console.ResetColor()
    Thread.Sleep(600)
# スピン中グリッチ：リール表示が一瞬バグる

def SpinGlitch():
    if st.addictionLevel < 60 and not st.devilContractActive:
        return
    # 発動確率：中毒度/悪魔契約で変化
    chance = (25 if st.devilContractActive else (st.addictionLevel - 60) / 3)
    if st.rand.Next(100) >= chance:
        return
    ScreenGlitch(1)
    # 一瞬だけ不穏なテキストを表示
    messages = [ "    ERROR: REEL_SYNC_FAILED", "    ████ 存在してはいけない ████", "    SYSTEM: memory corruption detected", "    ▓▒░ 現実が　　歪んで　　いる ░▒▓", "    ??? UNDEFINED BEHAVIOR ???", ]
    savedTop = Console.CursorTop
    try:
        Console.SetCursorPosition(0, Math.Max(0, savedTop - 2))
        Console.ForegroundColor = ConsoleColor.DarkRed
        msg = messages[st.rand.Next(len(messages))]
        GlitchText(msg, ConsoleColor.DarkRed, 4, 40)
        Thread.Sleep(300)
        Console.SetCursorPosition(0, Console.CursorTop)
        Console.Write((" " * (len(msg) + 4)))
        Console.SetCursorPosition(0, savedTop)
    except Exception:
        pass
    Console.ResetColor()
# メニューグリッチ：選択肢の一部が一瞬化ける

def MenuGlitch():
    if st.addictionLevel < 80:
        return
    if st.rand.Next(100) >= 8:
        return
    flickers = [ "    ??? 何かが見えた気がした", "    ▓▓▓ ベル「...逃げないで」 ▓▓▓", "    ERROR 404: 現実が見つかりません", "    ░░░ もうやめろ ░░░", ]
    Thread.Sleep(100)
    savedTop = Console.CursorTop
    try:
        Console.SetCursorPosition(0, Math.Max(0, savedTop - 1))
        Console.ForegroundColor = ConsoleColor.DarkRed
        msg = flickers[st.rand.Next(len(flickers))]
        Console.Write(msg)
        Thread.Sleep(180)
        Console.SetCursorPosition(0, Console.CursorTop)
        Console.Write((" " * (len(msg) + 4)))
        Console.SetCursorPosition(0, savedTop)
    except Exception:
        pass
    Console.ResetColor()
