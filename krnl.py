from fs import *
from pathlib import Path
from sc64 import *
import hub
import time
from multiprocessing import Pool

dt = ""
def running():
    return (Path(__file__).parent / "main").exists()

def Check():
    cond = Element(Path(__file__).parent / "api.py").IsExists()
    cond = cond and Element(Path(__file__).parent / "hub.py").IsExists()
    cond = cond and Element(Path(__file__).parent / "sc64.py").IsExists()
    if not cond:
        Crash("System is corrupted. Some files don't exist.")

def Start(*args):
    if "--skip-check" not in args:
        Check()
    hub.Start()
    running = True
    with Pool(processes=2) as th:
        res = UpdateDatetime()

def UpdateDatetime():
    global dt
    import datetime
    while running():
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)