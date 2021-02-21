#!/usr/bin/env python
import tqdm
import itertools
import gzip
import pickle
import numpy as np
from ising import Ising


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

        for T in tqdm.tqdm(range(10, 51), desc=f"(Metro L={L:02}) "):
            e, m = np.empty(500, dtype=float), np.empty(500, dtype=float)
            for i in range(500):
                model.randomize()
                _, e[i], m[i] = model.metropolis(500, 10.0/T)

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
    for L, method in [(4, exact), (16, metropolis), (64, metropolis)]:
        save(L, method.__name__, *method(L))