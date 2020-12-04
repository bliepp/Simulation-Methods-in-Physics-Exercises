#!/usr/bin/env python3

import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt

eps = 1
sig = 1
def lj_potential(r_ij: np.ndarray) -> float:
    r = scipy.linalg.norm(r_ij)
    return 4*eps*((sig/r)**12 - (sig/r)**6)
    

def lj_force(r_ij: np.ndarray) -> np.ndarray:
    r = scipy.linalg.norm(r_ij)
    return 24*eps*(2*(sig/r)**12 * r_ij/(r*r) - (sig/r)**6 * r_ij/(r*r))

if __name__ == "__main__":
    d = np.array([0.0,0.0])
    with open("/home/jens/Desktop/SimMeth/Exercise2/outfiles/ex_3_2.txt","w") as f:
        for d[0] in np.linspace(0.85,2.5,1000):
            pot = lj_potential(d)
            f_x,_ = lj_force(d)
            f.write("{:.5f}\t{:.5f}\t{:.5f}\n".format(d[0],pot,f_x))

