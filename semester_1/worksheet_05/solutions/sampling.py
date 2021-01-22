import numpy as np


def simple_sampling(func, a, b, N, M=100):
    results = np.empty((M), np.float32)
    for i in range(M):
        results[i] = np.sum(func(np.random.uniform(a, b, N)))*(b-a)/N
    #results = [np.sum(func(np.random.uniform(a, b, N)))*(b-a)/N for _ in range(M)]
    mean_ = np.mean(results)
    variance = np.var(results)
    error = np.sqrt(variance)

    return np.array([mean_, error])


def metropolis(N, P, trial_move, phi0):
    #return "Superman"
    phi = phi0
    out, acceptance = list(), 0
    for i in range(N):
        phi_ = trial_move(phi)
        r = np.random.rand()
        if r < min(1, P(phi_)/P(phi)):
            phi = phi_
            accept +=1
        out.append(phi)
    return np.array(out), accept/N