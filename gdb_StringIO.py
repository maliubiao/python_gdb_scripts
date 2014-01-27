import gdb
import pdb
"""
SPECS
/* Entries related to the type of user set breakpoints.  */
static struct pybp_code pybp_codes[] =
{
  { "BP_NONE", bp_none},
  { "BP_BREAKPOINT", bp_breakpoint},
  { "BP_WATCHPOINT", bp_watchpoint},
  { "BP_HARDWARE_WATCHPOINT", bp_hardware_watchpoint},
  { "BP_READ_WATCHPOINT", bp_read_watchpoint},
  { "BP_ACCESS_WATCHPOINT", bp_access_watchpoint},
  {NULL} /* Sentinel.  */
};

gdb.BreakPoint.__init__
  static char *keywords[] = { "spec", "type", "wp_class", "internal", NULL }; 
  if (! PyArg_ParseTupleAndKeywords (args, kwargs, "s|iiO", keywords,
				     &spec, &type, &access_type, &internal))

"""
O_s = {}

gdb_eval = gdb.parse_and_eval 

class StringO_New_BP(gdb.Breakpoint):
    def __init__(self):
        super(StringO_New_BP, self).__init__(
                spec = "cStringIO.c:566",
                type = gdb.WP_READ,
                wp_class = gdb.BP_READ_WATCHPOINT 
                ) 
        
    def stop(self):
        O_object = gdb_eval("self")
        address = str(O_object.address) 
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"]), 
                } 
        if address in O_s:
            if O_s[address]:
                O_s[address]["new"] = infos
            else:
                O_s[address] = {"new": infos}
        else:
            O_s[address] = {"new": infos}
        O_s[address]["object"] = O_object
        print "newO_obj", O_s[address]

class StringO_Write_BP(gdb.Breakpoint):
    def __init__(self):
        super(StringO_Write_BP, self).__init__(
                spec = "cStringIO.c:437",
                type = gdb.WP_READ,
                wp_class = gdb.BP_READ_WATCHPOINT
                )
    def stop(self):
        O_object = gdb_eval("self")
        address = str(O_object.address)
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"]), 
                } 
        if address in O_s:
            O_s[address]["after_write"] = infos 
        print "after_write", O_s[address]

class StringO_Writelines_BP(gdb.Breakpoint):
    def __init__(self):
        super(StringO_Writelines_BP, self).__init__(
                spec = "cStringIO.c:487",
                type = gdb.WP_READ,
                wp_class = gdb.BP_READ_WATCHPOINT
                )
    def stop(self):
        O_object = gdb_eval("self")
        address = str(O_object.address)
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"]), 
                } 
        if address in O_s:
            O_s[address]["after_writelines"] = infos 
        print "after_writelines", O_s[address]
        

class StringO_Dealloc_BP(gdb.Breakpoint):
    def __init__(self):
        super(StringO_Dealloc_BP, self).__init__(
                spec = "cStringIO.c:518",
                wp_class = gdb.BP_WATCHPOINT,
                type = gdb.WP_READ
                )
        
    def stop(self):
        O_object = gdb_eval("self")
        address = str(O_object.address) 
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"]),
                "object": O_object
                } 
        if address in O_s:
            if O_s[address]:
                O_s[address]["dealloc"] = infos
            else:
                O_s[address] = {"dealloc": infos}
        else:
            O_s[address] = {"dealloc": infos}
        print "dealloc", O_s[address]

StringO_New_BP()
StringO_Dealloc_BP()
StringO_Write_BP()
StringO_Writelines_BP()
