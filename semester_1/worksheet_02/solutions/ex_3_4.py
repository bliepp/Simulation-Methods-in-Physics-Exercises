#!/usr/bin/env python3

from contextlib import ExitStack
import numpy as np

import ex_3_2


def truncated(func, r_ij: np.ndarray, cutoff):
    if np.sqrt(sum(r_ij*r_ij)) > cutoff:
        return 0
    return func(r_ij)


def forces(x: np.ndarray, cutoff, box) -> np.ndarray:
    """Compute and return the forces acting onto the particles,
    depending on the positions x."""
    
    N = x.shape[1]
    f = np.zeros_like(x)
    for i in range(1, N):
        for j in range(i):
            # distance vector
            r_ij = x[:, j] - x[:, i]
            r_ij = r_ij - box*np.round(r_ij/box) #np.mod(r_ij, box)

            f_ij = truncated(ex_3_2.lj_force, r_ij, cutoff)
            f[:, i] -= f_ij
            f[:, j] += f_ij
    return f


def total_energy(x: np.ndarray, v: np.ndarray, cutoff, shift, box) -> np.ndarray:
    """Compute and return the total energy of the system with the
    particles at positions x and velocities v."""
    N = x.shape[1]
    E_pot = 0.0
    E_kin = 0.0
    # sum up potential energies
    for i in range(1, N):
        for j in range(i):
            # distance vector
            r_ij = x[:, j] - x[:, i]
            r_ij = r_ij - box*np.round(r_ij/box) #np.mod(r_ij, box)
            pot = truncated(ex_3_2.lj_potential, r_ij, cutoff) 
            E_pot += pot + shift*bool(pot) # only shift if in range
    # sum up kinetic energy
    for i in range(N):
        E_kin += 0.5 * np.dot(v[:, i], v[:, i])
    return E_pot, E_kin


def step_vv(x: np.ndarray, v: np.ndarray, f: np.ndarray, dt: float, cutoff, box):
    # update positions
    x += v * dt + 0.5 * f * dt * dt
    # half update of the velocity
    v += 0.5 * f * dt

    # compute new forces
    f = forces(x, cutoff, box)
    # we assume that all particles have a mass of unity

    # second half update of the velocity
    v += 0.5 * f * dt

    return x, v, f



if __name__ == "__main__":
    R_CUT = 2.5
    SHIFT = 0.016316891136
    BOX = np.ones(2)*10.0

    DT = 0.01
    T_MAX = 20.0
    N_TIME_STEPS = int(T_MAX / DT)

    # running variables
    time = 0.0

    # particle positions
    x = np.zeros((2, 2))
    x[:, 0] = [3.9, 3.0]
    x[:, 1] = [6.1, 5.0]

    # particle velocities
    v = np.zeros((2, 2))
    v[:, 0] = [-2.0, -2.0]
    v[:, 1] = [2.0, 2.0]

    f = forces(x, R_CUT, BOX)

    N_PART = x.shape[1]
    
    # main loop
    with ExitStack() as stack:
        vtffile = stack.enter_context(open('outfiles/ljbillards_pbc.vtf', 'w'))
        outfile = stack.enter_context(open("outfiles/ex_3_4.out", "w"))

        # write the structure of the system into the file:
        # N particles ("atoms") with a radius of 0.5
        vtffile.write(f'atom 0:{N_PART - 1} radius 0.5\n')
        vtffile.write(f'pbc {BOX[0]} {BOX[1]} 10.0\n')
        outfile.write("#TIME\tE_POT\tE_KIN\tPARTSXY\n")
        for i in range(N_TIME_STEPS):
            x, v, f = step_vv(x, v, f, DT, R_CUT, BOX)
            time += DT

            E_pot, E_kin = total_energy(x, v, R_CUT, SHIFT, BOX)

            # write out that a new timestep starts
            vtffile.write('timestep\n')
            outfile.write(f"{time:.4f}\t{E_pot:.4f}\t{E_kin:.4f}")
            # write out the coordinates of the particles
            #print(time)
            for p in x.T:
                vtffile.write(f"{p[0]} {p[1]} 0.\n")
                outfile.write(f"\t{p[0]:.4f}\t{p[1]:.4f}")
            outfile.write("\n")

