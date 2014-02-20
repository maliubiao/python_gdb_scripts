import gdb

types_dict = {
        gdb.TYPE_CODE_PTR: "PTR",
        gdb.TYPE_CODE_ARRAY: "ARRAY",
        gdb.TYPE_CODE_STRUCT: "STRUCT",
        gdb.TYPE_CODE_UNION: "UNION",
        gdb.TYPE_CODE_ENUM: "ENUM",
        gdb.TYPE_CODE_FLAGS: "FLAGS",
        gdb.TYPE_CODE_FUNC: "FUNC",
        gdb.TYPE_CODE_INT: "INT",
        gdb.TYPE_CODE_VOID: "VOID",
        gdb.TYPE_CODE_RANGE: "RANGE",
        gdb.TYPE_CODE_STRING: "STRING",
        gdb.TYPE_CODE_ERROR: "ERROR",
        gdb.TYPE_CODE_METHOD: "METHOD",
        gdb.TYPE_CODE_METHODPTR: "METHODPTR",
        gdb.TYPE_CODE_REF: "REF",
        gdb.TYPE_CODE_CHAR: "CHAR",
        gdb.TYPE_CODE_BOOL: "BOOL",
        gdb.TYPE_CODE_COMPLEX: "COMPLEX",
        gdb.TYPE_CODE_TYPEDEF: "TYPEDEF",
        gdb.TYPE_CODE_NAMESPACE: "NAMESPACE",
        gdb.TYPE_CODE_INTERNAL_FUNCTION: "INTERNAL_FUNCTION"
        }

class PrintTypeCmd(gdb.Command):
    def __init__(self):
        super(PrintTypeCmd, self).__init__(
                name = "pt",
                command_class = gdb.COMMAND_DATA,
                completer_class = gdb.COMPLETE_SYMBOL)
    def invoke(self, argument, from_tty): 
        tp = gdb.lookup_type(str(argument))
        self.print_type("", tp) 
        #no members, return
        if tp.code == gdb.TYPE_CODE_TYPEDEF:
            tp = tp.strip_typedefs()
            print "real type of %s:" % str(tp)
            self.print_type("\t", tp)
        if tp.code not in (gdb.TYPE_CODE_STRUCT,
                gdb.TYPE_CODE_UNION,
                gdb.TYPE_CODE_ENUM):
            return 
        for n, v in tp.items():
            print "field, %s:" % n 
            self.print_type("\t", v.type)
            if v.type.code == gdb.TYPE_CODE_TYPEDEF:
                print "real type of %s:" % str(v.type)
                self.print_type("\t", v.type.strip_typedefs()) 
        
    def print_type(self, prefix, tp): 
        print prefix, " type", str(tp)
        try:
            print("%s code: %s" % (prefix, types_dict[tp.code]))
        except:
            pass
        try: 
            print("%s tag: %s" % (prefix,  tp.tag))
        except:
            pass
        try:
            print("%s sizeof: %s" % (prefix, tp.sizeof))
        except:
            pass

PrintTypeCmd()
