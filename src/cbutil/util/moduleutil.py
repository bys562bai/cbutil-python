import runpy,sys

from .path import Path

def load_modlue(path):
    path = Path(path)
    cur_sys_path = sys.path.copy()
    sys.path[0] = path.prnt.to_str()
    runpy.run_path(path.to_str(), run_name=path.stem)
    sys.path = cur_sys_path