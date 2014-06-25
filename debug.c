#include <Python.h>
#include <signal.h>
#include <stdlib.h> 
#include <sys/types.h>
#include <sys/wait.h>

typedef void (*sighandler_t)(int);

sighandler_t prev;
int gdb_attached = 0; 
int masterpid = 0; 

void sigint_handler(int sig)
{ 
	int status;
	char buf[32]; 
	if (gdb_attached == 0) { 
		gdb_attached = 1; 
		if (fork() == 0) {
			signal(SIGINT, SIG_IGN);
			snprintf(buf, 32, "gdb -p %d", masterpid); 
			//call gdb
			status = system(buf);
			//notify main process
			kill(getppid(), SIGINT);
			exit(status);
		} else {
			//main process sleep
			sleep(1);
		}
	} else {
		/* gdb has detached from this process */
		waitpid(-1, &status, WNOHANG); 
		PySys_WriteStdout("received SIGINT, quit\n");
		exit(0);
	}
}


PyDoc_STRVAR(debug_pause4gdb_doc, "wait gdb");

static PyObject *
debug_pause4gdb(PyObject *object, PyObject *args)
{ 
	struct timespec req; 
	req.tv_sec = 0;
	req.tv_nsec = 100000; 
	
	masterpid = getpid();

	prev = signal(SIGINT, sigint_handler);	
	if (prev < 0) {
		Py_RETURN_FALSE;
	} 
	PySys_WriteStdout("waiting gdb... Press CTRL-C to proceed\n");
	while (1) {
		nanosleep(&req, 0);
		if (gdb_attached == 0)
			continue;
		else { 
			PySys_WriteStdout("gdb attached...\n"); 
			gdb_attached = 0;
			Py_RETURN_TRUE;
		}		
	}
}

static struct PyMethodDef debug_methods[] = { 
	{"pause", (PyCFunction)debug_pause4gdb,
		METH_VARARGS, debug_pause4gdb_doc},
	{NULL, NULL}
};


PyMODINIT_FUNC initdebug(void)
{
	PyObject *m;
	m = Py_InitModule("debug", debug_methods); 
	if (m == NULL)
		return;
}
