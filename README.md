# Simulation-Methods-in-Physics-Exercises
## Disclaimer
The code in this repository is not licensed under any specific license for legal reasons. Some of the code was provided by the tutors of the Institute for Computational Physics (ICP) of the University of Stuttgart. The website of the lecture can be found [here for the winter semester](https://www2.icp.uni-stuttgart.de/~icp/Simulation_Methods_in_Physics_I_WS_2020/2021). The tutorial files is almost identical to the one from the [previous year](https://www2.icp.uni-stuttgart.de/~icp/Simulation_Methods_in_Physics_I_WS_2019/2020). All other code may be used for personal use.

Please keep in mind that copying the code directly is most likely prohibited by your tutor.

## Setup
This project requires Python 3 and a valid C/C++ compiler. It is recommended to use the same compiler the python executables were created with (Linux: GCC, Windows: MSVC, macOS: Clang). When running the python interpreter in interactive mode the required compiler package is usually printed to the console (example for linux):
```
Python 3.9.1 (default, Dec 13 2020, 11:55:53) 
[GCC 10.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
If a different compiler is used C/C++ extensions for python might not be compatible. Please keep in mind that numba might not be compatible with the latest python version. Try using the previous minor release if it does not work correctly (install from your repositories).

It is highly recommended to start a new virtual environment for this project (current repository cloned into `exercises`):
```bash
exercises $ python -m venv .venv
exercises $ source .venv/bin/activate # may differ on other platforms
(.venv ) exercises $
```

Now install the required packages using pip:
```bash
(.venv) exercises $ pip install -r requirements.txt
```

Now install the custom packages inside the directory `packages`. A tutorial on how to install them into your local virtual environment can be found in there. Usually it works this way:
```bash
(.venv) exercises/packages/ising $ python setup.py bdist_wheel
(.venv) exercises/packages/ising $ pip install dist/*.whl
```