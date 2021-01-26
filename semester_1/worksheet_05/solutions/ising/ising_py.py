#!/usr/bin/env python
import numpy as np


class Ising():
    def __init__(self, L, init=True):
        self.L = L
        self.L2 = L*L

        # read-only attribute
        if init:
            self.__lattice = np.ones(self.L2, dtype=np.int32)
            #self.__lattice = np.random.choice([1, -1], size=self.L2)
        else:
            self.__lattice = np.empty(self.L2)
    
    @property
    def lattice(self):
        return self.__lattice
    
    @lattice.setter
    def lattice(self, new):
        if len(new) == len(self.__lattice):
            self.__lattice = np.array(new)
        else:
            raise IndexError(f"New list must be L*L = {self.L2} elements long")
    
    def get_spin(self, i, j):
        i, j = i % self.L, j % self.L
        return self.__lattice[i*self.L + j]
    
    def set_spin(self, i, j, value):
        i, j = i % self.L, j % self.L
        self.__lattice[i*self.L + j] = value
    
    def flip_spin(self, i, j):
        self.set_spin(i, j, -1*self.get_spin(i, j))
    
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
        for i in range(self.L):
            for j in range(self.L):
                mu += self.get_spin(i, j)
        return mu/(self.L2)
