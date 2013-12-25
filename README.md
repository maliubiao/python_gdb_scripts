python-gdb-scripts
==================
gdb helper scripts.

##internel.pause4gdb
###Demo
```shell
./test_internel.py
waiting gdb... Press CTRL-C to proceed 
Loaded symbols for /usr/lib64/libpython2.7.so.1.0
0x00007f46cde701b0 in __nanosleep_nocancel () from /lib64/libc.so.6
(gdb)bt 
#0  0x00007f46cde701b0 in __nanosleep_nocancel () from /lib64/libc.so.6
#1  0x00007f46cde70071 in sleep () from /lib64/libc.so.6
#2  0x00007f46cdbb40c0 in sigusr1_handler (sig=<optimized out>)
    at internel.c:26
#3  <signal handler called>
#4  0x00007f46ce877a90 in __nanosleep_nocancel ()
    at ../sysdeps/unix/syscall-template.S:81
#5  0x00007f46cdbb3f28 in internel_pause4gdb (object=<optimized out>, 
    args=<optimized out>) at internel.c:107
#6  0x00000000004a5bfe in call_function (oparg=<optimized out>, pp_stack=
    0x7fff75819770) at Python/ceval.c:4021
#7  PyEval_EvalFrameEx (f=<optimized out>, throwflag=throwflag@entry=0)
    at Python/ceval.c:2666
#8  0x00000000004a5c9c in fast_function (nk=<optimized out>, na=0, 
    n=<optimized out>, pp_stack=0x7fff75819970, func=
    <function at remote 0x7f46ceb6a578>) at Python/ceval.c:4107
#9  call_function (oparg=<optimized out>, pp_stack=0x7fff75819970)
    at Python/ceval.c:4042 
...
``` 
##pyshow PyObject *
###Demo
```shell
Breakpoint 3, PyEval_EvalCodeEx (co=co@entry=0x7ffff7f81030, 
globals=globals@entry=0x6252c0, locals=locals@entry=0x6252c0, 
args=args@entry=0x0, argcount=argcount@entry=0, kws=kws@entry=0x0, 
kwcount=kwcount@entry=0, defs=defs@entry=0x0, defcount=defcount@entry=0, 
closure=closure@entry=0x0) at Python/ceval.c:3018
3018    in Python/ceval.c
(gdb) pyshow f->f_code->co_filename
{'length': 48,
 'type': u'str',
 'value': '/data/project/py/Python-2.7.3/Lib/_weakrefset.py'}
(gdb) pyshow globals 
```
```shell
(gdb) pyshow f->f_globals
{'ma_fill': 8,
 'ma_mask': 31,
 'ma_used': 8,
 'objects': [({'length': 8, 'type': u'str', 'value': '__file__'},
              {'length': 49,
               'type': u'str',
               'value': '/data/project/py/Python-2.7.3/Lib/_weakrefset.pyc'}),
             ({'length': 8, 'type': u'str', 'value': '__name__'},
              {'length': 11, 'type': u'str', 'value': '_weakrefset'})],
 'type': u'dict'}
```
```shell
(gdb) pyshow f->f_builtins
{'ma_fill': 137,
 'ma_mask': 511,
 'ma_used': 137,
 'objects': [({'length': 5, 'type': u'str', 'value': 'False'},
              {'type': u'bool', 'value': '0'}),
             ({'length': 4, 'type': u'str', 'value': 'True'},
              {'type': u'bool', 'value': '1'}),
             ({'length': 8, 'type': u'str', 'value': '__name__'},
              {'length': 11, 'type': u'str', 'value': '__builtin__'}),
             ({'length': 7, 'type': u'str', 'value': '__doc__'},
              {'length': 126,
               'type': u'str',
               'value': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices."}),
             ({'length': 9, 'type': u'str', 'value': '__debug__'},
              {'type': u'bool', 'value': '1'})],
 'type': u'dict'}
```
```shell
(gdb) pyshow f->f_code->co_code
{'length': '332',
 'type': u'str',
 'value': 'e\x00\x00Z\x01\x00d\x1f\x00d\x00\x00\x84\x01\x00Z\x03\x00d\x01\x00\x84\x00\x00Z\x04\x00d\x02\x00\x84\x00\x00Z\x05\x00d\x03\x00\x84\x00\x00Z\x06\x00d\x04\x00\x84\x00\x00Z\x07\x00d\x05\x00\x84\x00\x00Z\x08\x00d\x1f\x00Z\t\x00d\x06\x00\x84\x00\x00Z\n\x00d\x07\x00\x84\x00\x00Z\x0b\x00d\x08\x00\x84\x00\x00Z\x0c\x00d\t\x00\x84\x00\x00Z\r\x00d\n\x00\x84\x00\x00Z\x0e\x00d\x0b\x00\x84\x00\x00Z\x0f\x00d\x0c\x00\x84\x00\x00Z\x10\x00d\r\x00\x84\x00\x00Z\x11\x00d\x0e\x00\x84\x00\x00Z\x12\x00d\x0f\x00\x84\x00\x00Z\x13\x00e\x13\x00Z\x14\x00d\x10\x00\x84\x00\x00Z\x15\x00d\x11\x00\x84\x00\x00Z\x16\x00d\x12\x00\x84\x00\x00Z\x17\x00e\x17\x00Z\x18\x00d\x13\x00\x84\x00\x00Z\x19\x00d\x14\x00\x84\x00\x00Z\x1a\x00d\x15\x00\x84\x00\x00Z\x1b\x00e\x1b\x00Z\x1c\x00d\x16\x00\x84\x00\x00Z\x1d\x00d\x17\x00\x84\x00\x00Z\x1e\x00e\x1e\x00Z\x1f\x00d\x18\x00\x84\x00\x00Z \x00d\x19\x00\x84\x00\x00Z!\x00d\x1a\x00\x84\x00\x00Z"\x00e"\x00Z#\x00d\x1b\x00\x84\x00\x00Z$\x00d\x1c\x00\x84\x00\x00Z%\x00d\x1d\x00\x84\x00\x00Z&\x00e&\x00Z\'\x00d\x1e\x00\x84\x00\x00Z(\x00RS'}
```
