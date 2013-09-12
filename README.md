python-gdb-scripts
==================
gdb helper scripts.

##pyshow PyObject *
###Demo
    Breakpoint 3, PyEval_EvalCodeEx (co=co@entry=0x7ffff7f81030, 
        globals=globals@entry=0x6252c0, locals=locals@entry=0x6252c0, 
        args=args@entry=0x0, argcount=argcount@entry=0, kws=kws@entry=0x0, 
        kwcount=kwcount@entry=0, defs=defs@entry=0x0, defcount=defcount@entry=0, 
        closure=closure@entry=0x0) at Python/ceval.c:3018
    3018    in Python/ceval.c
    (gdb) pyshow co->co_filename
    {'length': '32', 'type': u'str', 'value': u'/usr/lib64/python2.7/UserDict.py'} 
    (gdb) pyshow globals
    {'type': u'dict', 'ma_fill': '5', 'ma_used': '5'}
    key: {'length': '12', 'type': u'str', 'value': u'__builtins__'}
    value: {'type': 'dict', 'value': '0x621e70'}
    key: {'length': '8', 'type': u'str', 'value': u'__name__'}
    value: {'length': '8', 'type': u'str', 'value': u'UserDict'}
    key: {'length': '8', 'type': u'str', 'value': u'__file__'}
    value: {'length': '33', 'type': u'str', 'value': u'/usr/lib64/python2.7/UserDict.pyc'} 
    (gdb) pyshow co->co_names
    {'type': u'tuple', 'size': '28'}
    [0]: {'length': '8', 'type': u'str', 'value': u'__name__'}
    [1]: {'length': '10', 'type': u'str', 'value': u'__module__'}
    [2]: {'length': '4', 'type': u'str', 'value': u'None'}
    [3]: {'length': '8', 'type': u'str', 'value': u'__init__'}
    [4]: {'length': '8', 'type': u'str', 'value': u'__repr__'}
    [5]: {'length': '7', 'type': u'str', 'value': u'__cmp__'}
    [6]: {'length': '8', 'type': u'str', 'value': u'__hash__'}
    [7]: {'length': '7', 'type': u'str', 'value': u'__len__'}
    [8]: {'length': '11', 'type': u'str', 'value': u'__getitem__'}
    [9]: {'length': '11', 'type': u'str', 'value': u'__setitem__'}
    [10]: {'length': '11', 'type': u'str', 'value': u'__delitem__'}
    [11]: {'length': '5', 'type': u'str', 'value': u'clear'}
    [12]: {'length': '4', 'type': u'str', 'value': u'copy'}
    [13]: {'length': '4', 'type': u'str', 'value': u'keys'}
    [14]: {'length': '5', 'type': u'str', 'value': u'items'}
    [15]: {'length': '9', 'type': u'str', 'value': u'iteritems'}
    [16]: {'length': '8', 'type': u'str', 'value': u'iterkeys'}
    [17]: {'length': '10', 'type': u'str', 'value': u'itervalues'}
    [18]: {'length': '6', 'type': u'str', 'value': u'values'}
    [19]: {'length': '7', 'type': u'str', 'value': u'has_key'}
    [20]: {'length': '6', 'type': u'str', 'value': u'update'}
    [21]: {'length': '3', 'type': u'str', 'value': u'get'} 
    [22]: {'length': '10', 'type': u'str', 'value': u'setdefault'}
    [23]: {'length': '3', 'type': u'str', 'value': u'pop'}
    [24]: {'length': '7', 'type': u'str', 'value': u'popitem'}
    [25]: {'length': '12', 'type': u'str', 'value': u'__contains__'}
    [26]: {'length': '11', 'type': u'str', 'value': u'classmethod'}
    [27]: {'length': '8', 'type': u'str', 'value': u'fromkeys'}
