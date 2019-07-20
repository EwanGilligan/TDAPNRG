from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

extensions = [Extension("vrips", ["src/randology/vrips.pyx"])]

setup(
    name='randology',
    version='0.1',
    packages=['randology', 'pnrg'],
    package_dir={'': 'src'},
    url='https://github.com/EwanGilligan/TDAPNRG',
    license='',
    author='eg207',
    author_email='eg207@st-andrews.ac.uk',
    description='',
    install_requires=[
        'numpy',
        'scipy',
        'Cython',
        'scikit-tda',
        'matplotlib',
        'plotly',
        'GF2Matrix'
    ],
    ext_modules=cythonize(extensions)
)
