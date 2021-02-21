#ifndef ISING_HPP
#define ISING_HPP

#include <algorithm>
#include <cassert>
#include <random>
#include <iostream>
#include <vector>

// Negative numerb proof modulo
template <typename T> T mod(T a, T b) {
  T ret = a % b;
  while (ret < 0) {
    ret += b;
  }
  return ret;
}

class Ising {
public:
  // Constructor
  Ising(double beta, int l) {
    // Seed the random number generator
    m_rng.seed(42);

    // Store parameters
    m_beta = beta;
    m_l = l;

    // Setup data field to a random state
    m_data.resize(l * l);

    // Fill m_data with random states
    for (auto &i : m_data) {
      i = random_int(2) * 2 - 1;
      assert((i == 1) or (i == -1));
    };

    // Initialize running energy and magnetization
    update();
  };

  // Recalculate the energy from the state of the Ising model
  void recalculate_magnetization() {
    m_M = 0;
    for (auto &i : m_data) {
      m_M += i;
    }
    assert((m_M >= -m_l * m_l) and (m_M <= m_l * m_l));
  };

  // Recalculate the energy from the state of the Ising model
  void recalculate_energy() {
    double m_E = 0;
    for (int i = 0; i<m_l; i++) {
    for (int j = 0; j<m_l; j++) {
      m_E +=  -get(i,j) * ( get(i-1,j) + get(i+1,j) + get(i,j-1) + get(i,j+1) ) * 0.5;
    }
    }
  };

  // Update running values for energy and magnetization
  void update() {
    recalculate_energy();
    recalculate_magnetization();
    m_invalid = false;
  };

  // Get spin at i,j
  int get(int i, int j) {
    int _i = mod(i, m_l);
    int _j = mod(j, m_l);
    assert(_i >= 0 and _i < m_l);
    assert(_j >= 0 and _j < m_l);
    return m_data[get_linear_index(_i, _j)];
  };

  // Set spin at i,j
  void set(int i, int j, int v) {
    assert((v == 1) or (v == -1));
    int _i = mod(i, m_l);
    int _j = mod(j, m_l);
    assert(_i >= 0 and _i < m_l);
    assert(_j >= 0 and _j < m_l);
    m_data[get_linear_index(_i, _j)] = v;
    m_invalid = true;
  };

  // Try to flip a spin and return true if move accepted,
  // update magnetization/energy if move was accepted
  bool try_flip(int i, int j) {
    // Metropolis Criterion
    double r = random_double();
    double dE = 2 * get(i,j) * ( get(i-1,j) + get(i+1,j) + get(i,j-1) + get(i,j+1) );
    bool condition = r < std::min(1.0, std::exp(-m_beta * dE));

    // Spin Flip if condition was accepted
    if (condition) {
      int spin = get(i,j); // Spin at i,j
      spin = spin * (-1); // Flip spin
      set(i,j,spin); // Set new spin at i,j
      update();
    }
    return condition;
  };

  // Try flipping a random spin. Return true if move accepted
  // If move was accepted, also update energy and magnetization
  bool try_random_flip() {
    // Try a single flip on a randomly chosen
    // spin. Re-use (don't copy) existing code.
    // Return true/false depending on whether the move was accepted
    int i = random_int(m_l);
    int j = random_int(m_l);
    return try_flip(i, j);
  };

  void try_many_random_flips(int n) {
    // Try n moves at randomly chosen spins.
    // Re-use (don't copy) existing code!
    for (int p = 0; p < n; p++)
      try_random_flip();
  }

  // Get the current energy
  double get_energy() {
    if (m_invalid) {
      update();
    }
    return m_E;
  };

  // Get the current magnetization
  double get_magnetization() {
    if (m_invalid) {
      update();
    }
    return m_M / (m_l * m_l);
  };

  // Get the raw data
  std::vector<int> get_data() { return m_data; };

private:
  // Parameters
  double m_beta;
  int m_l;

  // Running magnetization, energy
  double m_M;
  double m_E;
  // Are the running values invalid
  bool m_invalid;

  // Ising model
  std::vector<int> m_data;

  // Random number generator
  std::mt19937 m_rng;
  std::uniform_real_distribution<double> m_uniform_dist;
  double random_double() { return m_uniform_dist(m_rng); }

  int random_int(int below) {
    auto x = random_double();
    auto v = static_cast<int>(x * below);
    assert(v >= 0 and v < below);
    return v;
  };

  // Convert 2d indices from 0<=i,j<l to linear index 0<ind<l*l
  int get_linear_index(int i, int j) {
    i = mod(i,m_l);
    j = mod(j,m_l);
    int index = i * m_l + j;
    return index;
  };
};

#endif
