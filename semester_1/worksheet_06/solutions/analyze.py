#!/usr/bin/env python
import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

paths = [
    ("L_64_metropolis_N_100000.dat.gz", "tab:orange"),
    ("L_16_metropolis_N_100000.dat.gz", "tab:green"),
    #("L_4_metropolis_N_100000.dat.gz", "tab:grey"),
    ("L_4_exact.dat.gz", "tab:blue"),
    ]


def analytical_magnetization():
    kwargs = dict(
        linewidth=0.7, linestyle='solid', color="tab:red")
    
    T_1 = np.linspace(1.0, 2/(np.log(1+np.sqrt(2))), 1000)
    T_2 = np.linspace(2/(np.log(1+np.sqrt(2))), 5.1, 1000)
    plt.plot(T_1, (1-np.sinh(2/T_1)**(-4))**(1./8), label=r'L$\rightarrow \infty$, analytically', **kwargs)
    plt.plot(T_2, np.zeros_like(T_2), **kwargs)


def plot(pdf, mode, label):
    plt.xlabel(r"Temperature $T$")
    plt.ylabel(label)

    for path, color in paths:
        data = load_data(path)
        plt.errorbar(data["TMP"], data[mode][0], data[mode][1], None, '.-', capsize= 1.4, linewidth=0.7, label=f"L = {data['L']}, {data['METHOD']}", color=color)
    
    if mode == "MAG":
        analytical_magnetization()
    
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend()
    pdf.savefig(bbox_inches="tight")
    plt.close()


def load_data(path):
    with gzip.open(path, "rb") as f:
        return pickle.load(f)
    return dict()


if __name__ == "__main__":
    with PdfPages("plots/exercise3.pdf") as pdf:
        plot(pdf, mode="MAG", label=r"Mean Magnetization $m$")
        plot(pdf, mode="ENG", label=r"Mean Energy $e$")