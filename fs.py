from pathlib import Path
from dataclasses import dataclass
import sc64 as sc

@dataclass
class Element:
    path: Path
    owner: str = "*"
    def IsFolder(self, base_path: Path = None):
        if base_path:
            real_path = (base_path / str(self.path).lstrip("/")).resolve()
            return real_path.is_dir()
        return str(self.path).endswith("/") or self.path.suffix == ""
    def IsFile(self, base_path: Path = None):
        if base_path:
            real_path = (base_path / str(self.path).lstrip("/")).resolve()
            return real_path.is_file()
        return not self.IsFolder() and not self.IsLink()
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
    def IsExists(self, base_path: Path = None) -> bool:
        if base_path:
            return (base_path / str(self.path).lstrip("/")).resolve().exists()
        return self.path.exists()
    def IsSubpathOf(self, base_path: Path) -> bool:
        try:
            resolved_base = base_path.resolve()
            resolved_self = (base_path / self.path).resolve()
        
            return resolved_base in resolved_self.parents or resolved_base == resolved_self
        except Exception:
            return False