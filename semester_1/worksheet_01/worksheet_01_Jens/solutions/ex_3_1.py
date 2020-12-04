#!/usr/bin/env python3

import numpy as np
import scipy.constants
import matplotlib.pyplot as plt

data = np.load('/home/jens/Desktop/SimMeth/Exercise1/files/solar_system.npz')
names = data['names']
x_init = data['x_init']
v_init = data['v_init']
m = data['m']
g = data['g']

dt = 0.0001

#print(x_init)
print(x_init[1,1])


def force(r_ij, m_i, m_j, g):
    return g*m_i*m_j*r_ij/(np.sqrt(sum(r_ij**2))**3)


def step_euler(x, v, dt, mass, g, forces):
    _x = x + v*dt
    _v = v + forces(x,mass,g)/mass*dt
    return _x,_v

def forces(x, masses, g):
    outforces = np.zeros((2,6),dtype='float')
    for i in range(len(names)-1):
        for j in range(i+1,len(names)):
            c = x[:,i] #current Planet
            o = x[:,j] #other Planets
            f = force(o-c, masses[i], masses[j], g)
            outforces[:,i] += f
            outforces[:,j] -= f
    return np.array(outforces)


def run(x,v,dt,masses,g):
    _x = np.copy(x)
    _v = np.copy(v)
    t=0

    with open("/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_1.txt","w") as outfile:
        outstring = "\t".join(["{:5f}"]*(len(masses)*2+1))
        for k in range(int(1/dt)):
            t += dt
            _forces = forces(_x,masses,g)
            _x,_v = step_euler(_x, _v, dt, masses, g, forces)
            outfile.write(outstring.format(t, *_x.T.flatten()) + "\n")
            yield t,_x,_v
            


if __name__ == "__main__":
    print(names)
    list(run(x_init, v_init, 0.0001, m, g))