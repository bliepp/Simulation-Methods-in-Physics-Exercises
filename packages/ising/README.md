# Ising model simulation package
A python package for simulating the 2D Ising model.

## Features
* C++ extension written with pybind11
* Python drop-in replacement as fallback

## Installation
Since this package is not uploaded to PyPI, it cannot be installed with pip. Instead you have to compile and package it manually. That isn't dificult. Just execute the following build command in the current directory:
```
python[3] setup.py sdist bdist_wheel
```
Next, you have to install it locally via pip:
```
pip[3] install dist/ising*.whl
```
If you want to install using legacy package format (not wheel), use:
```
pip[3] install dist/ising*.tar.gz
```

## Updating
When a new version is in the repository and you rebuilt it using the setup.py you can simply run pip upgrade:
```
pip[3] install --upgrade ising
```
That works because after the first installation the source path is set. This becomes clear when having a look at `pip freeze`:
```
ising @ file://<destination-of-package>/ising-1.0.0-cp38-cp38-linux_x86_64.whl
# or
ising @ file://<destination-of-package>/ising-1.0.0.tar.gz
```
