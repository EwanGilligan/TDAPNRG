# TDAPNRG

Dependancies:
  * numpy
  * scipy
  * Cython
  * [scitkit-tda](https://scikit-tda.org/)
  * matplotlib.
  * scikit-learn

Cython should be the only one required before installation. Due to setuptools not specifying order of installation, you may need to install Cython before setup, which can be done by running

```bash
pip install Cython
```

This may also occur for numpy.

**Windows users:** If you are using a Windows machine, you will also need to install [MinGW](http://www.mingw.org) on your system.

To setup for development use:
```bash
# TDAPNRG/python-implementation/
python setup.py develop
```

Or for install:
```bash
# TDAPNRG/python-implementation/
python setup.py install
```
