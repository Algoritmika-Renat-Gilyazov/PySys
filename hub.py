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
        
        if cwd is None:
            self.cwd = fs.Element(Path("/"))
        else:
            self.cwd = cwd
            
        self.real_cwd = self.root_dir
        self.inp = ""
        self.inp0 = []
        self.command = ""
        self.args = []
    def Start(self):
        with Pool(processes=2) as p:
            self.MainCycle()
        
    def UpdateRealCwd(self):
        self.real_cwd = (self.root_dir / self.cwd.path.relative_to("/")).resolve()

    def ChangeDirectory(self, target_str: str):
        """Safe directory change"""
        target_path = Path(target_str)
        
        if target_str.startswith("/"):
            new_relative = Path(target_str.lstrip("/"))
        else:
            new_relative = self.cwd.path / target_path

        potential_real_path = (self.root_dir / new_relative).resolve()
        
        if self.root_dir in potential_real_path.parents or self.root_dir == potential_real_path:
            if potential_real_path.is_dir():
                virtual_relative = potential_real_path.relative_to(self.root_dir)
                self.cwd = fs.Element(Path("/") / virtual_relative)
                self.UpdateRealCwd()
            else:
                print(f"{TEXT_RED}Error: directory not found.{RESET}")
        else:
            print(f"{TEXT_RED}Access denied by virtual filesystem contoller.{RESET}")

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
                case "exit":
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{TEXT_MAGENTA_G}Do you mean 'shutdown' for exit form console?")
                    self.Help()
                case _:
                    print(f"{TEXT_RED}Unknown command: '{self.command}'.{RESET}")
                    self.Help()
            print()
    def Help(self):
        print(f"{BOLD}{TEXT_MAGENTA_G}Help:\n{RESET}{TEXT_YELLOW_G}shutdown:{TEXT_GREEN} Exit from console and shutdown.\n{TEXT_YELLOW_G}crash:{TEXT_GREEN} Crash manually.\n{TEXT_YELLOW_G}help:{TEXT_GREEN} Show this message.\n{TEXT_YELLOW_G}echo:{TEXT_GREEN} Print the text.\n{TEXT_YELLOW_G}cd:{TEXT_GREEN} Change directory.")
        print(RESET, end="")

def Start():
    term = Terminal()
    term.Start()