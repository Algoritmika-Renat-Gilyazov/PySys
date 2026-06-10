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
    def __init__(self, cwd=None):
        self.root_dir = Path(__file__).parent.resolve()
        
        self.cwd = cwd if cwd else fs.Element(Path("/"))
        
        self.real_cwd = self.root_dir
        
        self.inp = ""
        self.inp0 = []
        self.command = ""
        self.args = []
        
        self.UpdateRealCwd()

    def UpdateRealCwd(self):
        virtual_str = str(self.cwd.path).lstrip("/")
        self.real_cwd = (self.root_dir / virtual_str).resolve()

    def ChangeDirectory(self, target_str: str):
        self.cwd = fs.Element(target_str)
        # Verification underconstruction
        return
        try:
            target = Path(target_str).resolve()
        except:
            print(f"{TEXT_RED}Directory '{target_str}' doesn't exists.{RESET}")
            return
        print(f"[DEBUG] target: {target.as_posix()}")
        root = Path(__file__).parent
        print(f"[DEBUG] Parents: {target.parents}")
        if root in target.parents or target == root:
            self.cwd = fs.Element(target.resolve().relative_to(self.cwd.path))
            self.UpdateRealCwd()
        else:
            print(f"{TEXT_RED}Access denied.{RESET}")

    def Start(self):
        print(f"PySys {version.get('name', 'Unknown')}.\nCopyleft.")
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
                case "cd":
                    if self.args:
                        self.ChangeDirectory(self.args[0])
                    else:
                        self.ChangeDirectory("/")
                case "shutdown":
                    (Path(__file__).parent / "main").unlink(True)
                case "crash":
                    sc64.Crash("Test crash.")
                case "help":
                    self.Help()
                case "echo":
                    print(*self.args)
                case _:
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{RESET}\n")
                    self.Help()
            print()

    def Help(self):
        print(f"{BOLD}{TEXT_MAGENTA_G}Help:\n{RESET}{TEXT_YELLOW_G}cd [путь]:{TEXT_GREEN} Сменить директорию.\n{TEXT_YELLOW_G}shutdown:{TEXT_GREEN} Exit from console and shutdown.\n{TEXT_YELLOW_G}crash:{TEXT_GREEN} Crash manually.\n{TEXT_YELLOW_G}help:{TEXT_GREEN} Show this message.\n{TEXT_YELLOW_G}echo:{TEXT_GREEN} Print the text.\n{TEXT_YELLOW_G}cd:{TEXT_GREEN} Change directory.")
        print(RESET)

def Start():
    term = Terminal()
    term.Start()