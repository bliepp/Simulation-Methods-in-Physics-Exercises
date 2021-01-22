import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse

from sampling import metropolis


def distribution(x):
    return np.exp(-x*x)/np.sqrt(np.pi)


if __name__ == "__main__":
    with PdfPages("plots/importance.pdf") as pdf:
        for dx in (0.1, 1.0, 10.0, 100.0):
            samples = metropolis(
                100_000, distribution,
                lambda phi: phi + np.random.uniform(-dx, +dx),
                0.0
                )

            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.hist(samples[0], 50, density=True, facecolor='tab:blue', alpha=0.75, label='Metropolis')
            plt.legend()
            pdf.savefig(bbox_inches="tight")
            plt.close()