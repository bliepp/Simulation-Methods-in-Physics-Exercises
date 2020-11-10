#!/usr/bin/env python3

import numpy as np
import scipy.constants

from helper import data2file


class Particle():
    def __init__(self, x, y, vx, vy, mass=1, name=""):
        self.pos = np.array([x, y])
        self.vel = np.array([vx, vy])
        self.mass = mass
        self.force = np.array([0, 0])

    def reset_force():
        self.force *= 0

    def add_forces(self, other, bidirectional=True):
        if isinstance(other, (int, float, bool)):
            self.force += other
            return
        if isinstance(other, Particle):
            rel = other.pos - self.pos # correct order?
            force = G*other.mass*self.mass*rel
            force /= np.sqrt(sum(rel**2))**3
            self.force += force
            other.force -= force*bidirectional
            return


def force(r_ij, m_i, m_j, g):
    return g*m_i*m_j*r_ij / np.sqrt(sum(rel**2))**3

def step_euler(x, v, dt, mass, g, forces):
    _x = x + v*dt
    _v = v + forces*dt/mass
    return _x, _v

def forces(x, masses, g):
    outforces = x*0
    for i in range(len(masses)-1):
        for j in range(i+1, len(masses)):
            current = x[:,i], masses[i]
            other = x[:,j], masses[j]
            f = force(
                current[0] - other[0],
                current[1],
                other[1],
                g
            )
            outforces[:,i]+= f
            outforces[:,j] -= f
    return np.array(outforces)


def run(x, v, dt, masses, g):
    _x = np.copy(x)
    _v = np.copy(v)
    time = 0
    
    with open("outfiles/ex_3_1.out") as outfile:
        outstring = "\t".join(["{}"]*(len(masses)*2+1))
        for i in range(int(1/dt)): # one year
            time += dt
            _forces = forces(x.T[i], masses[i], g)
            _x, _v = step_euler(_x, _v, dt, masses, _g, _forces)
            outfile.write(outstring.format(
                time, *_x.T.flatten() # write x1 y1 x2 y2 etc.
            ) + "\n")
            yield time, _x, _y



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # init astro objects
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_init = npz["x_init"]
    v_init = npz["v_init"]
    masses = npz["m"]
    g = npz["g"]

    run(x_init, v_init, 0.0001, masses, g)

#    particles = []
#    for i in range(len(names)):
#        particles.append( Particle(*x_init[:,i], *v_init[:,i], masses[i], names[i]) )
