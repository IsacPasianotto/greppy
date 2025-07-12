from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "utils/search_cython.pyx",
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False,
            'nonecheck': False,
            'cdivision': True,
        },
        annotate=True,
    ),
    zip_safe=False,
)
