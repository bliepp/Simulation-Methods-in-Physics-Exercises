#!/usr/bin/env python
from glob import glob
import setuptools

from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = "1.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()


ext_modules = [
    Pybind11Extension("ising.cpp.__ising",
        sorted(glob("ising/cpp/src/*.cpp")),
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', __version__)],
        ),
]

setuptools.setup(
    name="ising",
    version=__version__,
    author="bliepp",
    #author_email="author@example.com",
    description="C++ and Python implementation of the Ising model for simulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bliepp/Simulation-Methods-in-Physics-Exercises",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    
    # pybind setup
    ext_modules=ext_modules,
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
