#! /usr/bin/env python
import os
import time
import signal

pypath = "/data/project/py/Python-2.7.3/python"
pid = os.fork()

if not pid:
    os.execvp(pypath, [pypath, "test.py"])

tmp_file = "gdb_commands"
f = open(tmp_file, "w")
f.write("attach %s\nfile %s\nsource %s\ncontinue\n" % (str(pid), pypath, "gdb_StringIO.py"))
f.close() 

if not os.fork():
    os.execve("/usr/bin/gdb", ["gdb", "-x", tmp_file], os.environ) 

time.sleep(0.5)
#send SIGUSR1 to python
try:
    os.kill(pid, signal.SIGUSR1)
except OSError:    
    pass
#wait gdb to quit
os.wait()
#kill python
try:
    os.kill(pid, signal.SIGKILL) 
except OSError:
    pass
os.wait()
os.remove(tmp_file)

