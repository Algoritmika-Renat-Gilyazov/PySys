from pathlib import Path
from dataclasses import dataclass
import sc64 as sc

@dataclass
class Element:
    path: Path
    owner: str = "*"
    def IsFolder(self):
        if (self.path.exists() and self.path.is_dir()) or str(self.path)[-1] == "/":
            return True
        return False
    def IsFile(self):
        if (self.path.exists() and self.path.is_file()) or str(self.path)[-1] != "/":
            return True
        return False
    def IsLink(self):
        if "://" in str(self.path):
            return True
        return False
    def GetParent(self):
        return self.path.parent
    def AddChild(self, ch: Element):
        path = Element(self.path / ch.path)
        if path.IsFile():
            path.path.touch()
        elif path.IsFolder():
            path.path.mkdir(parents=True, exist_ok=True)
        else:
            sc.Err(f"{str(ch.path)} isn't a correct element.")
    def IsExists(self):
        return self.path.exists()