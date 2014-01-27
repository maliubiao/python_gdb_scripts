import cStringIO
import time
import signal

gdb = False

def wait_gdb(sig, frame):
    global gdb    
    gdb = True

signal.signal(signal.SIGUSR1, wait_gdb)

while True:
    time.sleep(0.5)
    if gdb:
        break

k = cStringIO.StringIO()
k.write("hello")
del k
