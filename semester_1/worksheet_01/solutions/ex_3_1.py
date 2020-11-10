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
    outforces = x*0
    for i in range(len(masses)-1):
        for j in range(i+1, len(masses)):
            current = x[:,i]
            other = x[:,j]
            f = force(
                other - current,
                masses[i],
                masses[j],
                g
            )
            outforces[:,i] += f
            outforces[:,j] -= f
    return np.array(outforces)


def run(x, v, dt, masses, g):
    _x = np.copy(x)
    _v = np.copy(v)
    time = 0

    with open("outfiles/ex_3_1.out", "w") as outfile:
        outstring = "\t".join(["{:.5f}"]*(len(masses)*2+1))
        for i in range(int(1/dt)): # one year
            time += dt
            _forces = forces(_x, masses, g)
            _x, _v = step_euler(_x, _v, dt, masses, g, forces)
            outfile.write(outstring.format(
                time, *_x.T.flatten() # write x1 y1 x2 y2 etc.
            ) + "\n")
            yield time, _x, _v



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # init astro objects
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_init = npz["x_init"]
    v_init = npz["v_init"]
    masses = npz["m"]
    g = npz["g"]
    
    print(names)
    list(run(x_init, v_init, 0.0001, masses, g))

