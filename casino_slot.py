# -*- coding: utf-8 -*-
"""FEWJSCasinoSlot エントリポイント (本体は casino/ パッケージ)"""
from cs_runtime import Console
from casino.state import rand
from casino.app import Main


if __name__ == "__main__":
    try:
        Main()
    except (KeyboardInterrupt, EOFError):
        pass
    except SystemExit:
        pass
    finally:
        try:
            Console.ResetColor()
            Console.CursorVisible = True
            print()
        except Exception:
            pass
