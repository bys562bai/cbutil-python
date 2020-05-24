import pathlib
import chardet
from .iterutil import is_iterable
import shutil
import os
# from itertools import chain

_Path = type(pathlib.Path(''))


class Path(_Path):
    _Path = _Path

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        absPath = Path._Path(*args, **kwargs).resolve()
        return super().__new__(cls, str(absPath), **kwargs)

    @property
    def prnt(self):
        return Path(super().parent)

    @property
    def ext(self):
        return super().suffix[1:]


#begin iter

    def get_son_iter(self, *filters):
        if self.is_dir():
            if len(filters) == 0:
                return super().iterdir()
            return filter(lambda x: all(map(lambda f: f(x), filters)), super().iterdir())
        else:
            return iter([])

    def get_file_son_iter(self, *filters):
        return self.get_son_iter(Path.is_file, *filters)

    def get_dir_son_iter(self, *filters):
        return self.get_son_iter(Path.is_dir, *filters)

    @property
    def son_iter(self):
        return self.get_son_iter()

    @property
    def file_son_iter(self):
        return self.get_file_son_iter()

    @property
    def dir_son_iter(self):
        return self.get_dir_son_iter()

    @property
    def sons(self):
        return list(self.son_iter)

    @property
    def file_sons(self):
        return list(self.file_son_iter)

    @property
    def dir_sons(self):
        return list(self.dir_son_iter)
#end iter


    @property
    def str(self):
        return self.__str__()


    def rel_to(self,path):
        return super().relative_to(path)

    def open(self,mode, buffering=-1, encoding=None, *args, **kwargs):
        if encoding == None:
            if mode in ('r','r+','rw'):
                with super().open('rb',buffering) as fr:
                    encoding = chardet.detect(fr.read(512))['encoding']
        return super().open(mode,buffering, encoding,*args,**kwargs)
    
    def safe_mkdir(self, mode=0o777):
        if not self.exists():
            return super().mkdir(mode, parents = True)

    def remove(self):
        if self.exists():
            if self.is_dir():
                shutil.rmtree(self.absolute().to_str())
            else:
                os.remove(self.absolute().to_str())
    
    def to_str(self):
        return str(self)

del _Path