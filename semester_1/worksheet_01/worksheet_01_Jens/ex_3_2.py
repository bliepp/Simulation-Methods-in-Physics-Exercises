#!/usr/bin/env python3

import numpy as np

from ex_3_1 import *


def step_symplectic_euler(x, v, dt, mass, g, forces):
    _v = v + forces(x,mass,g)/mass*dt
    _x = x + _v*dt
    return _x,_v

def step_velocity_verlet(x, v, dt, mass, g, forces):
    forces_old = forces(x,mass,g)
    _x=x+v*dt+forces_old/(2*mass)*dt**2
    forces_n=forces(_x,mass,g)
    _v = v+(forces_old/(2*mass))*dt + (forces_n/(2*mass))*dt
    return _x,_v

def run_var(x,v,dt,masses,g,alg):
    _x = np.copy(x)
    _v = np.copy(v)
    t=0
    filename = "/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_2_"+alg.__name__+".txt"
    with open(filename,"w") as outfile:
        outstring = "\t".join(["{:5f}"]*(len(masses)*2+1))
        for k in range(int(1/dt)):
            t += dt
            _forces = forces(_x,masses,g)
            _x,_v = alg(_x, _v, dt, masses, g, forces)
            outfile.write(outstring.format(t, *_x.T.flatten()) + "\n")
            yield t,_x,_v

if __name__ == "__main__":
    print(names)
    list(run_var(x_init, v_init, 0.01, m, g,step_euler))
    list(run_var(x_init, v_init, 0.01, m, g,step_symplectic_euler))
    list(run_var(x_init, v_init, 0.01, m, g,step_velocity_verlet))
