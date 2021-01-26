#include "ising.hpp"

Ising::Ising(unsigned int L, bool init): L(L), L2(L*L){
    // heap allocated because of dynamic size
    this->lattice = new int[this->L2]; // don't forget deleting!
    this->generator = new std::mt19937();
    this->choose_element = new std::uniform_int_distribution<int>(0, this->L2);

    if (init){
        for (unsigned int i = 0; i < this->L2; i++){
            this->set_spin_by_index(i, 1);
        }
    }
}

Ising::~Ising(){
    delete this->lattice;
    delete this->generator;
    delete this->choose_element;
}

void Ising::randomize(){
    std::uniform_int_distribution<int> distribution(0, 1);
    for (unsigned int i = 0; i < this->L2; i++){
        this->set_spin_by_index(i, 2*distribution(*this->generator)-1);
    }
}

/*
 * INTERNAL HELPERS
 */
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

/*
 * GETTERS AND SETTERS
 */
void Ising::set_spin_by_index(int index, int value){
    // pointer arithmetic, equivalent of lattice[index]
    *(this->lattice + index) = value;
}

int Ising::get_spin_by_index(int index){
    // pointer arithmetic, equivalent of lattice[index]
    return *(this->lattice + index);
}

void Ising::set_spin(int i, int j, int value){
    this->set_spin_by_index(this->index(i, j), value);
}

int Ising::get_spin(int i, int j){
    return this->get_spin_by_index(this->index(i, j));
}

float Ising::flip_spin(int i, int j){
    float dE = this->local_energy(i, j);
    this->set_spin(i, j, -1*this->get_spin(i, j));
    dE = this->local_energy(i, j) - dE;
    return dE;
}

void Ising::set_lattice(std::vector<int> &v){
    if (v.size() != this->L2){
        throw py::index_error("New list must be L*L = " + std::to_string(this->L2) + " elements long");
    }
    for (size_t i = 0; i < v.size(); i++){
        *(this->lattice + i) = v[i];
    }
}

std::vector<int> Ising::get_lattice(){
    std::vector<int> v(this->lattice, this->lattice + this->L2);
    return v;//py::array(v.size(), v.data());
}

/*
 * COMPUTE PROPERTIES
 */
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