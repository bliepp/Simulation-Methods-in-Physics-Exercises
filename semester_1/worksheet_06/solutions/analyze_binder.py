#!/usr/bin/env python
import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

paths = [
    ("L_4_binder.dat.gz", "tab:blue"),
    ("L_16_binder.dat.gz", "tab:green"),
    ("L_32_binder.dat.gz", "tab:orange"),
    ]


def plot(pdf):
    plt.xlabel(r"Temperature $T$")
    plt.ylabel(r"Binder $U$")

    for path, color in paths:
        data = load_data(path)
        plt.plot(data["TMP"], data["BIN"], '.-', linewidth=0.7, label=f"L = {data['L']}", color=color)

    plt.grid(alpha=0.7,linestyle=":")
    plt.legend()
    pdf.savefig(bbox_inches="tight")
    plt.close()


def load_data(path):
    with gzip.open(path, "rb") as f:
        return pickle.load(f)
    return dict()


if __name__ == "__main__":
    with PdfPages("plots/exercise4_1.pdf") as pdf:
        plot(pdf)