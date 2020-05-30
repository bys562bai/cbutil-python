import sys
import importlib.util as imputil

from .path import Path

def load_module(path, add_to_sys_modules = False):
    path = Path(path)
    cur_sys_path = sys.path.copy()
    sys.path[0] = path.prnt.to_str()
    spec = imputil.spec_from_file_location(path.stem, path.to_str())
    m = imputil.module_from_spec(spec)
    spec.loader.exec_module(m)
    if add_to_sys_modules:
        sys.modules[spec.name] = m
    sys.path = cur_sys_path
    return m

__all__ = ['load_module']