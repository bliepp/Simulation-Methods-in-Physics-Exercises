#ifndef ISING_H
#define ISING_H
#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>
#include <vector>
#include <random>

namespace py = pybind11;

class Ising {
public:
    Ising(unsigned int L, bool init = true);
    ~Ising();

    Ising& randomize();

    // getters and setters
    unsigned int get_L(){return this->L;}
    unsigned int get_L2(){return this->L2;}

    int get_spin_by_index(int index);
    Ising& set_spin_by_index(int index, int value);
    int get_spin(int i, int j);
    Ising& set_spin(int i, int j, int value);
    double flip_spin(int i, int j);

    std::vector<int> get_lattice();
    void set_lattice(std::vector<int> &v);

    // compute properties
    double local_energy(int i, int j);
    double energy();
    double magnetization();

    // simulate
    std::vector<double> metropolis(unsigned int steps, double beta = 0.0);

protected:
    // internal helpers
    int index(int i, int j);
    int get_i(unsigned int index);
    int get_j(unsigned int index);

    int *lattice; // heap allocated

//private:
    unsigned int L;
    unsigned int L2;

    std::mt19937 *generator;
};

#endif
