#ifndef ISING_H
#define ISING_H
#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

class Ising {
public:
    Ising(unsigned int L, bool init = true);
    ~Ising();

    // setters and setters
    void set_spin(int i, int j, int value);
    int get_spin(int i, int j);
    void flip_spin(int i, int j);

    unsigned int get_L(){return this->L;}
    unsigned int get_L2(){return this->L2;}

    void set_lattice(std::vector<int> &v);
    std::vector<int> get_lattice();

    // compute properties
    float local_energy(int i, int j);
    float energy();
    float magnetization();

protected:
    int index(int i, int j);
    int get_i(int index);
    int get_j(int index);

    int *lattice; // heap allocated

//private:
    unsigned int L;
    unsigned int L2;
};

#endif
