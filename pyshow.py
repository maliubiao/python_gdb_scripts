import gdb
import re

class PyObjectCmd(gdb.Command):
    def __init__(self):
        super(PyObjectCmd, self).__init__(
                name="pyshow",
                command_class = gdb.COMMAND_DATA,
                completer_class = gdb.COMPLETE_SYMBOL, 
                ) 
        self.init_data()

    def init_data(self):
        self.reculevel = 0        
        self.pointer = "" 
        self.outdata = {
                "type": None,
                "objects": []
                } 
        self.s = self.outdata['objects'] 
        
    def invoke(self, argument, from_tty):
        args = gdb.string_to_argv(argument)
        if len(args) != 1:
            raise gdb.GdbError("usage: pyshow PyObject *") 
        pointer_type = str(gdb.parse_and_eval(args[0]).type) 
        if not re.match(r"Py.*Object \*", pointer_type):
            raise gdb.GdbError("error: argument is not a PyObject *") 

        self.handle_type(self.decide_type(args[0]))
        self.pretty_print()
        self.init_data()

    def decide_type(self, pointer): 
        try:
            if str(gdb.parse_and_eval(pointer)) == "0x0": 
                return "None"
            target = "*(%s->ob_type)" % pointer 
            obj = gdb.parse_and_eval(target)
            self.pointer = pointer
            return obj['tp_name'].string()
        except Exception as e:
            raise gdb.GdbError(str(e))

    def handle_type(self, tp_name): 
        if tp_name in "bool int long":
            obj = gdb.parse_and_eval("*(PyIntObject *)(%s)"
                                           % self.pointer
                                           )
            self.s.append(self.handle_int(tp_name, obj))

        if tp_name == "float":
            obj = gdb.parse_and_eval("*(PyFloatObject *)(%s)"
                                           % self.pointer
                                           )
            self.s.append(self.handle_float(tp_name, obj))

        elif tp_name == "str":
            self.s.append(self.handle_string(tp_name, self.pointer))

        elif tp_name == "complex":
            obj = gdb.parse_and_eval("*(PyComplexObject *)(%s)"
                                           % self.pointer
                                           )
            self.s.append(self.handle_string(tp_name, obj))

        elif tp_name == "bytearray":
            obj = gdb.parse_and_eval("*(PyByteArrayObject *)(%s)"
                                           % self.pointer
                                           )
            self.s.append(self.handle_string(tp_name, obj))

        elif tp_name == "list":
            obj = gdb.parse_and_eval("*(PyListObject *)(%s)"
                                           % self.pointer
                                           )
            if self.reculevel > 0: 
                self.s.append(
                        {
                            "type": "tuple",
                            "value": str(obj.address), 
                        }
                    ) 
                return 
            self.s.append(self.handle_list(tp_name, self.pointer, obj)) 

        elif tp_name == "tuple":
            obj = gdb.parse_and_eval("*(PyTupleObject *)(%s)"
                        % self.pointer
                    )
            if self.reculevel > 0: 
                self.s.append(
                        {
                            "type": "tuple",
                            "value": str(obj.address), 
                        }
                    ) 
                return 

            self.s.append(self.handle_tuple(tp_name, self.pointer, obj)) 

        elif tp_name == "dict":
            obj = gdb.parse_and_eval("*(PyDictObject *)(%s)"
                        % self.pointer
                    )
            if self.reculevel > 0:
                self.s.append(
                        {
                            "type": "dict",
                            "value": str(obj.address), 
                        }
                    ) 
                return 

            self.s.append(self.handle_dict(tp_name, self.pointer, obj)) 

        elif tp_name == "None":
            self.s.append(None)

        else:
            self.s.append("unknown type %s" % tp_name)

    def pretty_print(self):
        tp_name = self.outdata['type'] 
        if tp_name == None:
            print self.s[0]
        elif tp_name in "tuple list":
            print self.outdata['listdata']
            for i,v in enumerate(self.s[:-1]):
                print "[%s]: %s" % (i, str(v)) 
        elif tp_name == "dict": 
            print self.outdata['dictdata']
            i = 0 
            total = len(self.s)/2
            while i < total:
                print "key: %s" % str(self.s[i]) 
                print "value: %s" % str(self.s[i+1])
                i = i + 2

    def handle_int(self, tp_name, obj):
        return {
                 "type": tp_name,
                 "value": str(obj['ob_ival'])
               } 

    def handle_float(self, tp_name, obj):
        return {
                 "type": tp_name,
                 "value": str(obj['ob_fval'])
               }

    def handle_complex(self, tp_name, obj):
        return {
                 "type": tp_name,
                 "real": str(obj['cval']['real']),
                 "imag": str(obj['cval']['imag']) 
               }

    def handle_string(self, tp_name, arg): 
        obj = gdb.parse_and_eval("*(PyStringObject *)(%s)" % arg) 
        value = gdb.parse_and_eval("(char *)(((PyStringObject *)(%s))->\
                                    ob_sval)" % arg) 
        return {
                 "type": tp_name,
                 "value": value.string(),
                 "length": str(obj['ob_size'])
               }

    def handle_bytearray(self, tp_name, obj):
        return {
                 "type": tp_name,
                 "value": obj['ob_bytes'].string(),
                 "ob_alloc": str(obj['ob_alloc']),
                 "ob_exports": str(obj['ob_exports'])
               } 

    def handle_tuple(self, tp_name, pointer, obj): 
        self.outdata['type'] = tp_name
        list_data = { 
                "type": tp_name,
                "size": str(obj['ob_size']), 
                } 
        self.outdata['listdata'] = list_data
        total = int(str(obj['ob_size']))
        for i in range(0, total): 
            tp_str =  "(((PyTupleObject *)%s)->ob_item[%d])" % (pointer, i) 
            self.handle_type(self.decide_type(tp_str))  
        self.reculevel = 1     
 

    def handle_list(self, tp_name, pointer, obj): 
        self.outdata['type'] = tp_name
        list_data = { 
                "type": tp_name,
                "allocated": str(obj['allocated']), 
                "ob_size": str(obj['ob_size'])
                } 
        self.outdata['listdata'] = list_data
        self.reculevel = 1     
        total = int(str(obj['ob_size']))
        for i in range(0, total): 
            tp_str =  "(((PyListObject *)%s)->ob_item[%d])" % (pointer, i) 
            self.handle_type(self.decide_type(tp_str))


    def handle_dict(self, tp_name, pointer, obj): 
        self.outdata['type'] = tp_name
        dict_data = {
                "type": tp_name,
                "ma_fill": str(obj['ma_fill']),
                "ma_used": str(obj['ma_used'])
                } 
        self.outdata['dictdata'] = dict_data
        total = int(dict_data['ma_used'])
        self.reculevel = 1
        for i in range(0, total):
            tpkey_str = "(((PyDictObject *)%s)->ma_table[%d]->me_key)"\
                            % (pointer, i)
            tpvalue_str = "(((PyDictObject *)%s)->ma_table[%d]->me_value)"\
                            % (pointer, i) 
            self.handle_type(self.decide_type(tpkey_str))
            self.handle_type(self.decide_type(tpvalue_str)) 

PyObjectCmd()
