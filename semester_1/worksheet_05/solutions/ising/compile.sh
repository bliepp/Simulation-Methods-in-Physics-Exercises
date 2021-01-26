PYBIND11=$(python -m pybind11 --includes)

echo "Compiling with $PYBIND11"

g++ -O3 -Wall -shared -std=c++20 -fPIC $PYBIND11 main.cpp ising.cpp -o ising_cpp.so