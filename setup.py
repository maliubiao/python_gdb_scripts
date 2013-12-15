#! /usr/bin/env python
from distutils.core import setup, Extension

m = Extension("internel",
        sources=["internel.c"],
        extra_compile_args=["-Wall", "-Werror" ])

setup(name = "internel", description = "gdb helper",
        ext_modules = [m])

