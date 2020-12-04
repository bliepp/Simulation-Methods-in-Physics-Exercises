#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

#force acting on cannonball
def force(mass, gravity):
    return np.array([0,-1*mass*gravity])
    


#Euler step describing evolution of cannonbal
def step_euler(x,v,dt,mass,gravity,f):
    _x = x + v*dt
    _v = v + f/mass*dt
    return _x,_v


#Loop simulating ball motion
if __name__ == "__main__":
    x,v, = np.array([0,0]) , np.array([50,50])
    m = 2.0
    g = 9.81
    t = 0
    dt = 0.01
    with open("/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_1_out.txt","a") as outfile:
        while x[1]>=0:
            t += dt
            f = force(m,g)
            x,v = step_euler(x,v,dt,m,g,f)
            print(t,x,v)
            np.savetxt(outfile,np.c_[t,x[0],x[1],v[0],v[1]],fmt='%f',delimiter='\t')




