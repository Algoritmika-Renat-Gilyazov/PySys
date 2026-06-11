import sc64
import time
from pathlib import Path
from traceback import format_exc
from ansi import *

if __name__ != "__main__":
    quit(1)

(Path(__file__).parent / "main").touch()

try:
    import fs
    import krnl
    import sys
    blc = "\u2588"
    print(f"{TEXT_WHITE}{blc}" * 15)
    print(f"{TEXT_WHITE}{blc}" * 15)
    print((f"{TEXT_WHITE}{blc}" * 6) + (f"{TEXT_BLUE}{blc}" * 3) + (f"{TEXT_WHITE}{blc}" * 6))
    print((f"{TEXT_WHITE}{blc}" * 5) + (f"{TEXT_BLUE}{blc}" * 5) + (f"{TEXT_WHITE}{blc}" * 5))
    print((f"{TEXT_WHITE}{blc}" * 4) + (f"{TEXT_YELLOW_G}{blc}" * 3) + (f"{TEXT_BLUE}{blc}" * 3) + (f"{TEXT_WHITE}{blc}" * 5))
    print((f"{TEXT_WHITE}{blc}" * 5) + (f"{TEXT_YELLOW_G}{blc}" * 5) + (f"{TEXT_WHITE}{blc}" * 5))
    print((f"{TEXT_WHITE}{blc}" * 6) + (f"{TEXT_YELLOW_G}{blc}" * 3) + (f"{TEXT_WHITE}{blc}" * 6))
    print(f"{TEXT_WHITE}{blc}" * 15)
    print((f"{TEXT_WHITE}{blc}" * 5) + (f"{BG_WHITE}{TEXT_BLACK}{BOLD}PySys{RESET}") + (f"{TEXT_WHITE}{blc}" * 5))
    print(f"{TEXT_WHITE}{blc}" * 15)
    print(f"{TEXT_WHITE}{blc}" * 15)
    time.sleep(5)
    print("\033c", end="")
    krnl.Start(*sys.argv)
except Exception:
    sc64.Crash(format_exc())
