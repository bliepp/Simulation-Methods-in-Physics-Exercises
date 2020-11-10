#!/usr/bin/env python3

import numpy as np
from helper import data2file

def force(mass, gravity):
    return np.array([0, -1*mass*gravity])

def step_euler(x, v, dt, mass, gravity, f):
    _x = x + v*dt
    _v = v + f*dt/mass
    return _x, _v

if __name__ == "__main__":
    x, v = np.array([0,0]), np.array([50, 50]) # m, m/s
    g = 9.81 # m/s^2
    m = 2.0 # kg
    
    time = 0
    dt = 0.01
    
    with open("outfiles/ex_2_1.out", "w") as outfile:
        data2file(outfile, time, x, v)
        while x[1] >= 0:
            time += dt
            f = force(m, g)
            x, v = step_euler(x, v, dt, m, g, f)
            data2file(outfile, time, x, v)



