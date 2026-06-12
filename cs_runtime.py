# -*- coding: utf-8 -*-
"""C# Console API 互換ランタイムシム (FEWJSCasinoSlot Python移植用)
Windows / macOS / Linux 対応
"""
import sys, os, time, math, random, json
import datetime as _dt

IS_WIN = os.name == "nt"

# ---- ANSI有効化 (Windows) ----
if IS_WIN:
    os.system("")
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        h = k32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if k32.GetConsoleMode(h, ctypes.byref(mode)):
            k32.SetConsoleMode(h, mode.value | 0x0004)
    except Exception:
        pass

# ================= ConsoleColor =================
class ConsoleColor:
    Black = "30"; DarkBlue = "34"; DarkGreen = "32"; DarkCyan = "36"
    DarkRed = "31"; DarkMagenta = "35"; DarkYellow = "33"; Gray = "37"
    DarkGray = "90"; Blue = "94"; Green = "92"; Cyan = "96"
    Red = "91"; Magenta = "95"; Yellow = "93"; White = "97"

# ================= ConsoleKey =================
class ConsoleKey:
    Enter = "Enter"; Escape = "Escape"; Spacebar = "Spacebar"
    LeftArrow = "LeftArrow"; RightArrow = "RightArrow"
    UpArrow = "UpArrow"; DownArrow = "DownArrow"
    Backspace = "Backspace"; Tab = "Tab"
    F1="F1";F2="F2";F3="F3";F4="F4";F5="F5";F6="F6";F7="F7";F8="F8";F9="F9";F10="F10";F11="F11";F12="F12"
    D0="D0";D1="D1";D2="D2";D3="D3";D4="D4";D5="D5";D6="D6";D7="D7";D8="D8";D9="D9"
    # A-Z
for _c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    setattr(ConsoleKey, _c, _c)

class ConsoleKeyInfo:
    __slots__ = ("KeyChar", "Key")
    def __init__(self, key_char, key):
        self.KeyChar = key_char
        self.Key = key

# ---- 低レベルキー入力 ----
if IS_WIN:
    import msvcrt
    def _read_key_raw():
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            ch2 = msvcrt.getwch()
            m = {"K": ConsoleKey.LeftArrow, "M": ConsoleKey.RightArrow,
                 "H": ConsoleKey.UpArrow, "P": ConsoleKey.DownArrow,
                 "?": ConsoleKey.F5, "C": ConsoleKey.F9,
                 ";": ConsoleKey.F1, "<": ConsoleKey.F2, "=": ConsoleKey.F3,
                 ">": ConsoleKey.F4, "@": ConsoleKey.F6, "A": ConsoleKey.F7,
                 "B": ConsoleKey.F8, "D": ConsoleKey.F10}
            return ConsoleKeyInfo("\x00", m.get(ch2, ""))
        return _make_keyinfo(ch)
else:
    import termios, tty
    def _read_key_raw():
        fd = sys.stdin.fileno()
        try:
            old = termios.tcgetattr(fd)
        except termios.error:
            # stdin が TTY でない (パイプ/テスト時) → 1文字読み取り
            ch = sys.stdin.read(1)
            if not ch:
                return ConsoleKeyInfo("\r", ConsoleKey.Enter)
            return _make_keyinfo(ch)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                import select
                seq = ""
                while select.select([sys.stdin], [], [], 0.01)[0]:
                    seq += sys.stdin.read(1)
                m = {"[A": ConsoleKey.UpArrow, "[B": ConsoleKey.DownArrow,
                     "[C": ConsoleKey.RightArrow, "[D": ConsoleKey.LeftArrow,
                     "[15~": ConsoleKey.F5, "[20~": ConsoleKey.F9,
                     "OP": ConsoleKey.F1, "OQ": ConsoleKey.F2,
                     "OR": ConsoleKey.F3, "OS": ConsoleKey.F4}
                if seq in m:
                    return ConsoleKeyInfo("\x00", m[seq])
                return ConsoleKeyInfo("\x1b", ConsoleKey.Escape)
            return _make_keyinfo(ch)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def _make_keyinfo(ch):
    if ch in ("\r", "\n"):
        return ConsoleKeyInfo("\r", ConsoleKey.Enter)
    if ch == "\x1b":
        return ConsoleKeyInfo(ch, ConsoleKey.Escape)
    if ch == " ":
        return ConsoleKeyInfo(ch, ConsoleKey.Spacebar)
    if ch in ("\x08", "\x7f"):
        return ConsoleKeyInfo(ch, ConsoleKey.Backspace)
    if ch.isdigit():
        return ConsoleKeyInfo(ch, "D" + ch)
    if ch.isalpha() and ch.isascii():
        return ConsoleKeyInfo(ch, ch.upper())
    return ConsoleKeyInfo(ch, "")

# ================= Console =================
class _Console:
    def __init__(self):
        self._fg = None
        self._cursor_top = 0
        self.CursorVisible = True
        self.OutputEncoding = "utf-8"

    @property
    def CursorVisible(self):
        return self._cv
    @CursorVisible.setter
    def CursorVisible(self, v):
        self._cv = v
        try:
            sys.stdout.write("\033[?25h" if v else "\033[?25l")
            sys.stdout.flush()
        except Exception:
            pass

    @property
    def ForegroundColor(self):
        return self._fg
    @ForegroundColor.setter
    def ForegroundColor(self, code):
        self._fg = code
        sys.stdout.write("\033[%sm" % code)
        sys.stdout.flush()

    @property
    def BackgroundColor(self):
        return getattr(self, "_bg", None)
    @BackgroundColor.setter
    def BackgroundColor(self, code):
        self._bg = code
        try:
            sys.stdout.write("\033[%dm" % (int(code) + 10))
            sys.stdout.flush()
        except (TypeError, ValueError):
            pass

    @property
    def WindowWidth(self):
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80
    @property
    def WindowHeight(self):
        try:
            return os.get_terminal_size().lines
        except OSError:
            return 24
    @property
    def BufferHeight(self):
        return 9001  # Windows コンソールの既定スクロールバッファ高 (近似)
    @property
    def CursorLeft(self):
        return 0  # 追跡不可のため近似

    @property
    def CursorTop(self):
        return self._cursor_top

    def ResetColor(self):
        self._fg = None
        sys.stdout.write("\033[0m")
        sys.stdout.flush()

    def Clear(self):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        self._cursor_top = 0
    clear = Clear  # transpiler が .Clear()→.clear() に一括変換するため

    def Write(self, s=""):
        s = _to_str(s)
        sys.stdout.write(s)
        sys.stdout.flush()
        self._cursor_top += s.count("\n")

    def WriteLine(self, s=""):
        self.Write(_to_str(s) + "\n")

    def ReadKey(self, intercept=False):
        ki = _read_key_raw()
        if not intercept and ki.KeyChar and ki.KeyChar.isprintable():
            self.Write(ki.KeyChar)
        return ki

    def ReadLine(self):
        try:
            return input()
        except EOFError:
            return ""

    def SetCursorPosition(self, x, y):
        sys.stdout.write("\033[%d;%dH" % (int(y) + 1, int(x) + 1))
        sys.stdout.flush()
        self._cursor_top = int(y)

def _to_str(s):
    if isinstance(s, bool):
        return "True" if s else "False"
    return str(s)

Console = _Console()

# ================= Thread =================
class Thread:
    @staticmethod
    def Sleep(ms):
        time.sleep(ms / 1000.0)

# ================= Random =================
class Random:
    def __init__(self):
        self._r = random.Random()
    def Next(self, a=None, b=None):
        if a is None:
            return self._r.randint(0, 2**31 - 1)
        if b is None:
            return self._r.randrange(a)
        return self._r.randrange(a, b)
    def NextDouble(self):
        return self._r.random()

# ================= Math =================
class Math:
    PI = math.pi
    @staticmethod
    def Min(a, b): return min(a, b)
    @staticmethod
    def Max(a, b): return max(a, b)
    @staticmethod
    def Abs(a): return abs(a)
    @staticmethod
    def Clamp(v, lo, hi): return max(lo, min(hi, v))
    @staticmethod
    def Ceiling(v): return math.ceil(v)
    @staticmethod
    def Floor(v): return math.floor(v)
    @staticmethod
    def Sin(v): return math.sin(v)
    @staticmethod
    def Cos(v): return math.cos(v)
    @staticmethod
    def Tan(v): return math.tan(v)
    @staticmethod
    def Pow(a, b): return a ** b

# ================= TimeSpan =================
class TimeSpan:
    def __init__(self, seconds=0.0):
        self._s = float(seconds)
    @property
    def TotalSeconds(self): return self._s
    @property
    def TotalMinutes(self): return self._s / 60.0
    @property
    def TotalHours(self): return self._s / 3600.0
    @property
    def TotalDays(self): return self._s / 86400.0
    @property
    def Seconds(self): return int(self._s) % 60
    @property
    def Minutes(self): return (int(self._s) // 60) % 60
    @property
    def Hours(self): return (int(self._s) // 3600) % 24
    @property
    def Days(self): return int(self._s) // 86400
    @property
    def Milliseconds(self): return int(self._s * 1000) % 1000
    def __lt__(self, o): return self._s < o._s
    def __le__(self, o): return self._s <= o._s
    def __gt__(self, o): return self._s > o._s
    def __ge__(self, o): return self._s >= o._s
    def __eq__(self, o): return isinstance(o, TimeSpan) and self._s == o._s
    @staticmethod
    def FromSeconds(s): return TimeSpan(s)
    @staticmethod
    def FromMinutes(m): return TimeSpan(m * 60)
    @staticmethod
    def FromHours(h): return TimeSpan(h * 3600)
    def __repr__(self):
        return "%02d:%02d:%02d" % (self.Hours, self.Minutes, self.Seconds)

# ================= DateTime =================
_CS2PY_FMT = (("yyyy", "%Y"), ("MM", "%m"), ("dd", "%d"),
              ("HH", "%H"), ("mm", "%M"), ("ss", "%S"))

class DateTime:
    def __init__(self, dt=None):
        self._dt = dt or _dt.datetime.now()
    @classmethod
    def _now(cls):
        return cls(_dt.datetime.now())
    @staticmethod
    def Parse(s):
        try:
            return DateTime(_dt.datetime.fromisoformat(s))
        except Exception:
            return DateTime(_dt.datetime.strptime(s, "%Y-%m-%d"))
    @property
    def Hour(self):
        return self._dt.hour
    def AddMinutes(self, m):
        return DateTime(self._dt + _dt.timedelta(minutes=m))
    def AddHours(self, h):
        return DateTime(self._dt + _dt.timedelta(hours=h))
    def AddDays(self, d):
        return DateTime(self._dt + _dt.timedelta(days=d))
    def __sub__(self, o):
        return TimeSpan((self._dt - o._dt).total_seconds())
    def __lt__(self, o): return self._dt < o._dt
    def __le__(self, o): return self._dt <= o._dt
    def __gt__(self, o): return self._dt > o._dt
    def __ge__(self, o): return self._dt >= o._dt
    def __eq__(self, o): return isinstance(o, DateTime) and self._dt == o._dt
    def __format__(self, spec):
        if not spec:
            return str(self)
        for cs, py in _CS2PY_FMT:
            spec = spec.replace(cs, py)
        return self._dt.strftime(spec)
    def __str__(self):
        return self._dt.strftime("%Y/%m/%d %H:%M:%S")
    def isoformat(self):
        return self._dt.isoformat()

class _DateTimeMeta:
    pass
# DateTime.Now をプロパティ的に使うためのモジュールフック
class _DT:
    MinValue = DateTime(_dt.datetime(1, 1, 1))
    @property
    def Now(self):
        return DateTime(_dt.datetime.now())
    Parse = staticmethod(DateTime.Parse)
_DT.MinValue = DateTime(_dt.datetime(1, 1, 1))
DateTimeNS = _DT()  # transpiler が DateTime.Now → DateTimeNS.Now に置換

# ================= File =================
class File:
    @staticmethod
    def Exists(p): return os.path.exists(p)
    @staticmethod
    def ReadAllText(p):
        with open(p, encoding="utf-8") as f:
            return f.read()
    @staticmethod
    def WriteAllText(p, t):
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    @staticmethod
    def Delete(p):
        if os.path.exists(p):
            os.remove(p)
    @staticmethod
    def AppendLine(p, line):
        with open(p, "a", encoding="utf-8") as f:
            f.write(str(line) + "\n")
    @staticmethod
    def ReadAllLines(p):
        with open(p, encoding="utf-8") as f:
            return f.read().splitlines()

class Directory:
    @staticmethod
    def Exists(p): return os.path.isdir(p)
    @staticmethod
    def CreateDirectory(p): os.makedirs(p, exist_ok=True)

# C# ConsoleColor enum順 (0-15)
_CC_ORDER = [ConsoleColor.Black, ConsoleColor.DarkBlue, ConsoleColor.DarkGreen,
             ConsoleColor.DarkCyan, ConsoleColor.DarkRed, ConsoleColor.DarkMagenta,
             ConsoleColor.DarkYellow, ConsoleColor.Gray, ConsoleColor.DarkGray,
             ConsoleColor.Blue, ConsoleColor.Green, ConsoleColor.Cyan,
             ConsoleColor.Red, ConsoleColor.Magenta, ConsoleColor.Yellow,
             ConsoleColor.White]

def CONSOLE_COLOR_BY_INDEX(i):
    return _CC_ORDER[int(i) % 16]

def py_username():
    try:
        import getpass
        return getpass.getuser()
    except Exception:
        return os.environ.get("USER") or os.environ.get("USERNAME") or "Player"

def py_str_list(*names):
    return list(names)

def py_none_list(n):
    return [None] * int(n)

def py_extend_bools(arr, n):
    return list(arr) + [False] * max(0, int(n) - len(arr))

def py_count_completed(missions):
    return sum(1 for m in missions if m.Completed)

def py_filter_missions_uncompleted(missions):
    return [m for m in missions if not m.Completed and m.Name != "???"][:2]

def py_top10_rankings(rankings):
    return sorted(rankings, key=lambda r: r.Money, reverse=True)[:10]

def py_locked_symbols(all_symbols, unlocked):
    return [s for s in all_symbols if s not in unlocked]

def make_mission_savedata_list(missions):
    out = []
    for m in missions:
        d = MissionSaveData()
        d.Name = m.Name
        d.Description = m.Description
        d.Reward = m.Reward
        d.Completed = m.Completed
        out.append(d)
    return out

# ================= helpers =================
def try_parse_int(s):
    try:
        return int(str(s).strip())
    except (ValueError, TypeError):
        return None

def coalesce(a, b):
    return a if a is not None else b
_coalesce = coalesce  # alias

def coalesce_throw(a, exc):
    if a is None:
        raise exc
    return a
_coalesce_throw = coalesce_throw  # alias

def cs_int_parse(s):
    return int(str(s).strip())

# ================= データクラス =================
class MissionSaveData:
    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Reward = 0
        self.Completed = False

class HighScore:
    def __init__(self):
        self.Name = ""
        self.Money = 0
        self.Spins = 0
        self.Date = DateTime(_dt.datetime(1, 1, 1))

class Mission:
    def __init__(self, name, desc, check, reward):
        self.Name = name
        self.Description = desc
        self.CheckComplete = check
        self.Reward = reward
        self.Completed = False

# SaveData のフィールド定義: (名前, 型タグ)  ※transpilerが自動生成して差し替える
SAVEDATA_FIELDS = []  # transpiler 生成

class SaveData:
    def __init__(self):
        for name, typ in SAVEDATA_FIELDS:
            setattr(self, name, _default_for(typ))

def _default_for(typ):
    if typ == "int": return 0
    if typ == "bool": return False
    if typ == "string": return ""
    if typ == "DateTime": return DateTime(_dt.datetime(1, 1, 1))
    if typ == "TimeSpan": return TimeSpan(0)
    if typ == "dict": return {}
    if typ == "list": return []
    if typ == "list_mission": return []
    if typ == "list_highscore": return []
    if typ == "rooms": return [[False]*5, [False]*5, [False]*5, [False]*4]
    return None

def _jsonable(v):
    if isinstance(v, DateTime):
        return {"__dt__": v.isoformat()}
    if isinstance(v, TimeSpan):
        return {"__ts__": v.TotalSeconds}
    if isinstance(v, (MissionSaveData, HighScore)):
        return {"__cls__": type(v).__name__,
                "data": {k: _jsonable(x) for k, x in v.__dict__.items()}}
    if isinstance(v, list):
        return [_jsonable(x) for x in v]
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    return v

def _unjsonable(v):
    if isinstance(v, dict):
        if "__dt__" in v:
            return DateTime.Parse(v["__dt__"])
        if "__ts__" in v:
            return TimeSpan(v["__ts__"])
        if "__cls__" in v:
            cls = {"MissionSaveData": MissionSaveData, "HighScore": HighScore}[v["__cls__"]]
            obj = cls()
            for k, x in v["data"].items():
                setattr(obj, k, _unjsonable(x))
            return obj
        return {k: _unjsonable(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unjsonable(x) for x in v]
    return v

def json_serialize(obj):
    return json.dumps({k: _jsonable(v) for k, v in obj.__dict__.items()},
                      ensure_ascii=False, indent=2)

def json_deserialize_savedata(text):
    if not text or not text.strip():
        return None
    raw = json.loads(text)
    sd = SaveData()
    for k, v in raw.items():
        setattr(sd, k, _unjsonable(v))
    return sd
