import pathlib
import chardet
from .iterutil import is_iterable
import shutil
from zipfile import ZipFile
from .pbar import file_proc_bar
from .util import get_unique_name
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
        
    @property
    def size(self):
        return self.stat().st_size
    
    @property
    def rsize(self):
        return self.stat().st_rsize

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

    def get_sibling_iter(self, *filters):
        return self.prnt.get_son_iter(lambda x: x!=self, *filters)

    @property
    def son_iter(self):
        return self.get_son_iter()

    @property
    def sibling_iter(self, *filters):
        return self.get_sibling_iter()

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
    def siblings(self):
        return list(self.sibling_iter)

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
    
    def mkdir(self, *args, do_if_exist =True, parents =True, **kwargs):
        if not self.exists():
            return super().mkdir(*args, parents=parents, **kwargs)

    def remove(self):
        if self.exists():
            if self.is_dir():
                shutil.rmtree(self.absolute().to_str())
            else:
                os.remove(self.absolute().to_str())
    
    def to_str(self):
        return str(self)

    def copy_to(self, dst):
        a = self.to_str()
        b = Path(dst).to_str()
        if self.is_dir():
            shutil.copytree(a,b)
        else:
            shutil.copyfile(a,b)

    def move_to(self, dst):
        a = self.to_str()
        b = Path(dst).to_str()
        shutil.move(a,b)

    def make_archive(self, dst, format = None):
        dst = Path(dst)
        if format == None:
            format = dst.detect_format_by_suffix()
            if format == None:
                format = 'zip'
        a = self.absolute().to_str()
        b = dst.absolute().to_str()
        shutil.make_archive(b, format, a)

    def unpack_archive_to(self, dst, format = None):
        if format == None:
            format = self.detect_format_by_suffix()
        a = self.absolute().to_str()
        b = Path(dst).absolute().to_str()
        shutil.unpack_archive(a,b,format)

    def detect_format_by_suffix(self):
        m = {
            'zip' : 'zip',
            'tar' : 'tar',
            'gz' : 'gztar',
            'bz' : 'bztar',
            'xz' : 'xztar'
        }
        ext = self.ext
        if ext:
            format = m.get(ext)
            if format:
                return format
            else:
                return ext
        
    def unzip(self, dst):
        dst = Path(dst).absolute().to_str()
        zf = ZipFile(self.to_str())
        l = zf.infolist()
        file_num = len(l)
        total_size = sum(f.file_size for f in l)
        total_compress_size = sum(f.compress_size for f in l)
        print(f'Unzip: {self.absolute().to_str()}')
        print(f'Unzip to: {dst}')
        # print(f'Number of items: {file_num}')
        # print(f'Total size: {total_size}')
        # print(f'Total Compress size: {total_compress_size}')
        with file_proc_bar(total=total_compress_size) as bar:
            for i,f in enumerate(l):
                zf.extract(f, dst)
                bar.set_description(f'{i}')
                bar.update(f.compress_size)

    def get_unique_path(self):
        name = self.name
        prnt = self.prnt
        son_names = [x.name for x in prnt.son_iter]
        name = get_unique_name(name, son_names)
        return prnt/name

    def make_temp_dir(self):
        if self.is_file():
            dir_ = self.prnt
        else:
            dir_ = self
        uqtmp = (dir_/'temp').get_unique_path()
        uqtmp.mkdir()
        return uqtmp

    def remove_temp_sons(self):
        assert(self.is_dir())
        for son in self.sons:
            if son.name.startswith('temp'):
                son.remove()

    def rename_inplace(self, name:str):
        new_path = self.prnt/name
        self.rename(new_path)

    def move_all_sons_to(self, dst):
        for son in self.sons:
            son.move_to(dst)

    def move_all_out(self):
        assert(self.is_dir())
        uq_name = get_unique_name(self.name,[x.name for x in self.son_iter] + [x.name for x in self.siblings])
        if uq_name!=self.name:
            self.rename_inplace(uq_name)
            self = self.prnt/uq_name
        self.move_all_sons_to(self.prnt)
        self.remove()

del _Path
