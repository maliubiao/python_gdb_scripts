#! /usr/bin/env python
from distutils.core import setup, Extension

m = Extension("debug",
        sources=["debug.c"],
        extra_compile_args=["-Wall", "-Werror" ])

setup(name = "debug", description = "gdb helper",
        ext_modules = [m])

