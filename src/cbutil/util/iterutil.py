from collections.abc import Iterable
from .util import is_iterable
from collections import deque



#begin impl

def preorder_iter_impl1(root):
    for n in root:
        yield n
        if is_iterable(n):
            yield from preorder_iter_impl1(n)

def postorder_iter_impl1(root):
    for n in root:
        if is_iterable(n):
            yield from postorder_iter_impl1(n)
        yield n


def preorder_iter_impl4(root, cond):
    if not cond(root): return
    for n in root:
        yield n
        if is_iterable(n):
            yield from preorder_iter_impl4(n, cond)

def postorder_iter_impl4(root, cond):
    if not cond(root): return
    for n in root:
        if is_iterable(n):
            yield from postorder_iter_impl4(n, cond)
        yield n

        

def preorder_iter_impl2(root, get_son_iter):
    it = get_son_iter(root)
    if not is_iterable(it): return
    for n in it:
        yield n
        yield from preorder_iter_impl2(n, get_son_iter)

def postorder_iter_impl2(root, get_son_iter):
    it = get_son_iter(root)
    if not is_iterable(it): return
    for n in it:
        yield from postorder_iter_impl2(n, get_son_iter)
        yield n


def preorder_iter_impl3(root, get_son_iter, cond):
    if not cond(root): return
    it = get_son_iter(root)
    if not is_iterable(it): return
    for n in it:
        yield n
        yield from preorder_iter_impl3(n, get_son_iter, cond)

def postorder_iter_impl3(root, get_son_iter, cond):
    if not cond(root): return
    it = get_son_iter(root)
    if not is_iterable(it): return
    for n in it:
        yield from postorder_iter_impl3(n, get_son_iter, cond)       
        yield n


def breadth_iter_impl1(root):
    q = deque()
    q.append(root)

    while len(q):
        it = q.popleft()
        for n in it:
            yield n
            if is_iterable(n):
                q.append(n)

def breadth_iter_impl4(root, cond):
    q = deque()
    if not cond(root): return
    q.append(root)
    while len(q):
        it = q.popleft()
        for n in it:
            yield n
            if is_iterable(n) and cond(n):
                q.append(n)


def breadth_iter_impl2(root, get_son_iter):
    it = get_son_iter(root)
    if not is_iterable(it):
        return
    q = deque()
    q.append(it)

    while len(q):
        it = q.popleft()
        for n in it:
            yield n
            it_ = get_son_iter(n)
            if is_iterable(it_):
                q.append(it_)

def breadth_iter_impl3(root, get_son_iter, cond):
    if not cond(root): return
    it = get_son_iter(root)
    if not is_iterable(it):
        return
    q = deque()
    q.append(it)

    while len(q):
        it = q.popleft()
        for n in it:
            yield n
            if not cond(root): continue
            it_ = get_son_iter(n)
            if is_iterable(it_):
                q.append(it_)
#end impl


def preorder_iter(root, get_son_iter = None, cond = None):
    if get_son_iter == None and cond == None:
        yield from preorder_iter_impl1(root)
    elif get_son_iter == None:
        yield from preorder_iter_impl4(root, cond)
    elif cond == None:
        yield from preorder_iter_impl2(root, get_son_iter)
    else:
        yield from preorder_iter_impl3(root, get_son_iter, cond)

def postorder_iter(root, get_son_iter = None, cond = None):
    if get_son_iter == None and cond == None:
        yield from postorder_iter_impl1(root)
    elif get_son_iter == None:
        yield from postorder_iter_impl4(root, cond)
    elif cond == None:
        yield from postorder_iter_impl2(root, get_son_iter)
    else:
        yield from postorder_iter_impl3(root, get_son_iter, cond)


def breadth_iter(root, get_son_iter = None, cond = None):
    if get_son_iter == None and cond == None:
        yield from breadth_iter_impl1(root)
    elif get_son_iter == None:
        yield from breadth_iter_impl4(root, cond)
    elif cond == None:
        yield from breadth_iter_impl2(root, get_son_iter)
    else:
        yield from breadth_iter_impl3(root, get_son_iter, cond)




class TreeIter:
    def __init__(self, root, get_son_iter = iter, cond = lambda x: True):
        self.nodes = [root]
        self.get_son_iter = get_son_iter
        self.cond = cond

    @property
    def root(self):
        return self.nodes[0]

    @root.setter
    def root(self,x):
        self.nodes[0] = x

    @property
    def cur_node(self):
        return self.nodes[-1]

    @cur_node.setter
    def cur_node(self,x):
        self.nodes[-1] = x

    @property
    def cur_deepth(self):
        return len(self.nodes) -1


    def preorder_iter(self):
        cur_node = self.cur_node
        cond = self.cond
        if not cond(cur_node): return
        it = self.get_son_iter(cur_node)
        if not is_iterable(it): return
        nodes = self.nodes
        cur_len = len(nodes)

        try:
            n = next(it)
        except StopIteration:
            return

        nodes.append(n)
        yield n
        yield from self.preorder_iter()

        for n in it:
            self.cur_node = n
            yield n
            yield from self.preorder_iter()
        self.nodes = nodes[0: cur_len]

    def postorder_iter(self):
        cur_node = self.cur_node
        cond = self.cond
        if not cond(cur_node): return
        it = self.get_son_iter(cur_node)
        if not is_iterable(it):
            return

        nodes = self.nodes
        cur_len = len(nodes)

        try:
            n = next(it)
        except StopIteration:
            return
        nodes.append(n)
        yield from self.postorder_iter()      
        self.cur_node = n 
        yield n

        for self.cur_node in it:
            yield from self.postorder_iter()
            yield self.cur_node

        self.nodes = nodes[0: cur_len]

    def breadth_iter(self):
        cur_node = self.cur_node
        cond = self.cond
        if not cond(cur_node): return
        
        get_son_iter = self.get_son_iter
        nodes = self.nodes
        cur_len = len(nodes)

        it = get_son_iter(cur_node)
        if not is_iterable(it):
            return

        vi_pair = [cur_node, it]
        q = deque()
        q.append(vi_pair)
        while len(q):
            vi_pair = q.popleft()
            n,it = vi_pair
            try:
                n = next(it)
            except StopIteration:
                continue
            nodes.append(n)
            yield n
            it_ = get_son_iter(n)
            if is_iterable(it_) and cond(n):
                q.append([n,it_])

            for n in it:
                self.cur_node = n 
                yield n
                it_ = get_son_iter(n)
                if is_iterable(it_) and cond(n):
                    q.append([n,it_])
        self.nodes = nodes[0: cur_len]

    pre_iter = preorder_iter
    post_iter = postorder_iter
    bre_iter = breadth_iter
        

pre_iter = preorder_iter
post_iter = postorder_iter
bre_iter = breadth_iter

__all__ = [
    'pre_iter', 'post_iter', 'bre_iter', 
    'preorder_iter', 'postorder_iter', 'breadth_iter',
    'TreeIter'
]