#include "ising.hpp"

Ising::Ising(unsigned int L, bool init): L(L), L2(L*L){
    // heap allocated because of dynamic size
    this->lattice = new int[this->L2]; // don't forget deleting!
    if (init){
        for (unsigned int i = 0; i < this->L2; i++){
            *(this->lattice + i) = 1;
        }
    }
}

Ising::~Ising(){
    delete this->lattice;
}

int Ising::index(int i, int j){
    i = i % this->L; // not modulo, it's a remainder!
    j = j % this->L; // overiding local instance of variable

    return i * this->L + j
        + (i < 0)*this->L*this->L // correcting remainder to modulo for i
        + (j < 0)*this->L; // correcting remainder to modulo for j
}

int Ising::get_i(int index){
    return index / this->L; // int division
}

int Ising::get_j(int index){
    return index % this->L; // int division
}

// Getter and Setter
void Ising::set_spin(int i, int j, int value){
    // pointer arithmetic, equivalent of lattice[index]
    *(this->lattice + this->index(i,j)) = value;
}

int Ising::get_spin(int i, int j){
    // pointer arithmetic, equivalent of lattice[index]
    return *(this->lattice + this->index(i,j));
}

void Ising::flip_spin(int i, int j){
    this->set_spin(i, j, -1*this->get_spin(i, j));
}

void Ising::set_lattice(std::vector<int> &v){
    if (v.size() != this->L2){
        throw py::index_error("New list must be L*L = " + std::to_string(this->L2) + " elements long");
    }
    for (unsigned int i = 0; i < v.size(); i++){
        *(this->lattice + i) = v[i];
    }
}

std::vector<int> Ising::get_lattice(){
    std::vector<int> v(this->lattice, this->lattice + this->L2);
    return v;//py::array(v.size(), v.data());
}

// compute properties
float Ising::local_energy(int i, int j){
    return this->get_spin(i,j)*(
        this->get_spin(i-1, j)
        + this->get_spin(i+1, j)
        + this->get_spin(i, j-1)
        + this->get_spin(i, j+1)
    );
}

float Ising::energy(){
    float total = 0;
    for (unsigned int i = 0; i < this->L; i++){
    for (unsigned int j = 0; j < this->L; j++){
        total += this->local_energy(i, j);
    }
    }
    return 0.5 * total;
}

float Ising::magnetization(){
    float mu = 0;
    for (unsigned int i = 0; i < this->L; i++){
    for (unsigned int j = 0; j < this->L; j++){
        mu += this->get_spin(i, j);
    }
    }
    return mu/this->L2;
}