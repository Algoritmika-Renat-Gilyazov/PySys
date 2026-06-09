import logging as lg
import json
import time
from ansi import *
from pathlib import Path

content: dict = {}
settings: dict = {}
with open((Path(__file__).parent / "version.json").as_posix(), "r") as f:
    content = json.load(f)
with open((Path(__file__).parent / "settings.json").as_posix(), "r")as f:
    settings = json.load(f)

lg.basicConfig(filename=(Path(__file__).parent / "system.log").as_posix(), level=lg.INFO if content.get("stable", False) else lg.DEBUG, filemode="a")

def Err(msg: str = ""):
    lg.error(msg)
def Info(msg: str = ""):
    lg.info(msg)
def Debug(msg: str = ""):
    lg.debug(msg)
def Crash(msg: str = ""):
    lg.critical(msg)
    # Clean output
    print("\033c", end="")
    if settings.get("insider_crash_enabled", False) and not content.get("stable", False):
        print(BG_GREEN, end="")
    else:
        print(BG_RED, end="")
    print(f"===========\nPySys CRASH\n===========\n\n\tError message: {msg}\n\n\tSystem will shutdown in 10 seconds.\n\n\tSystem version: {content.get("id", "unkonwn")}")
    print(RESET)
    time.sleep(10)
    (Path(__file__).parent / "main").unlink(True)
    quit(2)