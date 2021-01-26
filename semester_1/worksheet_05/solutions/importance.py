#!/usr/bin/env python
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from sampling import metropolis


parser = argparse.ArgumentParser()
parser.add_argument('--plot', help="Exercise 3", action="store_true")
parser.add_argument('--acceptance', help="Exercise 3", action="store_true")
args = parser.parse_args()


def distribution(x):
    return np.exp(-x*x)/np.sqrt(np.pi)


def plot_metropolis():
    with PdfPages("plots/importance.pdf") as pdf:
        for dx in (0.1, 1.0, 10.0, 100.0):
            samples = metropolis(
                100_000, distribution,
                lambda phi: phi + np.random.uniform(-dx, +dx),
                0.0
                )

            if args.acceptance:
                print(f"dx = {dx}:\t{samples[1]}")

            if args.plot:
                x_range = np.linspace(-5, 5, 1000)
                plt.xlabel("x")
                plt.ylabel("f(x)")
                plt.hist(samples[0], 50, density=True, facecolor='tab:blue', alpha=0.75, label=f'dx = {dx}')
                plt.plot(x_range, distribution(x_range), label=r"$\exp(-x^2)/\sqrt{\pi}$", color='tab:red')
                plt.legend()
                pdf.savefig(bbox_inches="tight")
                plt.close()


if __name__ == "__main__":
    plot_metropolis()