from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("poly.pyx"),
    include_dirs=[numpy.get_include()]
)

# [build-system]
requires = ["setuptools", "wheel", "Cython"]
# python setup.py build_ext --inplace
