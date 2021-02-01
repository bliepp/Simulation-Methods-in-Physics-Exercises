#!/usr/bin/env python
import numpy as np


class Ising():
    def __init__(self, L, init=True):
        self.L = L
        self.L2 = L*L

        # read-only attribute
        if init:
            self.__lattice = np.ones(self.L2, dtype=np.int32)
        else:
            self.__lattice = np.empty(self.L2)
    
    def randomize(self):
        self.__lattice = np.random.choice([1, -1], size=self.L2)
        return self

    # getters and setters
    def get_spin_by_index(self, index):
        index = index % self.L2
        return self.__lattice[index]
    
    def set_spin_by_index(self, index, value):
        index = index % self.L2
        self.__lattice[index] = value
        return self

    def get_spin(self, i, j):
        i, j = i % self.L, j % self.L
        return self.get_spin_by_index(i*self.L + j)

    def set_spin(self, i, j, value):
        i, j = i % self.L, j % self.L
        self.set_spin_by_index(i*self.L + j, value)
        return self
    
    def flip_spin(self, i, j):
        dE = self._local_energy(i, j)
        self.set_spin(i, j, -1*self.get_spin(i, j))
        dE = self._local_energy(i, j) - dE # not sure about sign
        return dE

    @property
    def lattice(self):
        return self.__lattice
    
    @lattice.setter
    def lattice(self, new):
        if len(new) == len(self.__lattice):
            self.__lattice = np.array(new)
        else:
            raise IndexError(f"New list must be L*L = {self.L2} elements long")
    
    # compute properties
    def _local_energy(self, i, j):
        return self.get_spin(i, j)*(
            self.get_spin(i-1, j)
            + self.get_spin(i+1, j)
            + self.get_spin(i, j-1)
            + self.get_spin(i, j+1)
        )
    
    @property
    def energy(self):
        total = 0
        for i in range(self.L):
            for j in range(self.L):
                total += self._local_energy(i, j)
        return 0.5 * total
    
    @property
    def magnetization(self):
        mu = 0
        for index in range(self.L2):
            mu += self.get_spin_by_index(index)
        return mu/(self.L2)
    
    # simulate
    def metropolis(self, steps, beta = 0):
        accepted, e, m = 0, 0, 0

        E = self.energy
        for _ in range(steps):
            r = np.random.rand() # 0..1
            pos = np.random.randint(0, self.L, size=2) # i, j

            dE = self.flip_spin(*pos)
            condition = r < min(1, np.exp(-beta * dE))

            accepted += condition
            E += dE*condition

            if not condition:
                self.flip_spin(*pos)

            # no np.exp(-beta * E)because p = exp(-beta*E)/Z is chosen
            # see https://en.wikipedia.org/wiki/Monte_Carlo_method_in_statistical_physics#Importance_sampling
            e += E
            m += abs(self.magnetization)

        return accepted/steps, e/steps/self.L2, m/steps
