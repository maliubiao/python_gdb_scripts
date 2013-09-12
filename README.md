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
	3018	in Python/ceval.c
	(gdb) pyshow co->co_names
	{'type': u'tuple', 'size': '7'}
	[0]: {'length': '7', 'type': u'str', 'value': u'__doc__'}
	[1]: {'length': '8', 'type': u'str', 'value': u'UserDict'}
	[2]: {'length': '16', 'type': u'str', 'value': u'IterableUserDict'}
	[3]: {'length': '7', 'type': u'str', 'value': u'_abcoll'}
	[4]: {'length': '14', 'type': u'str', 'value': u'MutableMapping'}
	[5]: {'length': '8', 'type': u'str', 'value': u'register'}
	[6]: {'length': '9', 'type': u'str', 'value': u'DictMixin'}
