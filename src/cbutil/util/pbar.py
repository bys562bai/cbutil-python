from tqdm import tqdm

def proc_file_bar(iterable, chunk_size, total_size):
    def bar():
        with tqdm(unit= 'b', unit_scale= True, total=total_size) as pbar:
            for x in iterable:
                updated_size = yield x
                if updated_size:
                    chunk_size = updated_size
                pbar.update(chunk_size)
    return bar()

__all__ = ['proc_file_bar']