import json
from multiprocessing import Pool
import fs
from pathlib import Path
import sc64
from ansi import *
import shutil

version: dict = {}
with open((Path(__file__).parent / "version.json").as_posix(), "r") as f:
    version = json.load(f)

settings: dict = {}
with open((Path(__file__).parent / "settings.json").as_posix(), "r") as f:
    settings = json.load(f)

vfs: bool = settings.get("vfs_enabled", False)

def running():
    return (Path(__file__).parent / "main").exists()

class Terminal:
    def __init__(self, cwd=None):
        self.root_dir = Path(__file__).parent.resolve()
        
        if vfs:
            self.cwd: fs.Element = cwd if cwd else fs.Element(Path("/"))
        else:
            self.cwd: Path = cwd if cwd else self.root_dir
        
        self.real_cwd = self.root_dir
        
        self.inp = ""
        self.inp0 = []
        self.command = ""
        self.args = []
        
        self.UpdateRealCwd()

    def UpdateRealCwd(self):
        if not vfs:
            self.real_cwd = self.cwd.resolve()
            return
        virtual_str = str(self.cwd.path).lstrip("/")
        self.real_cwd = (self.root_dir / virtual_str).resolve()

    def ChangeDirectory(self, target_str: str):
        if not vfs:
            try:
                if (self.cwd / target_str).resolve().is_dir():
                    self.cwd = (self.cwd / target_str).resolve()
                else:
                    print(f"{TEXT_RED}'{(self.cwd / target_str).as_posix()}' not a directory.{RESET}")
                    return
            except:
                print(f"{TEXT_RED}'{(self.cwd / target_str).as_posix()}' not found.{RESET}")
            return
                
        self.cwd = fs.Element(target_str)
        # VFS verification under construction
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
            if vfs:
                self.inp = input(f"{self.cwd.path.as_posix()}> ")
            else:
                self.inp = input(f"{self.cwd.as_posix()}> ")
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
                        print(f"{TEXT_RED}Expected 1 argument, but given 0.{RESET}")
                case "shutdown":
                    (Path(__file__).parent / "main").unlink(True)
                case "crash":
                    sc64.Crash("Test crash.")
                case "help":
                    self.Help()
                case "echo":
                    print(*self.args)
                case "mkdir":
                    if len(self.args) < 1:
                        print(f"{TEXT_RED}Expected 1 argument, but given 0.{RESET}")
                    if not vfs:
                        path = Path(self.args[0]).relative_to(self.cwd)
                    else:
                        path = Path(self.args[0]).relative_to(self.real_cwd)
                    path.mkdir(parents=True, exist_ok=True)
                case "rmdir":
                    if len(self.args) < 1:
                        print(f"{TEXT_RED}Expected 1 argument, but given 0.{RESET}")
                    if not vfs:
                        path = Path(self.args[0]).relative_to(self.cwd)
                    else:
                        path = Path(self.args[0]).relative_to(self.real_cwd)
                    shutil.rmtree(path.as_posix(), ignore_errors=True)
                case "touch":
                    if len(self.args) < 1:
                        print(f"{TEXT_RED}Expected 1 argument, but given 0.{RESET}")
                    if not vfs:
                        path = Path(self.args[0]).relative_to(self.cwd)
                    else:
                        path = Path(self.args[0]).relative_to(self.real_cwd)
                    path.touch(parents=True, exist_ok=True)
                case "rm":
                    if len(self.args) < 1:
                        print(f"{TEXT_RED}Expected 1 argument, but given 0.{RESET}")
                    if not vfs:
                        path = Path(self.args[0]).relative_to(self.cwd)
                    else:
                        path = Path(self.args[0]).relative_to(self.real_cwd)
                    path.unlink(missing_ok=True)
                case _:
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{RESET}\n")
                    self.Help()
            print()

    def Help(self):
        print(f"{BOLD}{TEXT_MAGENTA_G}Help:\n{RESET}{TEXT_YELLOW_G}shutdown:{TEXT_GREEN} Exit from console and shutdown.\n{TEXT_YELLOW_G}crash:{TEXT_GREEN} Crash manually.\n{TEXT_YELLOW_G}help:{TEXT_GREEN} Show this message.\n{TEXT_YELLOW_G}echo:{TEXT_GREEN} Print the text.\n{TEXT_YELLOW_G}cd:{TEXT_GREEN} Change directory.\n{TEXT_YELLOW_G}mkdir:{TEXT_GREEN} Create a directory.\n{TEXT_YELLOW_G}rmdir:{TEXT_GREEN} Remove a directory.\n{TEXT_YELLOW_G}touch:{TEXT_GREEN} Create a file.\n{TEXT_YELLOW_G}rm:{TEXT_GREEN} Remove a file.")
        print(RESET)

def Start():
    term = Terminal()
    term.Start()