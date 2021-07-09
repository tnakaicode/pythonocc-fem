
#!/usr/bin/env python3
import numpy
import setuptools
import site
#from distutils.core import setup, Extension
from Cython.Distutils import build_ext
from numpy.distutils.core import setup, Extension

site.ENABLE_USER_SITE = True

setup(
    #cmdclass = {'build_ext': build_ext},
    ext_modules=[
        Extension(name="pyprod", sources=["prod.f90"]),
        Extension(name="badprec", sources=["badprec.f90"]),
    ],
    include_dirs=[numpy.get_include()]
)

# pip install fortran-language-server
# python setup_example.py build_ext --inplace
