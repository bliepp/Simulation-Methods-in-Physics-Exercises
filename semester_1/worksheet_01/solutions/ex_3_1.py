#!/usr/bin/env python3

import numpy as np
import scipy.constants


def force(r_ij, m_i, m_j, g):
    return g*m_i*m_j*r_ij / np.sqrt(sum(r_ij**2))**3

def step_euler(x, v, dt, mass, g, forces):
    _x = x + v*dt
    _v = v + forces(x, mass, g)*dt/mass
    return _x, _v

def forces(x, masses, g):
    outforces = np.zeros_like(x) # or x*0
    for i in range(len(masses)-1):
        for j in range(i+1, len(masses)):
            f = force(x[:,j] - x[:,i], masses[i], masses[j], g)
            outforces[:,i] += f
            outforces[:,j] -= f
    return outforces


def run(x, v, dt, masses, g, integrator, years=1.0):
    _x = np.copy(x)
    _v = np.copy(v)
    time = 0

    for i in range(int(years/dt)):
        time += dt
        #_forces = forces(_x, masses, g)
        _x, _v = integrator(_x, _v, dt, masses, g, forces)
        yield time, _x, _v



if __name__ == "__main__":    
    # init astro objects
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_0 = npz["x_init"]
    v_0 = npz["v_init"]
    masses = npz["m"]
    g = npz["g"]

    print(names)
    for f, (algorithm, dt) in {
    	"ex_3_1.out": (step_euler, 0.0001),
    	"ex_3_1_coarse.out": (step_euler, 0.001)
    }.items():
        with open("outfiles/{}".format(f), "w") as outfile:
            outstring = "\t".join(["{:.5f}"]*(len(masses)*2+1))
            for t, x, v in run(x_0, v_0, dt, masses, g, algorithm):
                outfile.write(outstring.format(
                    t, *x.T.flatten() # write x1 y1 x2 y2 etc.
                ) + "\n")

