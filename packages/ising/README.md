# Ising model simulation package
A python package for simulating the 2D Ising model.

## Features
* C++ extension written with pybind11
* Python drop-in replacement as fallback

The C++ part of the code has no dependency on `pybind11.h` or the `Python.h` (except for the python bindings in `bindings.cpp`, obviously). This means that you are not limited to use python and may compile parts of this package into your C++ program, too.

## Reqirements
Since you need to compile this package yourself pybind11 is neccessary. As a build system `setuptools` in `setup.py` is used, therefore requiring pybind11 beeing installed via pip (`pip install pybind11`). For the python fallback numpy is required (`pip install numpy`).

## Installation
Since this package is not uploaded to PyPI, it cannot be installed with pip directly. Instead you have to compile and package it manually. That isn't dificult. Just execute the following build command in the current directory and install it locally with pip (with python/pip beeing python3/pip3):
```bash
(.venv) ising $ python setup.py bdist_wheel
(.venv) ising $ pip install dist/ising*.whl
```

If you want to install using legacy package format instead of the wheel packaging format, use:
```bash
(.venv) ising $ python setup.py sdist
(.venv) ising $ pip install dist/ising*.tar.gz
```

## Updating
When a new version is in the repository and you rebuilt it using the `setup.py` you can simply run pip again:
```bash
(.venv) ising $ pip install dist/ising*.whl
# or
(.venv) ising $ pip install dist/ising*.tar.gz
```
If that does not work try to specify the correct file and don't use the wildcard.
