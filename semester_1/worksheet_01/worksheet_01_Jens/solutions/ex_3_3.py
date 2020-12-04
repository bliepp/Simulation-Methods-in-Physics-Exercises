#!/usr/bin/env python3

import numpy as np
import scipy.constants
import matplotlib.pyplot as plt

from ex_3_2 import *
from ex_3_1 import *

            
def run_var_d(x,v,dt,masses,g,alg):
    _x = np.copy(x)
    _v = np.copy(v)
    t=0
    filename = "/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_3_"+alg.__name__+".txt"
    with open(filename,"w") as outfile:
        outstring = "\t".join(["{:5f}"]*2)
        for k in range(int(10/dt)):
            t += dt
            #_forces = forces(_x,masses,g)
            _x,_v = alg(_x, _v, dt, masses, g, forces)
            rel = _x[:,2] - _x[:,1]
            d = np.sqrt(sum(rel**2)) #Absolute Distance
            outfile.write(outstring.format(t,d) + "\n")
            yield t,_x,_v

if __name__ == "__main__":
    print(names)
    list(run_var_d(x_init, v_init, 0.01, m, g,step_euler))
    list(run_var_d(x_init, v_init, 0.01, m, g,step_symplectic_euler))
    list(run_var_d(x_init, v_init, 0.01, m, g,step_velocity_verlet))