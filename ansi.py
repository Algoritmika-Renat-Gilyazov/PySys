import sys

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32
    
    kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
    kernel32.GetStdHandle.restype = wintypes.HANDLE
    kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel32.GetConsoleMode.restype = wintypes.BOOL
    kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel32.SetConsoleMode.restype = wintypes.BOOL

    stdout_handle = kernel32.GetStdHandle(wintypes.DWORD(-11))
    
    if stdout_handle and stdout_handle != wintypes.HANDLE(-1).value:
        mode = wintypes.DWORD()
        if kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode)):
            new_mode = mode.value | 0x0004
            kernel32.SetConsoleMode(stdout_handle, new_mode)

def Format(code):
    return f"\033[{code}m"

RESET = Format(0)
BOLD = Format(1)
DIM = Format(2)
ITALIC = Format(3)
UND_LN = Format(4)
BLINK = Format(5)
FLASH = Format(6)
INVERT = Format(7)

TEXT_BLACK = Format(30)
BG_BLACK = Format(40)
TEXT_BLACK_G = Format(90)
BG_BLACK_G = Format(100)

TEXT_RED = Format(31)
BG_RED = Format(41)
TEXT_RED_G = Format(91)
BG_RED_G = Format(101)

TEXT_GREEN = Format(32)
BG_GREEN = Format(42)
TEXT_GREEN_G = Format(92)
BG_GREEN_G = Format(102)

TEXT_YELLOW = Format(33)
BG_YELLOW = Format(43)
TEXT_YELLOW_G = Format(93)
BG_YELLOW_G = Format(103)

TEXT_BLUE = Format(34)
BG_BLUE = Format(44)
TEXT_BLUE_G = Format(94)
BG_BLUE_G = Format(104)

TEXT_MAGENTA = Format(35)
BG_MAGENTA = Format(45)
TEXT_MAGENTA_G = Format(95)
BG_MAGENTA_G = Format(105)

TEXT_CYAN = Format(36)
BG_CYAN = Format(46)
TEXT_CYAN_G = Format(96)
BG_CYAN_G = Format(106)

TEXT_WHITE = Format(37)
BG_WHITE = Format(47)
TEXT_WHITE_G = Format(97)
BG_WHITE_G = Format(107)

