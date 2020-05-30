import sys
import importlib.util as imputil
import runpy

from .path import Path

def load_module(path):
    path = Path(path)
    cur_sys_path = sys.path.copy()
    sys.path[0] = path.prnt.to_str()
    m = __import__(path.stem)
    sys.path = cur_sys_path
    return m

__all__ = ['load_module']