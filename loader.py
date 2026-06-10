import sc64
import time
from pathlib import Path
from traceback import format_exc

if __name__ != "__main__":
    quit(1)

(Path(__file__).parent / "main").touch()

try:
    import fs
    import krnl
    import sys
    krnl.Start(*sys.argv)
except Exception:
    sc64.Crash(format_exc())
