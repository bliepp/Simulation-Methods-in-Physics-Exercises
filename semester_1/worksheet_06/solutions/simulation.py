#!/usr/bin/env python
import tqdm
import itertools
import gzip
import pickle
import argparse
import numpy as np
from ising import Ising


parser = argparse.ArgumentParser()
parser.add_argument("--exact", help="Additionaly run exact simulation for L=4" ,action="store_true")
args = parser.parse_args()


def exact(L=4):
    TMP, ENG, MAG = list(), list(), list()
    model = Ising(L)

    for T in tqdm.tqdm(range(10, 51), desc=f"(Exact L={L:02}) "):
        beta = 10.0 / T
        
        energy_per_side, mag_per_side, partition_function = 0.0, 0.0, 0.0
        lattices = itertools.product(*[(-1,1)]*model.L2)
        length = 1 << (model.L2) # binary representation of lattice -> 2^(L*L) possiblilities

        for lattice in lattices:#tqdm.tqdm(lattices, total=length, desc=f"(Exact)"):
            model.lattice = lattice
            energy = model.energy
            magnetization = model.magnetization

            # <A> = SUM A*exp(-beta H) / Z
            energy_per_side += energy * np.exp(-beta * energy)
            mag_per_side += abs(magnetization) * np.exp(-beta * energy) 
            partition_function += np.exp(-beta * energy)

        TMP.append(T*0.1)
        ENG.append((energy_per_side / partition_function / model.L2, 0))
        MAG.append((mag_per_side / partition_function, 0))
    
    return np.array(TMP), np.array(ENG).T, np.array(MAG).T



def metropolis(L=4):
    TMP, ENG, MAG = list(), list(), list()
    model = Ising(L, init=False)
    MEANS, VALUES = 100, 100_000

    Tc = 2/(np.log(1+np.sqrt(2)))
    for T in tqdm.tqdm(range(10, 51), desc=f"(Metro L={L:02}) "):
        randmax = 1- T*0.1 / (2*Tc)
        e, m = np.empty(MEANS, dtype=float), np.empty(MEANS, dtype=float)
        for i in range(MEANS):

            # Ensure that we reach the important parts for T < Tc
            # --> Fill on average 70% of all lattice points with spin +1
            model.randomize()
            for j in range(model.L2):
                if np.random.random() < randmax:
                    model.set_spin_by_index(j, 1)

            _, e[i], m[i] = model.metropolis(VALUES, 10.0/T)

        TMP.append(T*0.1)
        ENG.append( (np.mean(e), np.std(e)) )
        MAG.append( (np.mean(m), np.std(m)) )

    return np.array(TMP), np.array(ENG).T, np.array(MAG).T



def save(L, method, TMP, ENG, MAG):
    with gzip.open(f"L_{L}_{method}.dat.gz", "wb") as f:
        pickle.dump({
            "L": L,
            "METHOD": method,
            "TMP": TMP,
            "ENG": ENG,
            "MAG": MAG
        }, f)



if __name__ == "__main__":
    runs = []
    if args.exact:
        runs.append((4, exact))
    else:
        runs.append((4, metropolis))
        runs.append((16, metropolis))
        runs.append((64, metropolis))
    
    for L, method in runs:
        save(L, method.__name__, *method(L))