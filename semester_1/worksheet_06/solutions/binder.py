#!/usr/bin/env python
import tqdm
import itertools
import gzip
import pickle
import numpy as np
from ising import Ising

def binder(L=4):
    TMP, BIN = list(), list()
    model = Ising(L, init=False)
    STEPS = 400_000

    for T in tqdm.tqdm(range(200, 240, 2), desc=f"(Metro L={L:02}) "):
        m = np.empty(STEPS)
        for i in range(STEPS):
            _, _, m[i] = model.metropolis(100, 100.0/T)
        m4 = np.mean(m*m*m*m)
        m2 = np.mean(m*m)
        BIN.append(1 - 0.3333333 * m4/(m2*m2))


        TMP.append(T*0.01)
    
    return np.array(TMP), np.array(BIN)


def save(L, suffix, TMP, BIN):
    with gzip.open(f"L_{L}_{suffix}.dat.gz", "wb") as f:
        pickle.dump({
            "L": L,
            "TMP": TMP,
            "BIN": BIN
        }, f)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    for N in [4, 16, 32]:
        T, U = binder(N)
        save(N, "binder", T, U)
        plt.plot(T, U)
    plt.show()