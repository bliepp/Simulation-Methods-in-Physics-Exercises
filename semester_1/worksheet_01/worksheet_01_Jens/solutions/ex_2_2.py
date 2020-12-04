 #!/usr/bin/env python3

import numpy as np

import ex_2_1

def force(mass, gravity, v, gamma, v_0):
    return ex_2_1.force(mass,gravity) - gamma*(v-v_0)


if __name__ == "__main__":
    x,v,v_0 = np.array([0,0]) , np.array([50,50]) , np.array([50,0])
    m = 2.0
    g = 9.81
    t = 0
    dt = 0.01
    gamma=0.1
    print(force(m,g,v,gamma,v_0))
    with open("/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_2_f_ww_out.txt","a") as outfile:
        while x[1]>=0:
            t += dt
            f = force(m,g,v,gamma,v_0)
            x,v = ex_2_1.step_euler(x,v,dt,m,g,f)
            print(t,x,v)
            np.savetxt(outfile,np.c_[t,x[0],x[1],v[0],v[1]],fmt='%f',delimiter='\t')

#def run(x, v, dt, mass, gravity, gamma, v_0):
#    t=0
#    with open("/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_2_out.txt","a") as outfile:
#        while x[1]>=0:
#            t += dt
#            f = force(mass,gravity,v,gamma,v_0)
#            x,v = ex_2_1.step_euler(x,v,dt,mass,gravity,f)
#            np.savetxt(outfile,np.c_[t,x[0],x[1],v[0],v[1]],fmt='%f',delimiter='\t')


#if __name__ == "__main__":
#    run(np.array([0,0]),np.array([50,50]),0.01,2.0,9.81,0.1,np.array([0,0]))
