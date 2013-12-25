import gdb 
import pdb
import re
from pprint import pprint

simple_type = "bool int long float str complex bytearray None"
container_type = "list tuple dict code"

class PyObjectCmd(gdb.Command):
    def __init__(self):
        super(PyObjectCmd, self).__init__(
                name="pyshow",
                command_class = gdb.COMMAND_DATA,
                completer_class =gdb.COMPLETE_SYMBOL
                ) 
    def invoke(self, argument, from_tty):
        args = gdb.string_to_argv(argument)
        if len(args) != 1:
            raise gdb.GdbError("usage: pyshow PyObject *")
        p = args[0]
        pt = str(gdb.parse_and_eval(p).type)
        if not re.match(r"Py.*Object \*", pt):
            raise gdb.GdbError("only accept pointer whose type is struct PyObject *")
        if str(gdb.parse_and_eval(p)) == "0x0":
            return "NULL Pointer" 
        tp_name = self.objtype(p) 
        if not tp_name:
            print "failed to identify object"
            return
        if tp_name in simple_type:
            pprint(self.handle_basetype(tp_name, p))
        elif tp_name in container_type: 
            pprint(self.handle_container(tp_name, p)) 
        else: 
            print "unknown type %s" % tp_name 

    def objtype(self, p):
        try:  
            obj = gdb.parse_and_eval("*(%s->ob_type)" % p)
            tp_name = obj['tp_name'].string() 
        except Exception as e: 
            return None
        return tp_name 

    def handle_basetype(self, tp_name, p): 
        basetype_dict = {"type": tp_name}
        if tp_name in "bool int long":
            obj = gdb.parse_and_eval("*(PyIntObject *)(%s)" % p) 
            basetype_dict["value"] = str(obj["ob_ival"]) 
        elif tp_name == "float":
            obj = gdb.parse_and_eval("*(PyFloatObject *)(%s)" % p)
            basetype_dict["value"] = str(obj["ob_fval"])
        elif tp_name == "str": 
            obj = gdb.parse_and_eval("*(PyStringObject *)(%s)" % p)
            inferior = gdb.selected_inferior()
            ob_size = int(str(obj["ob_size"]))
            value = inferior.read_memory(int(str(obj["ob_sval"].address), 16), ob_size) 
            basetype_dict["value"] = str(value)
            basetype_dict["length"] = ob_size
        elif tp_name == "bytearray":
            obj = gdb.parse_and_eval("*(PyByteArrayObject *)(%s)" % p)
            basetype.update({
                "value": obj["ob_bytes"].string(),
                "ob_alloc": obj["ob_alloc"].string(),
                "ob_exports": obj["ob_exports"].string()
                }) 
        elif tp_name == "complex":
            obj = gdb.parse_and_eval("*(PyComplexObject *)(%s)" % p)
            basetype_dict["real"] = str(obj["cval"]["real"])
            basetype_dict["image"] = str(obj["cval"]["imag"])
        return basetype_dict                    

    def handle_container(self, tp_name, p): 
        container_dict = {"type": tp_name} 
        if tp_name == "list":
            obj = gdb.parse_and_eval("*(PyListObject *)(%s)" % p)
            container_dict.update({
                "allocated": str(obj["allocated"]),
                "ob_size": str(obj["ob_size"])
                })
            objs = []
            for index in range(int(str(obj["ob_size"]))):
                item = "(((PyListObject *)%s)->ob_item[%d])" % (p, index)
                tp_name = self.objtype(item)
                if tp_name in "bool int long float str complex bytearray None":
                    objs.append(self.handle_basetype(tp_name, p))
                elif tp_name in "list tuple dict":
                    objs.append({"type": tp_name, "value": str(obj.address)}) 
            container_dict["objects"] = objs
        if tp_name == "tuple": 
            obj = gdb.parse_and_eval("*(PyTupleObject *)(%s)" % p)
            container_dict.update({
                "size": int(str(obj["ob_size"]))
                })
            objs = []
            for index in range(container_dict["size"]):
                item = "(((PyTupleObject *)%s)->ob_item[%d])" % (p, index)
                tp_name = self.objtype(item) 
                objs = []
                if tp_name in simple_type:
                    objs.append(self.handle_basetype(tp_name, p))
                elif tp_name in container_type:
                    objs.append({"type": tp_name, "value": str(obj.address)}) 
            container_dict["objects"] = objs
        if tp_name == "dict":
            obj = gdb.parse_and_eval("*(PyDictObject *)(%s)" % p)
            container_dict.update({
                "ma_fill": int(str(obj["ma_fill"])),
                "ma_used": int(str(obj["ma_used"])),
                "ma_mask": int(str(obj["ma_mask"]))
                }) 
            objs = [] 
            for index in range(container_dict["ma_mask"]): 
                keyitem = "(((PyDictObject *)%s)->ma_table[%d]->me_key)" % (p, index) 
                valueitem = "(((PyDictObject *)%s)->ma_table[%d]->me_value)" % (p, index) 
                #empty
                key_tp_name = self.objtype(keyitem)
                if not key_tp_name:
                    continue
                value_tp_name=  self.objtype(valueitem) 
                try:
                    if key_tp_name in simple_type:
                        key = self.handle_basetype(key_tp_name, keyitem) 
                    elif key_tp_name in container_type:
                        key = {"type": key_tp_name, "value": str(obj.address)}
                    if value_tp_name in simple_type:
                        objs.append((key, self.handle_basetype(value_tp_name, valueitem)))
                    elif key_tp_name in container_type:
                        objs.append((key, {"type": value_tp_name, "value": str(obj.address)}))
                except Exception, err:
                    print objs
                    print index 
            container_dict["objects"] = objs 
        if tp_name == "code":
            obj = gdb.parse_and_eval("*(PyDictObject *)(%s)" % p)
        return container_dict 

PyObjectCmd()                 

