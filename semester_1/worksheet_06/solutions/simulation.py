#!/usr/bin/env python
import tqdm, gzip, pickle
import numpy as np
from ising import Ising


if __name__ == "__main__":
    for N in [16, 64]:
        print(f"Running for {N}*{N} = {N*N} grid size.")
        TEMP, EN, MAG = list(), list(), list()
        model = Ising(N, init=False)

        for T in tqdm.tqdm(range(10, 51)):
            e, m = np.empty(500, dtype=float), np.empty(500, dtype=float)
            for i in range(500):
                model.randomize()
                _, e[i], m[i] = model.metropolis(500, 10.0/T)
            EN.append( (np.mean(e), np.std(e)) )
            MAG.append( (np.mean(m), np.std(m)) )

            TEMP.append(T*0.1)
            MAG.append(ms)
        
        with gzip.open(f"N={N}.dat.gz") as f:
            pickle.dump({
                "TEMP": TEMP,
                "EN": EN,
                "MAG": MAG
            }, f)
        
        