# TDAPNRG

Dependancies:
  * numpy
  * scipy
  * Cython
  * [scitkit-tda](https://scikit-tda.org/)
  * matplotlib.
  * scikit-learn
  * plotly
  * [GF2Matrix](https://github.com/EwanGilligan/GF2Matrix)

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

## Running with Docker

To build:
```bash
#path/to/TDAPNRG
sudo docker build --tag=randology .
```

To run as a single container, the `run.sh` shell script is provided for convenience. This handles the locations that files need to be mounted.
```bash
sudo bash ./run.sh relative/path/to/output_directory relative/path/to/config_file.json
```

For infomation on writing config files, [see config-syntax.md](config-syntax.md)
