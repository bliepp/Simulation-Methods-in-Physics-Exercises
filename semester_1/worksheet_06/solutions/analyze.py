#!/usr/bin/env python
import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

paths = [
    ("L_64_metropolis.dat.gz", "tab:orange"),
    ("L_16_metropolis.dat.gz", "tab:green"),
    ("L_4_metropolis.dat.gz", "tab:grey"),
    ("L_4_exact.dat.gz", "tab:blue"),
    ]


def plot(pdf, mode, label):
    plt.xlabel(r"Temperature $T$")
    plt.ylabel(label)

    for path, color in paths:
        data = load_data(path)
        plt.errorbar(data["TMP"], data[mode][0], data[mode][1], None, '.', capsize= 1.4, linewidth=0.7, label=f"L = {data['L']}, {data['METHOD']}", color=color)
    
    if mode == "MAG":
        xrange = np.linspace(1, 2.275, 41_000)
        func = lambda T: np.power((1-np.sinh(2/T)**(-4)), 1/8)
        plt.plot(xrange, func(xrange), label="Analytical Solution", linewidth=0.7, linestyle='solid', color="tab:red")
    
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