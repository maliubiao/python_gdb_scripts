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

domain_dict = {
        "undef": gdb.SYMBOL_UNDEF_DOMAIN,
        "var": gdb.SYMBOL_VAR_DOMAIN,
        "struct": gdb.SYMBOL_STRUCT_DOMAIN,
        "label": gdb.SYMBOL_VARIABLES_DOMAIN,
        #"func": gdb.SYMBOL_FUNCTION_DOMAIN,
        "types": gdb.SYMBOL_TYPES_DOMAIN
        }


addrs_dict = {
        gdb.SYMBOL_LOC_UNDEF: "undef",
        gdb.SYMBOL_LOC_CONST: "const int",
        gdb.SYMBOL_LOC_STATIC: "fixed addr",
        gdb.SYMBOL_LOC_REGISTER: "register",
        gdb.SYMBOL_LOC_ARG: "argument",
        gdb.SYMBOL_LOC_REF_ARG: "ref argument",
        gdb.SYMBOL_LOC_REGPARM_ADDR: "regparm",
        gdb.SYMBOL_LOC_LOCAL: "local",
        gdb.SYMBOL_LOC_TYPEDEF: "typdef",
        gdb.SYMBOL_LOC_BLOCK: "block",
        gdb.SYMBOL_LOC_CONST_BYTES: "byte seqs",
        gdb.SYMBOL_LOC_UNRESOLVED: "unresolved",
        gdb.SYMBOL_LOC_OPTIMIZED_OUT: "optimized out",
        gdb.SYMBOL_LOC_COMPUTED: "computed location" 
        } 


