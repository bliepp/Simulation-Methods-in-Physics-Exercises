#!/usr/bin/env python
from copy import deepcopy
import argparse
import itertools
import tqdm
#import tqdm.contrib.itertools as itertools
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('-L', help="Exercise 4", type=int)
args = parser.parse_args()

TOTAL = args.L*args.L


def get_spin(lattice, i, j):
    return lattice[i % args.L, j % args.L]

def compute_energy(lattice, i, j):
    return 0.5 * (get_spin(lattice, i, j)*(
            get_spin(lattice, i-1, j)
            + get_spin(lattice, i+1, j)
            + get_spin(lattice, i, j-1)
            + get_spin(lattice, i, j+1)
        ))

def compute_total_energy(lattice):
    Energy = 0
    for i in range(args.L):
        for j in range(args.L):
            Energy += compute_energy(lattice, i, j)

    return Energy

def compute_magnetization(lattice):
    mu = 0
    for i in range(args.L):
        for j in range(args.L):
            mu += get_spin(lattice, i, j)
    return mu/(args.L*args.L)

def ising_pure_python():
    TMP, ENG, MAG = list(), list(), list()

    for T in range(10, 51):
        kB, T = 1, T/10
        beta = 1 / (kB*T)
        
        energy_per_side, mag_per_side = 0, 0
        lattices = itertools.product(*[(-1,1)]*args.L*args.L)

        inv_Z = 1/len(list(deepcopy(lattices)))
        for lattice in tqdm.tqdm(lattices, total=1/inv_Z, desc=f"T = {T}"):
            lattice = np.array(lattice).reshape(args.L, args.L)
            energy = compute_total_energy(lattice)
            magnetization = compute_magnetization(lattice)

            # <A> = SUM A*exp(-beta H) / Z
            energy_per_side += energy * np.exp(-beta * energy)
            mag_per_side += abs(magnetization) * np.exp(-beta * energy) 
        
        TMP.append(T)
        ENG.append(energy_per_side * inv_Z / TOTAL)
        MAG.append(mag_per_side * inv_Z)
    
    return TMP, ENG, MAG

def ising_oop(nopython=False):
    TMP, ENG, MAG = list(), list(), list()

    if nopython: # c++ module
        from ising.cpp import Ising
    else: # pure python oop
        from ising.py import Ising
    modell = Ising(args.L)

    for T in range(10, 51):
        kB, T = 1, T/10
        beta = 1 / (kB*T)
        
        energy_per_side, mag_per_side = 0, 0
        lattices = itertools.product(*[(-1,1)]*modell.L2)

        inv_Z = 1/len(list(deepcopy(lattices)))
        for lattice in tqdm.tqdm(lattices, total=1/inv_Z, desc=f"T = {T}"):
            modell.lattice = lattice
            energy = modell.energy
            magnetization = modell.magnetization

            # <A> = SUM A*exp(-beta H) / Z
            energy_per_side += energy * np.exp(-beta * energy)
            mag_per_side += abs(magnetization) * np.exp(-beta * energy) 
        
        TMP.append(T)
        ENG.append(energy_per_side * inv_Z / TOTAL)
        MAG.append(mag_per_side * inv_Z)
    
    return TMP, ENG, MAG


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    # A bit higher computational costs (~10^13 iterations)
    # for i in range(TOTAL + 1):
    #     lattice = np.concatenate((
    #         np.ones(i, dtype=np.int32), # number of spin downs
    #         -np.ones(TOTAL-i, dtype=np.int32) # number of spin up
    #     ))
    #     # lattices.extend(set( itertools.permutations(lattice) ) )
    #     for lattice in set( itertools.permutations(lattice) ):
    #         lattice = np.array(lattice).reshape(args.L, args.L)
    #         print(lattice)
    #         energies.append(compute_total_energy(lattice))
    #         magnetizations.append(compute_magnetization(lattice))

    data = ising_oop(nopython=True)
    data = {
        "temperature": data[0],
        "energy_per_side": data[1],
        "mag_per_side": data[2],
    }
    
    with PdfPages("plots/ising_exact.pdf") as pdf:
        plt.xlabel("Temperature T")
        plt.ylabel("Energy per side e")
        plt.plot(data["temperature"], data["energy_per_side"])
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.xlabel("Temperature T")
        plt.ylabel("Magnetization per side m")
        plt.plot(data["temperature"], data["mag_per_side"])
        pdf.savefig(bbox_inches="tight")
        plt.close()