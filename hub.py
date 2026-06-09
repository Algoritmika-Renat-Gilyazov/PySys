import json
from multiprocessing import Pool
import fs
from pathlib import Path
import sc64
from ansi import *

version: dict = {}
with open((Path(__file__).parent / "version.json").as_posix(), "r") as f:
    version = json.load(f)
    
def running():
    return (Path(__file__).parent / "main").exists()

class Terminal:
    def __init__(self, cwd=fs.Element("/")):
        self.cwd = cwd
        self.real_cwd = Path(__file__).parent / self.cwd.path
        self.inp = ""
        self.inp0 = []
        self.command = ""
        self.args = []
    def UodateRealCwd(self):
        self.real_cwd = Path(__file__).parent / self.cwd.path
    def Start(self):
        print(f"PySys {version.get("name", "Unknown")}.\nCopyleft.")
        print("\n")
        with Pool(processes=2) as pool:
            res = self.MainCycle()
    def MainCycle(self):
        while running():
            self.inp = input(f"{str(self.cwd.path)}> ")
            self.inp0 = self.inp.split()
            try:
                self.command = self.inp0[0]
            except IndexError:
                self.command = ""
            try:
                self.args = self.inp0[1:]
            except IndexError:
                self.args = []
            match(self.command):
                case "":
                    pass
                case "shutdown":
                    (Path(__file__).parent / "main").unlink(True)
                case "crash":
                    sc64.Crash("Test crash.")
                case "help":
                    self.Help()
                case "echo":
                    print(*self.args)
                case "exit":
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{TEXT_MAGENTA_G}Do you mean 'shutdown' for exit form console?\n")
                    self.Help()
                case _:
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{RESET}\n")
                    self.Help()
            print()
    def Help(self):
        print(f"{BOLD}{TEXT_MAGENTA_G}Help:\n{RESET}{TEXT_YELLOW_G}shutdown:{TEXT_GREEN} Exit from console and shutdown.\n{TEXT_YELLOW_G}crash:{TEXT_GREEN} Crash manually.\n{TEXT_YELLOW_G}help:{TEXT_GREEN} Show this message.\n{TEXT_YELLOW_G}echo:{TEXT_GREEN} Print the text.")
        print(RESET)

def Start():
    term = Terminal()
    term.Start()