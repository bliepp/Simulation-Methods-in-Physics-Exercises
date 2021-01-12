#!/usr/bin/env python3

import pickle
import gzip
import argparse

import matplotlib.pyplot as plt
import numpy as np

import scipy.optimize as opt
from scipy import integrate

from Mersenne import MB

parser = argparse.ArgumentParser()
parser.add_argument('file', help="Path to pickle file.")
parser.add_argument('--langevin', help="Exercise 5", action="store_true")
parser.add_argument('--msd', help="Exercise 5", action="store_true")
parser.add_argument('--vacf', help="Exercise 5", action="store_true")
args = parser.parse_args()

with gzip.open(args.file, 'rb') as fp:
    data = pickle.load(fp)

GAMMA_LANGEVIN = data[2]
T = data[1]
DT = 0.01


# LANGEVIN STUFF
def average_velocities(v):
    _v = [vs.reshape(-1, 3) for vs in v]
    avg = np.array([np.sqrt(sum(sum(vs)**2)) for vs in _v])
    return avg

def plot_langevin():
    fitfunc = lambda x, a: a*np.ones_like(x)
    popt,pcov = opt.curve_fit(fitfunc, data[5], data[7])
    
    with PdfPages("plots/Langevin.pdf") as pdf:
        plt.xlabel("time t")
        plt.ylabel("temperature T")
        plt.plot(data[5], data[7],label='Simulation Results',linewidth=0.7,color='tab:blue')
        plt.plot(data[5],fitfunc(data[5],*popt),label='Average = {:.5f}'.format(popt[0]),linewidth=1,color='tab:red')
        plt.legend()
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.xlabel("average velocity v")
        plt.ylabel("distribution")

        avg = average_velocities(data[8])
        xrange = np.linspace(0, 20, 1000)
        plt.hist(
            avg, 40,# range=(xrange[0], xrange[-1]),
            density=True, facecolor='tab:blue', alpha=0.75,
            label='Simulation Results')
        plt.plot(
            xrange,
            0.003*MB(xrange, 0.6, 0.55*np.sqrt(2*T*GAMMA_LANGEVIN/DT)),
            linewidth='0.7', color='tab:red',
            label='Theoretical MB')
        plt.legend()
        
        pdf.savefig(bbox_inches="tight")
        plt.close()


# MSD STUFF
def msd(traj, steprange):
    #x = np.array([xs.reshape(-1, 3) for xs in traj])
    for step in steprange:
        var = np.zeros_like(traj[0])
        for i in range(step, len(traj), step):
            var += (abs(traj[i] - traj[i-step])**2)
        msds = var * step/len(traj)
        yield sum(msds)/len(msds)

def compute_msd_konsti(Dt):
    p=0
    N = int(np.floor(4000/Dt))
    for i in range(N):
        p += np.sum((np.array(data[-1][(i)*Dt:(i+1)*Dt,:]) - np.repeat([data[-1][i*Dt,:]],Dt,axis=0))**2)/(150*Dt)
    return p/N

def plot_msd():
    msd_range = range(1, len(data[-1])//8)
    MSD = list(msd( data[-1], msd_range ))
    
    fitfuncdiffusion = lambda x,D,c: 6*D*x+c
    poptdiff,pcovdiff = opt.curve_fit(fitfuncdiffusion,msd_range[10:50],MSD[10:50])
    n = np.linspace(0,msd_range[-1],500)

    with PdfPages("plots/MSD.pdf") as pdf:
        plt.figure(figsize=(7,4))
        plt.xlabel(r"Subtrajectory length $\Delta$t")
        plt.ylabel(r'Mean Square Displacement $\langle\Delta x\rangle^2(\Delta t)$')
        plt.plot(msd_range, MSD,label='Simulation Results',linewidth=0.7,color='tab:blue')
        plt.plot(n, fitfuncdiffusion(n,*poptdiff),label='Theretical Value D = {:.2E}'.format(poptdiff[0]),linewidth=0.7,color='tab:red')
        plt.legend()
        
        pdf.savefig(bbox_inches="tight")
        plt.close()

        plt.figure(figsize=(7,4))
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(r"Subtrajectory length $\Delta$t")
        plt.ylabel(r'Mean Square Displacement $\langle\Delta x\rangle^2(\Delta t)$')
        plt.plot(msd_range, MSD,label='Simulation Results',linewidth=0.7,color='tab:blue')
        plt.legend()
        
        pdf.savefig(bbox_inches="tight")
        plt.close()
        
        plt.figure(figsize=(7,4))
        plt.xlim(0, 10)
        plt.ylim(-1, 3)
        plt.xlabel(r"subtrajectory length $\Delta$t")
        plt.ylabel(r'mean square displacement $\langle\Delta x\rangle^2(\Delta t)$')
        plt.plot([0] + list(msd_range), [0] + MSD,label='Simulation Results',linewidth=0.7,color='tab:blue')
        plt.plot(n, fitfuncdiffusion(n,*poptdiff),label='Theretical Value D = {:.2E}'.format(poptdiff[0]),linewidth=0.7,color='tab:red')
        plt.legend()
        
        pdf.savefig(bbox_inches="tight")
        plt.close()


# VACF STUFF
def VACF(v):
    _v = np.array(v).T
    Ds = list()
    for vs in _v:
        corr = np.correlate(vs, vs, mode="full")
        Ds.append(corr)
    return sum(Ds)/len(Ds)

def plot_vacf():
    v_squared = 3*data[1] * data[0] # v**2 = T*dim*N
    vacf = VACF(data[8])
    vacf *= v_squared/max(vacf)
    
    n = np.linspace(-data[5][-1], data[5][-1], len(vacf))
    D = integrate.trapezoid(vacf[len(vacf)//2+1:], np.linspace(0, data[5][-1], len(vacf)//2))
    print("The via VACF calculated diffusion coefficient is D =", D)

    with PdfPages("plots/VACF.pdf") as pdf:
        plt.figure(figsize=(7,4))
        plt.xlabel(r"time lag $\Delta$t")
        plt.ylabel(r'VACF $\langle v(t) v(0) \rangle$')
        plt.plot(n, vacf,label='Simulation Results',linewidth=0.7,color='tab:blue')

        plt.legend()
        
        pdf.savefig(bbox_inches="tight")
        plt.close()
        


if __name__ == "__main__":
    from matplotlib.backends.backend_pdf import PdfPages
    
    plt.rcParams.update({"font.size": 14})

    if args.langevin:
        plot_langevin()
    
    if args.msd:
        plot_msd()
    
    if args.vacf:
        plot_vacf()


