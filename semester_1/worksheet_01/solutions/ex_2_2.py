#!/usr/bin/env python3

import numpy as np
from helper import data2file

import ex_2_1

def force(mass, gravity, v, gamma, v_0):
    return ex_2_1.force(mass, gravity) - gamma * (v - np.array([v_0, 0]))

def run(x, v, dt, mass, gravity, gamma, v_0, filename=None):
    _x, _v = np.copy(x), np.copy(v)
    time = 0

    with open(filename, "w") as outfile:
        data2file(outfile, time, _x, _v)
        while _x[1] >= 0:
            time += dt
            _x, _v = ex_2_1.step_euler(
                _x, _v, dt, mass, gravity,
                force(mass, gravity, _v, gamma, v_0)
            )
            data2file(outfile, time, _x, _v)
            yield time, _x, _v

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit

    mass = 2.0
    gravity = 9.81
    gamma = 0.1

    x = np.array([0, 0])
    v = np.array([50, 50])
    dt = 0.01
    
    # part 1
    trajectories = [
        run(x, v, dt, mass, gravity, 0, 0, "outfiles/ex_2_2.out"),
        run(x, v, dt, mass, gravity, gamma, 0, "outfiles/ex_2_2_friction.out"),
        run(x, v, dt, mass, gravity, gamma, -50, "outfiles/ex_2_2_friction_wind.out")
    ]
    trajectories = [
        np.array(list(t), dtype=object).T.tolist()
        for t in trajectories
    ]
    trajectories = dict(zip([
        "No fritction, no wind",
        "Only friction, no wind",
        "Friction and wind"
        ],trajectories))


    # part 2
    v_w = -50
    distances = []
    while v_w > -350:
        t = np.array(list(run(x, v, dt, mass, gravity, gamma, v_w, "outfiles/lost.out")),
            dtype=object).T.tolist()
        d = np.array(t[1])[:,0][-1]
        distances.append((v_w, d))
        v_w -= 1
    
    with open("outfiles/ex_2_2_winds.out", "w") as f:
        for item in distances:
            f.write("{}\t{}\n".format(item[0], item[1]))
    
    distances = np.array(distances).T
    
    params, cov = curve_fit(lambda m, b, x: m*x + b, distances[1], distances[0])
    print(params)


