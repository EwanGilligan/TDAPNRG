from setuptools import setup, find_packages
from Cython.Build import cythonize
from setuptools.extension import Extension

extensions = [Extension("vrips", ["src/randology/vrips.pyx"])]

setup(
    name='randology',
    version='0.2',
    packages=find_packages('src'),
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
        'ripser',
        'matplotlib',
        'plotly',
        'GF2Matrix'
    ],
    ext_modules=cythonize(extensions)
)
