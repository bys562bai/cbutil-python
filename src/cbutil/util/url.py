import requests
import contextlib
from tqdm import tqdm
from .path import Path
from urllib.parse import urlparse


def download_bar(iterable, chunk_size, total_size):
    def bar():
        with tqdm(unit= 'b', unit_scale= True, total=total_size) as pbar:
            for x in iterable:
                yield x
                pbar.update(chunk_size)
    return bar()

class URL:
    def __init__(self, url):
        self.url = url
        self.o = urlparse(url)

    def to_str(self, ts = str):
        return ts(self.url)

    def __str__(self):
        return self.to_str(str)

    def __repr__(self):
        return self.to_str(repr)

    @property
    def path(self):
        return self.o.path
    
    @property
    def name(self):
        return self.path.split('/')[-1]

    def download(self, save_path, enable_bar = True, chunk_size = 16<<10):
        url = self.url
        save_path = Path(save_path)
        with contextlib.closing(requests.get(url, stream = True)) as r:
            total_size = int(r.headers['Content-Length'] )
            with save_path.open('wb') as fw:
                it = r.iter_content(chunk_size=chunk_size)
                if enable_bar: it = download_bar(it, chunk_size = chunk_size, total_size = total_size)

                print(f'Downloading: {url}')
                print(f'Save as: {save_path}')
                for data in it:
                    fw.write(data)