#include <Python.h>
#include <signal.h>
#include <stdlib.h> 
#include <sys/types.h>
#include <sys/wait.h>

#define PycStringO_CheckExact(op) (strcmp(Py_TYPE(op)->tp_name, "cStringIO.StringO") == 0)
#define PycStringI_CheckExact(op) (strcmp(Py_TYPE(op)->tp_name, "cStringIO.StringI") == 0)

typedef void (*sighandler_t)(int);

sighandler_t prev;
int GDB_ATTACHED = 0; 
int MASTERPID = 0; 

void sigusr1_handler(int sig)
{ 
	int status;
	char buf[128]; 
	if (GDB_ATTACHED == 0) { 
		GDB_ATTACHED = 1; 
		if (fork() == 0) {
			signal(SIGINT, SIG_IGN);
			snprintf(buf, 128, "gdb -p %d", MASTERPID); 
			exit(system(buf));
		} else {
			sleep(1);
		}
	} else {
		/* gdb has detached from this process */
		waitpid(-1, &status, WNOHANG); 
		PySys_WriteStdout("received SIGINT, quit");
		exit(0);
	}
}

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

PyDoc_STRVAR(internel_pause4gdb_doc, "wait gdb");

static PyObject *
internel_pause4gdb(PyObject *object, PyObject *args)
{ 
	struct timespec req; 
	req.tv_sec = 0;
	req.tv_nsec = 100000; 
	
	MASTERPID = getpid();

	prev = signal(SIGINT, sigusr1_handler);	
	if (prev < 0) {
		Py_RETURN_FALSE;
	} 
	PySys_WriteStdout("waiting gdb... Press CTRL-C to proceed\n");
	while (1) {
		nanosleep(&req, 0);
		if (GDB_ATTACHED == 0)
			continue;
		else { 
			PySys_WriteStdout("gdb attached...\n"); 
			GDB_ATTACHED = 0;
			Py_RETURN_TRUE;
		}		
	}
}

static struct PyMethodDef internel_methods[] = {
	{"cStringIO_internel", (PyCFunction)cStringIO_get_internel,
		METH_VARARGS, cStringIO_get_internel_doc},
	{"pause4gdb", (PyCFunction)internel_pause4gdb,
		METH_VARARGS, internel_pause4gdb_doc},
	{NULL, NULL}
};


PyMODINIT_FUNC initinternel(void)
{
	PyObject *m;
	m = Py_InitModule("internel", internel_methods); 
	if (m == NULL)
		return;
}
