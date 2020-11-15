#!/usr/bin/env python3

import numpy as np

from ex_3_1 import run, force, forces, step_euler


old_forces = None # oh oh, global vars are bad!


def step_symplectic_euler(x, v, dt, mass, g, forces):
    # swapped order to make euler symplectic
    _v = v + forces(x, mass, g)*dt/mass
    _x = x + _v*dt
    return _x, _v

def step_velocity_verlet(x, v, dt, mass, g, forces):
    global old_forces
    if old_forces is None:
        old_forces = forces(x, mass, g)

    _x = x + v*dt + 0.5*old_forces*dt*dt/mass
    _v = v + 0.5*old_forces*dt/mass

    old_forces = forces(_x, mass, g) # recalc forces
    _v += 0.5*old_forces*dt/mass
    return _x, _v



if __name__ == "__main__":
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_0 = npz["x_init"]
    v_0 = npz["v_init"]
    masses = npz["m"]
    g = npz["g"]

    print(names)
    for f, (algorithm, dt) in {
        "ex_3_2_velver.out": (step_velocity_verlet, 0.01),
        "ex_3_2_symeul.out": (step_symplectic_euler, 0.01)
    }.items():
        with open("outfiles/{}".format(f), "w") as outfile:
            outstring = "\t".join(["{:.5f}"]*(len(masses)*2+1))
            for t, x, v in run(x_0, v_0, dt, masses, g, algorithm):
                outfile.write(outstring.format(
                    t, *x.T.flatten() # write x1 y1 x2 y2 etc.
                ) + "\n")

