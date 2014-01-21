import gdb

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

gdb_O_object_type = gdb.lookup_type("Oobject")

def StringO_New_BP(gdb.BreakPoint):
    def __init__(self):
        super(gdb.BreakPoint, self).__init__(
                spec = "cStringIO.c:566",
                type = gdb.BPWATCHPOINT,
                wp_class = gdb.WP_READ
                ) 
    def stop(self):
        O_self = gdb_eval("self")
        address = str(O_self.address)
        O_object = O_self.cast(gdb_O_object_type)
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"])
                } 
        if address in O_s:
            if O_s[address]:
                O_s[address]["new"] = infos
            else:
                O_s[address] = {"new": infos}
        else:
            O_s[address] = {"new": infos}

def StringO_Dealloc_BP(gdb.BreakPoint):
    def __init__(self):
        super(gdb.BreakPoint, self).__init__(
                spec = "cStringIO.c:518",
                type = gdb.BPWATCHPOINT,
                wp_class = gdb.WP_READ
                )
    def stop(self):
        O_self = gdb_eval("self")
        address = str(O_self.address) 
        O_object = O_self.cast(gdb_O_object_type)
        infos = {
                "pos": str(O_object["pos"]),
                "string_size": str(O_object["string_size"]),
                "buf_size": str(O_object["buf_size"]),
                "softspace": str(O_object["softspace"])
                } 
        if address in O_s:
            if O_s[address]:
                O_s[address]["dealloc"] = infos
            else:
                O_s[address] = {"dealloc": infos}
        else:
            O_s[address] = {"dealloc": infos}
