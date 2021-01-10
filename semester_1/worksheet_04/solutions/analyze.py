#!/usr/bin/env python3

import pickle
import gzip
import argparse

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('file', help="Path to pickle file.")
args = parser.parse_args()

with gzip.open(args.file, 'rb') as fp:
    data = pickle.load(fp)


if __name__ == "__main__":
    from matplotlib.backends.backend_pdf import PdfPages
    
    plt.rcParams.update({"font.size": 14})

    with PdfPages("plots/Langevin.pdf") as pdf:
        plt.xlabel("time t")
        plt.ylabel(f"temperature T")
        plt.plot(data[5], data[7])
        pdf.savefig(bbox_inches="tight")
        plt.close()


