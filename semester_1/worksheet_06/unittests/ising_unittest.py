#!/usr/bin/env python

import pathlib, sys
import argparse
import unittest

import tqdm
import ising

import numpy as np

sys.path.insert(
    0, str(
        pathlib.Path(__file__).resolve().parent.parent.joinpath('solutions')))
#import cising


def compute_energy(sigma):
    L = sigma.shape[0]
    shifted_ixs = np.roll(np.arange(0, L), -1)
    E = -(sigma*sigma[shifted_ixs, :]).sum()
    E -= (sigma*sigma[:, shifted_ixs]).sum()
    return E


class TestStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.L = 4
        cls.BETA = 1./5.


class TestCython():#TestStrategy):
    @classmethod
    def setUpClass(cls):
        super(TestCython, cls).setUpClass()
        cls.model = cising.IsingModel(cls.BETA, cls.L)

    def test_init(self):
        I_numpy = self.model.as_numpy()
        self.assertEqual(self.model.l, self.L, "L is not set correctly.")
        self.assertEqual(I_numpy.shape, (self.L,self.L), "Setting up the lattice dimensions failed.")
        self.assertTrue(np.all(np.abs(I_numpy.flatten()) == 1), "Not all spins are +/-1.")

    def test_setget(self):
        self.model.set(3, 2, 1)
        self.assertEqual(self.model.get(3, 2), 1,
            "Getter and setter do not work properly with spin up.")

        self.model.set(3, 2, -1)
        self.assertEqual(self.model.get(3, 2), -1,
            "Getter and setter do not work properly with spin down.")
    
    def test_properties(self):
        self.assertEqual(self.model.magnetization(), np.average(self.model.as_numpy()),
            "Calculation of the basic magnetization failed.")
        self.assertEqual(self.model.energy(), compute_energy(self.model.as_numpy()),
            "Calculation of the basic energy failed.")
        for v in -1, 1:
            for i in range(self.L+1):
                for j in range(self.L+1):
                    self.model.set(i, j , v)
            self.assertEqual(self.model.magnetization(), v,
                f"Magnetization failed for v = {v}")
            self.assertEqual(self.model.energy(), -2 * self.L*self.L,
                f"Energy failed for v = {v}")
    
    def test_spinflip(self):
        for i in range(1000):
            self.model.try_random_flip()
        self.assertEqual(self.model.energy(), compute_energy(self.model.as_numpy()),
            "Spin flip does not work as intended.")
    
    def test_bruteforce(self):
        Es, Ms = [], []
        for i in tqdm.tqdm(range(100_000), desc=self.__class__.__name__ ):
            self.model.try_many_random_flips(500)
            Es.append(self.model.energy())
            Ms.append(self.model.magnetization())

        self.assertLess( abs(np.average(Es)/(self.L*self.L) + 0.4561353695), 0.01,
            "Bruteforce energy calculation failed.")
        self.assertLess( abs(np.average(np.abs(Ms)) - 0.342765627554), 0.001,#2,
            "Bruteforce magnetization calculation failed.")


class TestOwn(TestStrategy):
    @classmethod
    def setUpClass(cls):
        super(TestOwn, cls).setUpClass()
        
        cls.code = "cpp"
        cls.model = ising.cpp.Ising(cls.L, init=False)
        cls.model.randomize()
    
    def test_init(self):
        I_numpy = np.array(self.model.lattice)
        self.assertEqual(self.model.L, self.L, "L is not set correctly.")
        self.assertEqual(len(I_numpy), self.L*self.L, "Setting up the lattice dimensions failed.")
        self.assertTrue(np.all(np.abs(I_numpy) == 1), "Not all spins are +/-1.")
    
    def test_setget(self):
        self.model.set_spin(3, 2, 1)
        self.assertEqual(self.model.get_spin(3, 2), 1,
            "Getter and setter do not work properly with spin up.")

        self.model.set_spin(3, 2, -1)
        self.assertEqual(self.model.get_spin(3, 2), -1,
            "Getter and setter do not work properly with spin down.")
    
    def test_properties(self):
        I_numpy = np.array(self.model.lattice).reshape(self.L, self.L)
        self.assertEqual(self.model.magnetization, np.average(I_numpy),
            "Calculation of the basic magnetization failed.")
        self.assertEqual(self.model.energy, compute_energy(I_numpy),
            "Calculation of the basic energy failed.")
        for v in -1, 1:
            for i in range(self.L+1):
                for j in range(self.L+1):
                    self.model.set_spin(i, j , v)
            self.assertEqual(self.model.magnetization, v,
                f"Magnetization failed for v = {v}")
            self.assertEqual(self.model.energy, -2 * self.L*self.L,
                f"Energy failed for v = {v}")
    
    def test_spinflip(self):
        for i in range(1000):
            pos = np.random.randint(0, self.L, size=2)
            self.model.flip_spin(*pos)
        
        I_numpy = np.array(self.model.lattice).reshape(self.L, self.L)
        self.assertEqual(self.model.energy, compute_energy(I_numpy),
            "Spin flip does not work as intended.")
    
    def test_bruteforce(self):
        #self.assertTrue(False, "This method does not work for some reason")
        Es, Ms = [], []
        for i in tqdm.tqdm(range(100_000), desc=self.__class__.__name__ + " " + self.code):
            self.model.metropolis(500, self.BETA)
            Es.append(self.model.energy)
            Ms.append(self.model.magnetization)

        self.assertLess( abs(np.average(Es)/(self.L*self.L) + 0.4561353695), 0.01,
            "Bruteforce energy calculation failed.")
        self.assertLess( abs(np.average(np.abs(Ms)) - 0.342765627554), 0.0012,
            "Bruteforce magnetization calculation failed.")


if __name__ == "__main__":
    unittest.main()