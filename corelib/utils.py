# -*- coding: utf-8 -*-

import re

class Empty(object):
    def __call__(self, *a, **kw):
        return empty
    def __nonzero__(self):
        return False
    def __contains__(self, item):
        return False
    def __repr__(self):
        return '<Empty Object>'
    def __str__(self):
        return ''
    def __eq__(self, v):
        return isinstance(v, Empty)
    def __getattr__(self, name):
        if not name.startswith('__'):
            return empty
        raise AttributeError(name)
    def __len__(self):
        return 0
    def __getitem__(self, key):
        return empty
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __iter__(self):
        return self
    def next(self):
        raise StopIteration

empty = Empty()

old_pattern = re.compile(r'%\w')
new_pattern = re.compile(r'\{(\w+(\.\w+|\[\w+\])?)\}')

__formaters = {}

def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)

def formater(text):
    """
    >>> format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    """
    def translator(k):
        if '.' in k:
            name,attr = k.split('.')
            if name.isdigit():
                k = int(name)
                return lambda *a, **kw: getattr(a[k], attr)
            return lambda *a, **kw: getattr(kw[name], attr)
        else:
            if k.isdigit():
                return lambda *a, **kw: a[int(k)]
            return lambda *a, **kw: kw[k]
    args = [translator(k) for k,_1 in new_pattern.findall(text)]
    if args:
        if old_pattern.findall(text):
            raise Exception('mixed format is not allowed')
        f = new_pattern.sub('%s', text)
        def _(*a, **kw):
            return f % tuple([k(*a,**kw) for k in args])
        return _
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        n = len(old_pattern.findall(text))
        return lambda *a, **kw: text % tuple(a[:n])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
