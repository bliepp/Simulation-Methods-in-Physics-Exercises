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
    _v = [vs.reshape(-1, 3) for vs in v]
    avg = np.array([np.sqrt(sum(sum(vs)**2)) for vs in _v])
    return avg

with gzip.open(args.file, 'rb') as fp:
    data = pickle.load(fp)

fitfunc = lambda x, a: a*np.ones_like(x)
popt,pcov = opt.curve_fit(fitfunc, data[5], data[7])

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
        plt.plot(data[5],fitfunc(data[5],*popt),label='Average = {:.5f}'.format(popt[0]),linewidth=1,color='tab:red')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.xlabel("average velocity v")
        plt.ylabel("distribution")

        avg = average_velocities(data[8])
        xrange = np.linspace(0, 50, 1000)
        plt.hist(
            avg, 150,# range=(xrange[0], xrange[-1]),
            density=True, facecolor='tab:blue', alpha=0.75,
            label='Simulation Results')
        plt.plot(
            xrange,
            0.003*MB(xrange, 5, np.sqrt(2*T*GAMMA_LANGEVIN/DT)),
            linewidth='0.7', color='tab:red',
            label='Theoretical MB')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()


