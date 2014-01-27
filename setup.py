#! /usr/bin/env python
from distutils.core import setup, Extension

m = Extension("internal",
        sources=["internal.c"],
        extra_compile_args=["-Wall", "-Werror" ])

setup(name = "internal", description = "gdb helper",
        ext_modules = [m])

