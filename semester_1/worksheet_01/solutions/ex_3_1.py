#!/usr/bin/env python3

import numpy as np
import scipy.constants


class Particle():
    def __init__(self, x, y, vx, vy, mass=1, name=""):
        self.pos = np.array([x, y])
        self.vel = np.array([vx, vy])
        self.mass = mass
        self.force = np.array([0, 0])

    def add_forces(self, other, bidirectional=False):
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
    pass

def step_euler(x, v, dt, mass, g, forces):
    pass

def forces(x, masses, g):
    pass

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # init astro objects
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_init = npz["x_init"]
    v_init = npz["v_init"]
    masses = npz["m"]
    g = npz["g"]

    l = []
    for i in range(len(names)):
        l.append( Particle(*x_init[:,i], *v_init[:,i], masses[i], names[i]) )
    print(l)
