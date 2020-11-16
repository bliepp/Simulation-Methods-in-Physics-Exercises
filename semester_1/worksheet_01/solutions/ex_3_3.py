#!/usr/bin/env python3

import numpy as np

from ex_3_1 import run, force, forces, step_euler
from ex_3_2 import step_symplectic_euler, step_velocity_verlet


if __name__ == "__main__":
    npz = np.load("../files/solar_system.npz")
    names = npz["names"]
    x_0 = npz["x_init"]
    v_0 = npz["v_init"]
    m = npz["m"]
    g = npz["g"]

    print(names)
    for f, (algo, dt) in {
        "ex_3_3_velver.out": (step_velocity_verlet, 0.01),
        "ex_3_3_symeul.out": (step_symplectic_euler, 0.01)
    }.items():
        with open("outfiles/{}".format(f), "w") as outfile:
            for t, x, v in run(x_0, v_0, dt, m, g, algo, years=10.0):
                outfile.write("{:.2f}\t{:.5f}\n".format(
                    t, np.sqrt(sum( (x[:,2]-x[:,1])**2 ))
                ))
