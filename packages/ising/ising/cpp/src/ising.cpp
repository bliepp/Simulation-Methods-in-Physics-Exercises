#include "ising.hpp"
#include <algorithm>
#include <numeric>
#include <cmath>
#include <iostream>

Ising::Ising(unsigned int L, bool init): L(L), L2(L*L){
    // heap allocated because of dynamic size
    this->lattice = new int[this->L2]; // don't forget deleting!
    this->generator = new std::mt19937();

    if (init){
        for (unsigned int i = 0; i < this->L2; i++){
            this->set_spin_by_index(i, 1);
        }
    }
}

Ising::~Ising(){
    delete this->lattice;
    delete this->generator;
}

Ising& Ising::randomize(){
    std::uniform_int_distribution<int> distribution(0, 1);
    for (unsigned int i = 0; i < this->L2; i++){
        this->set_spin_by_index(i, 2*distribution(*this->generator)-1);
    }
    return *this;
}

/*
 * INTERNAL HELPERS
 */
int Ising::index(int i, int j){
    // not modulo, it's a remainder!
    i = i % static_cast<int>(this->L); // casting because L is unsigned
    j = j % static_cast<int>(this->L); // overiding local instance of variable

    return i * this->L + j
        + (i < 0)*this->L*this->L // correcting remainder to modulo for i
        + (j < 0)*this->L; // correcting remainder to modulo for j
}

int Ising::get_i(unsigned int index){
    return index / this->L; // int division
}

int Ising::get_j(unsigned int index){
    return index % this->L; // int division
}

/*
 * GETTERS AND SETTERS
 */
int Ising::get_spin_by_index(int index){
    index = index % static_cast<int>(this->L2); // remainder, casting because L2 is unsigned
    index += (index < 0)*this->L2; // correction to modulo

    // pointer arithmetic, equivalent of lattice[index]
    return *(this->lattice + index);
}

Ising& Ising::set_spin_by_index(int index, int value){
    index = index % static_cast<int>(this->L2); // remainder, casting because L2 is unsigned
    index += (index < 0)*this->L2; // correction to modulo

    // pointer arithmetic, equivalent of lattice[index]
    *(this->lattice + index) = value;
    return *this;
}

int Ising::get_spin(int i, int j){
    return this->get_spin_by_index(this->index(i, j));
}

Ising& Ising::set_spin(int i, int j, int value){
    this->set_spin_by_index(this->index(i, j), value);
    return *this;
}

double Ising::flip_spin(int i, int j){
    double dE = this->local_energy(i, j);
    this->set_spin(i, j, -1*this->get_spin(i, j));
    dE = this->local_energy(i, j) - dE;
    return dE;
}

std::vector<int> Ising::get_lattice(){
    std::vector<int> v(this->lattice, this->lattice + this->L2);
    return v;
}

void Ising::set_lattice(std::vector<int> &v){
    if (v.size() != this->L2){
        throw std::out_of_range("New list must be L*L = " + std::to_string(this->L2) + " elements long");
    }
    for (size_t i = 0; i < v.size(); i++){
        this->set_spin_by_index(i, v[i]);
    }
}

/*
 * COMPUTE PROPERTIES
 */
double Ising::local_energy(int i, int j){
    return this->get_spin(i,j)*(
        this->get_spin(i-1, j)
        + this->get_spin(i+1, j)
        + this->get_spin(i, j-1)
        + this->get_spin(i, j+1)
    );
}

double Ising::energy(){
    double total = 0;
    for (unsigned int i = 0; i < this->L; i++){
    for (unsigned int j = 0; j < this->L; j++){
        total += this->local_energy(i, j);
    }
    }
    return 0.5 * total;
}

double Ising::magnetization(){
    double mu = 0;
    for (unsigned int i = 0; i < this->L2; i++){
        mu += this->get_spin_by_index(i);
    }
    return mu/this->L2;
}

/*
 * SIMULATE
 */
std::vector<double> Ising::metropolis(unsigned int steps, double beta){ //std = sexually transmitted desease
    std::uniform_real_distribution<float> r_dist(0.0, 1.0);
    std::uniform_int_distribution<int> choose_element(0, this->L2);

    double accepted = 0.0, e = 0.0, m = 0.0;

    double E = this->energy();
    for (unsigned int step = 0; step < steps; step++){
        float r = r_dist(*this->generator);
        int index = choose_element(*this->generator);
        int i = this->get_i(index), j = this->get_j(index);

        double dE = this->flip_spin(i, j);
        bool condition = r < std::min(1.0, std::exp(-beta*dE));

        accepted += condition;
        E += dE*condition;


        if (!condition){
            this->flip_spin(i, j); // flip back to previous state
        }

        // no exp(-beta * E), because p = exp(-beta*E)/Z is chosen
        // see https://en.wikipedia.org/wiki/Monte_Carlo_method_in_statistical_physics#Importance_sampling
        e += E;
        m += std::abs(this->magnetization());
    }
    return std::vector<double>({accepted/steps, e/steps/this->L2, m/steps});
}
