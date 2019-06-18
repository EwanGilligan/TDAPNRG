from setuptools import setup

setup(
    name='python-implementation',
    version='0.1',
    packages=[],
    package_dir={'': 'src'},
    url='https://github.com/EwanGilligan/TDAPNRG',
    license='',
    author='eg207',
    author_email='eg207@st-andrews.ac.uk',
    description='',
    setup_requires=[
        'numpy',
        'scipy',
        'Cython',
        'scikit-tda',
        'matplotlib',
    ]
)
