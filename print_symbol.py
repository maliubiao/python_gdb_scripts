import gdb
import sys
import os.path

sys.path.append(os.path.dirname(__file__))

from gdb_shared import domain_dict, types_dict, addrs_dict


class PrintSymbolCmd(gdb.Command):
    def __init__(self):
        super(PrintSymbolCmd, self).__init__(
                name="print_symbol",
                command_class = gdb.COMMAND_DATA,
                completer_class = gdb.COMPLETE_SYMBOL
                )

    def print_usage(self):
        print "usage: print_symbol symbol [domain=[undef,var,struct,label,vars,func,types]]" 

    def print_symbol(self, symbol):
        print "=============="
        print "type %s" % types_dict[symbol.type.code] 
        print "in file %s:%d" % (symbol.symtab.fullname(), symbol.line)
        print "name: %s, linkage_name: %s" % (symbol.name, symbol.linkage_name)
        print "addr type: %s" % addrs_dict[symbol.addr_class]
        print "=============="

    def invoke(self, argument, from_tty):
        args = gdb.string_to_argv(argument)
        if len(args) < 1: 
            self.print_usage()
            return
        domain = None 
        for arg in args:
            if "domain=" in arg: 
                domain = arg.split("=")[1] 
        if domain:
            symbol, _ = gdb.lookup_symbol(args[0], gdb.newest_frame().block(), domain_dict[domain]) 
        else:
            symbol, _ = gdb.lookup_symbol(args[0])
        if not symbol:
            print "not found in this frame"
            return
        self.print_symbol(symbol)                 

PrintSymbolCmd()
