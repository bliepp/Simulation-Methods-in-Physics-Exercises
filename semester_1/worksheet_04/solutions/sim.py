import argparse
import gzip
import pickle

import numpy as np

from Mersenne import BoxMuller

# SYSTEM CONSTANTS
# timestep
DT = 0.01
# length of run
TIME_MAX = 2000.0
# desired temperature
T = 0.3
# total number of particles
N = 50
# friction coefficient
GAMMA_LANGEVIN = 0.8
# number of steps to do before the next measurement
MEASUREMENT_STRIDE = 50


parser = argparse.ArgumentParser()
parser.add_argument('id', type=int, help='Simulation id')
args = parser.parse_args()


rng = BoxMuller(0, np.sqrt(2*T*GAMMA_LANGEVIN/DT))


def generate_random_force(arr):
    temp = np.empty_like(arr)
    for index, _ in np.ndenumerate(temp): 
        temp[index] = next(rng)
    return temp

def compute_temperature(v):
    return (v * v).sum() / (3*N)


def compute_energy(v):
    return (v * v).sum() / 2.


def step_vv(x, v, f, dt):
    # update positions
    x += v * dt + 0.5 * f * dt * dt

    # half update of the velocity
    v += 0.5 * f * dt

    # for this excercise no forces from other particles
    f = np.zeros_like(x)

    # second half update of the velocity
    v += 0.5 * f * dt

    return x, v, f


def step_vv_langevin(x, v, g, dt, gamma):
    # update positions
    x += (v * dt)*(1- dt * gamma * 0.5) + 0.5 * g * dt * dt

    # half update of the velocity
    factor = 1/(1 + dt * gamma * 0.5)
    v *= (1 - dt * gamma * 0.5) * factor
    v += 0.5 * g * dt * factor

    # for this excercise no forces from other particles
    g = generate_random_force(g)

    # second half update of the velocity
    v += 0.5 * g * dt * factor

    return x, v, g


# SET UP SYSTEM OR LOAD IT
print("Starting simulation...")
t = 0.0
step = 0

# random particle positions
x = np.random.random((N, 3))
v = np.zeros((N, 3))

# variables to cumulate data
ts = []
Es = []
Tms = []
vels = []
traj = []


# main loop
f = generate_random_force(x)


print(f"Simulating until tmax={TIME_MAX}...")

while t < TIME_MAX:
    x, v, f = step_vv_langevin(x, v, f, DT, GAMMA_LANGEVIN)

    t += DT
    step += 1

    if step % MEASUREMENT_STRIDE == 0:
        E = compute_energy(v)
        Tm = compute_temperature(v)
        vels.append(v.flatten())
        traj.append(x.flatten())
        print(f"t={t}, E={E}, T_m={Tm}")

        ts.append(t)
        Es.append(E)
        Tms.append(Tm)


# at the end of the simulation, write out the final state
datafilename = f'{args.id}.dat.gz'
print(f"Writing simulation data to {datafilename}.")
vels = np.array(vels)
traj = np.array(traj)

datafile = gzip.open(datafilename, 'wb')
pickle.dump([N, T, GAMMA_LANGEVIN, x, v, ts, Es, Tms, vels, traj], datafile)
datafile.close()


print("Finished simulation.")
