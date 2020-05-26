from functools import partial

def compute_length(*args,**kwargs):
    sep = kwargs.get('sep')
    end = kwargs.get('end')
    arg_num = len(args)
    length = 0
    if sep: length+= max(arg_num-1,0)*len(sep)
    if end: length+=len(end)
    length+=sum(map(len,map(str,args)))
    return length

printn = partial(print, end='')

def printr(*args, len=0, **kwargs):
    printn('\r' + ' '*len)
    printn('\r')
    printn(*args, **kwargs)

class InlinePrinter:
    def __init__(self):
        self.is_first = True
        self.cur_len = 0
        
    def print(self, *args,**kwargs):
        print = [self.printr,self.printn][self.is_first]
        print(*args,**kwargs)

    def printn(self, *args, **kwargs):
        printn(*args,**kwargs)
        self.cur_len = compute_length(*args, **kwargs)

    def printr(self, *args, **kwargs):
        printr(*args, len=self.cur_len,**kwargs)
        self.cur_len = compute_length(*args, **kwargs)


def inline_print():
    p = InlinePrinter()
    return p.print


__all__ = ['printn', 'printr', 'inline_print', 'InlinePrinter']