import gdb
import pdb
import sys
from pprint import pprint

class ReadMemory(gdb.Command):
    def __init__(self):
        super(ReadMemory, self).__init__(
                name="rd",
                command_class=gdb.COMMAND_DATA,
                completer_class = gdb.COMPLETE_SYMBOL
                )
    def invoke(self, argument, from_tty):
        args = gdb.string_to_argv(argument)
        if len(args) != 2:
            raise gdb.GdbError("usage: rd ptr length")
        p1 = args[0]
        try:
            l = int(args[1])
        except:
            raise gdb.GdbError("usage ptr length") 
        ptr1 = str(gdb.parse_and_eval(p1).type)
        obj = gdb.parse_and_eval("*%s" % p1)
        if not "*" in ptr1:
            raise gdb.GdbError("%s is not a ptr" % p1)
        inferior = gdb.selected_inferior() 
        value = inferior.read_memory(int(str(obj.address), 16), l) 
        k = str(value)
        #a gdb bug, have to use pprint instead of print
        pprint("address: %s" % (str(obj.address)))
        for i in range(0, len(k), 16): 
            pprint("{:<11} {:<11}".format(k[i:i+8], k[i+8:i+16])) 
     
ReadMemory()

