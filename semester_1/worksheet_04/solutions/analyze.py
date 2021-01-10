#!/usr/bin/env python3

import pickle
import gzip
import argparse

import matplotlib.pyplot as plt
import numpy as np

import scipy.optimize as opt

from Mersenne import MB

parser = argparse.ArgumentParser()
parser.add_argument('file', help="Path to pickle file.")
args = parser.parse_args()

def average_velocities(v):
    avg = np.array([np.abs(vs.sum()) for vs in v])
    return avg

with gzip.open(args.file, 'rb') as fp:
    data = pickle.load(fp)

fitfunc = lambda x, a: a*np.ones_like(x)
popt,pcov = opt.curve_fit(fitfunc,data[5],data[7])

#x = np.linspace(0,2000,1000)


if __name__ == "__main__":
    from matplotlib.backends.backend_pdf import PdfPages
    GAMMA_LANGEVIN = data[2]
    DT = 0.01
    T=0.3
    
    plt.rcParams.update({"font.size": 14})

    with PdfPages("plots/Langevin.pdf") as pdf:
        plt.xlabel("time t")
        plt.ylabel(f"temperature T")
        plt.plot(data[5], data[7],label='Simulation Results',linewidth=0.7,color='tab:blue')
        plt.plot(data[5],fitfunc(data[5],*popt),label='Average = {:.2f}'.format(popt[0]),linewidth=1,color='tab:red')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.xlabel("average velocity v")
        plt.ylabel("distribution")

        avg = average_velocities(data[8])
        xrange = np.linspace(460, 550, 1000)
        plt.hist(
            avg, 100, range=(xrange[0], xrange[-1]),
            density=True, facecolor='tab:blue', alpha=0.75,
            label='Simulation Results')
        plt.plot(
            xrange,
            MB(xrange, sum(avg)/(len(avg)), np.sqrt(2*T*GAMMA_LANGEVIN/DT)),
            linewidth='0.7', color='tab:red',
            label='Theoretical MB')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()


