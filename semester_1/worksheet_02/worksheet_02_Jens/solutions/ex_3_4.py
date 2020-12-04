#!/usr/bin/env python3

import numpy as np
import scipy.linalg

import ex_3_2

r_cut=2.5
eps = 1.0
sig = 1.0
L=np.array([10.0,10.0])
def lj_potential(r_ij: np.ndarray) -> float:
    r = scipy.linalg.norm(r_ij)
    if r > r_cut:
        return 0
    return 4*eps*((sig/r)**12 - (sig/r)**6)
    

def lj_force(r_ij: np.ndarray) -> np.ndarray:
    r = scipy.linalg.norm(r_ij)
    if r > r_cut:
        return 0
    return 24*eps*(2*(sig/r)**12 * r_ij/(r*r) - (sig/r)**6 * r_ij/(r*r))

def truncated_LJ(func,r_ij: np.ndarray):
    r = scipy.linalg.norm(r_ij)
    if r > r_cut:
        return 0
    return func(r_ij)
        

def forces(x: np.ndarray) -> np.ndarray:
    """Compute and return the forces acting onto the particles,
    depending on the positions x."""
    N = x.shape[1]
    f = np.zeros_like(x)
    for i in range(1, N):
        for j in range(i):
            # distance vector
            r_ij = x[:, j] - x[:, i]
            r_ij = np.mod(r_ij,L*0.5)
            f_ij = lj_force(r_ij)
            f[:, i] -= f_ij
            f[:, j] += f_ij
    return f


def total_energy(x: np.ndarray, v: np.ndarray) -> np.ndarray:
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
            r_ij = np.mod(r_ij,L*0.5)
            E_pot += lj_potential(r_ij)
    # sum up kinetic energy
    for i in range(N):
        E_kin += 0.5 * np.dot(v[:, i], v[:, i])
    return E_pot + E_kin


def step_vv(x: np.ndarray, v: np.ndarray, f: np.ndarray, dt: float):
    # update positions
    x += v * dt + 0.5 * f * dt * dt
    # half update of the velocity
    v += 0.5 * f * dt

    # compute new forces
    f = forces(x)
    # we assume that all particles have a mass of unity

    # second half update of the velocity
    v += 0.5 * f * dt

    return x, v, f


if __name__ == "__main__":
    import matplotlib.pyplot as plt
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

    f = forces(x)

    N_PART = x.shape[1]

    positions = np.full((N_TIME_STEPS, 2, N_PART), np.nan)
    energies = np.full((N_TIME_STEPS), np.nan)


    # main loop
    with open('ljbillards_trunc.vtf', 'w') as vtffile:
        # write the structure of the system into the file:
        # N particles ("atoms") with a radius of 0.5
        vtffile.write(f'atom 0:{N_PART - 1} radius 0.5\n')
        for i in range(N_TIME_STEPS):
            x, v, f = step_vv(x, v, f, DT)
            time += DT

            positions[i, :2] = x
            energies[i] = total_energy(x, v)
            print(x)

            # write out that a new timestep starts
            vtffile.write('timestep\n')
            # write out the coordinates of the particles
            for p in x.T:
                vtffile.write(f"{p[0]} {p[1]} 0.\n")

    traj = np.array(positions)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    for i in range(N_PART):
        ax1.plot(positions[:, 0, i], positions[:, 1, i], label='{}'.format(i))
    ax1.set_title('Trajectory')
    ax1.set_aspect('equal')
    ax1.set_xlabel('x position')
    ax1.set_ylabel('y position')
    ax1.legend()
    ax2.set_xlabel("Time step")
    ax2.set_ylabel("Total energy")
    ax2.plot(energies)
    ax2.set_title('Total energy')
    plt.show()
