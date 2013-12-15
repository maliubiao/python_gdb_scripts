#__del__ will be called when a instance object being dealloced.  
#__init__ will be called by PyInstance_New
#use function instance(class, [dict]) to create an instance
#   without calling its __init__ method 
#use function classobj(name, bases, dict) to create a class object manually.
#the tp_dealloc member of a instance object is function instance_dealloc
#Object/classobject.c:621 in CPython2.7.3
from types import ClassType as classobj
from types import InstanceType as instance
#for more? see types.py
#type is a builtin object, see Python/bltinmodule.c, Objects/typeobject.c
class C: 
    def __init__(self):
        print "__init__ called"
    def __del__(self):
        print "__del__ called"

def klass_init(self): 
    print "klass_init"
    
def klass_getname(self):
    return "klass name"

klass = {
        "__init__": klass_init,
        "name": klass_getname
        }
def func():
    C() 
    instance(C)
    print classobj("klass", (object, ), klass)().name()

func()
"""
result:
__init__ called
__del__ called
__del__ called
klass_init
klass name
"""


