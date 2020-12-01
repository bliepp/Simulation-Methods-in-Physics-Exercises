#!/usr/bin/env python3

import numpy as np
import scipy.linalg


EPSILON = 1
SIGMA = 1


def lj_potential(r_ij: np.ndarray) -> float:
    abs_r_ij = np.sqrt(sum(r_ij*r_ij))
    part = (SIGMA/abs_r_ij)**6
    return 4*EPSILON*(part*part - part)


def lj_force(r_ij: np.ndarray) -> np.ndarray:
    abs_r_ij = np.sqrt(sum(r_ij*r_ij))
    part = (SIGMA/abs_r_ij)**6
    return 24*EPSILON*(r_ij/(abs_r_ij*abs_r_ij))*(2*part*part - part)


if __name__ == "__main__":
    d = np.array([0.0, 0.0])
    
    with open("outfiles/ex_3_2.out", "w") as f:
        for d[0] in np.linspace(0.85, 2.5, 1000):
            pot = lj_potential(d)
            f_x, _ = lj_force(d)
            
            f.write("{:0.8f}\t{:.8f}\t{:.8f}\n".format(
                d[0], pot, f_x)
                )


