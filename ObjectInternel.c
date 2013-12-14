#include <Python.h>

#define PycStringO_CheckExact(op) (strcmp(Py_TYPE(op)->tp_name, "cStringIO.StringO") == 0)
#define PycStringI_CheckExact(op) (strcmp(Py_TYPE(op)->tp_name, "cStringIO.StringI") == 0)

/* Declarations for objects of type StringO */ 

typedef struct {
  PyObject_HEAD
  char *buf;
  Py_ssize_t pos, string_size;

  Py_ssize_t buf_size;
  int softspace;
} Oobject;

/* Declarations for objects of type StringI */

typedef struct {
  PyObject_HEAD
  char *buf;
  Py_ssize_t pos, string_size;
  /* We store a reference to the object here in order to keep
     the buffer alive during the lifetime of the Iobject. */
  PyObject *pbuf;
} Iobject;



PyDoc_STRVAR(cStringIO_get_internel_doc, "c strut Oobject");

static PyObject *
cStringIO_get_internel(PyObject *object, PyObject *args)
{
	PyObject *io;	
	PyObject *dict;
	Oobject *o;
	if(!PyArg_ParseTuple(args, "O:get_internel", &io)) {
		return NULL;
	}
	if (PycStringI_CheckExact(io)) {
		PyErr_SetString(PyExc_TypeError,
				"bufsize for input io is not meaningful");
			return NULL;
	}
	if (!PycStringO_CheckExact(io)) {
		PyErr_SetString(PyExc_TypeError,
				"need a cStringIO object");
		return NULL;
	}
	o = (Oobject *)io;
	dict = PyDict_New();
	PyDict_SetItemString(dict, "bufsize", PyInt_FromLong(o->buf_size)); 
	PyDict_SetItemString(dict, "pos", PyInt_FromLong(o->pos));
	PyDict_SetItemString(dict, "string_size", PyInt_FromLong(o->string_size));
	return dict; 
}

static struct PyMethodDef ObjectInternel_methods[] = {
	{"cStringIO_internel", (PyCFunction)cStringIO_get_internel,
		METH_VARARGS, cStringIO_get_internel_doc},
	{NULL, NULL}
};


PyMODINIT_FUNC initObjectInternel(void)
{
	PyObject *m;
	m = Py_InitModule("ObjectInternel", ObjectInternel_methods); 
	if (m == NULL)
		return;
}
