# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot — ランキング・コレクション (機械分割: refactor/transform.py 生成)"""
from cs_runtime import *
import cs_runtime
from . import state as st


def ShowRankings():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Yellow
    Console.WriteLine("╔═══════════════════════════════════╗")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("║         ★ ランキング ★          ║")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("╚═══════════════════════════════════╝")
    Console.ResetColor()
    Console.WriteLine("\n【歴代TOP10】\n")
    topRanks = py_top10_rankings(st.rankings)
    if len(topRanks) == 0:
        Console.WriteLine("  まだ記録がありません")
    else:
        for i in range(0, len(topRanks)):
            rank = topRanks[i]
            Console.ForegroundColor =(ConsoleColor.Yellow if i < 3 else ConsoleColor.White)
            Console.WriteLine(f"  {i + 1}位: {(rank.Name).ljust(int(12))} {rank.Money}G ({rank.Spins}回転) {rank.Date:yyyy/MM/dd}")
            Console.ResetColor()
    Console.WriteLine("\n\n【あなたの記録】")
    Console.WriteLine(f"  最高所持金: {st.maxMoney}G")
    Console.WriteLine(f"  最大連勝: {st.maxConsecutiveWins}回")
    Console.WriteLine(f"  777揃い: {st.total777Count}回")
    Console.WriteLine("\n\n何かキーを押して戻る...")
    Console.ReadKey(True)
# ========== コレクション ==========

def ShowCollection():
    Console.clear()
    Console.ForegroundColor = ConsoleColor.Cyan
    Console.WriteLine("╔═══════════════════════════════════╗")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("║       ♦ コレクション ♦          ║")
    Console.WriteLine("║                                   ║")
    Console.WriteLine("╚═══════════════════════════════════╝")
    Console.ResetColor()
    Console.WriteLine("\n【解放済み絵柄】")
    Console.WriteLine(f"  {len(st.unlockedSymbols)}/8 種類\n")
    allSymbols = [ "スライム", "ゴーレム", "777", "スマイル", "スター", "サークル", "ハッシュ", "ドル" ]
    for sym in allSymbols:
        if (sym in st.unlockedSymbols):
            Console.ForegroundColor = ConsoleColor.Green
            Console.WriteLine(f"  ✓ {sym}")
        else:
            Console.ForegroundColor = ConsoleColor.DarkGray
            Console.WriteLine(f"  ? ???")
        Console.ResetColor()
    Console.WriteLine("\n\n【イベントCGギャラリー】")
    Console.WriteLine(f"  {len(st.unlockedEvents)} 種類解放\n")
    for evt in st.unlockedEvents:
        Console.ForegroundColor = ConsoleColor.Yellow
        Console.WriteLine(f"  ★ {evt}")
        Console.ResetColor()
    if len(st.unlockedEvents) == 0:
        Console.ForegroundColor = ConsoleColor.DarkGray
        Console.WriteLine("  まだイベントがありません")
        Console.ResetColor()
    Console.WriteLine("\n\n何かキーを押して戻る...")
    Console.ReadKey(True)

def UnlockSymbol():
    allSymbols = [ "スライム", "ゴーレム", "777", "スマイル", "スター", "サークル", "ハッシュ", "ドル" ]
    locked = py_locked_symbols(allSymbols, st.unlockedSymbols)
    if len(locked) > 0 and st.rand.Next(100) < 30:
        newSymbol = locked[st.rand.Next(len(locked))]
        st.unlockedSymbols.append(newSymbol)
        Console.ForegroundColor = ConsoleColor.Magenta
        Console.WriteLine(f"\n\n  ✨ 新しい絵柄を解放！「{newSymbol}」")
        Console.ResetColor()
        Thread.Sleep(2000)
