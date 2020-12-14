import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy.ma as ma
from cycler import cycler
import os
#import seaborn as sns
#import pandas as pd
#import lmfit as lm


def latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """


    assert(columns in [1,2])

    default_cycler =  (cycler(marker=["o","s","D","^","p","P"]) +
                    cycler(linestyle=['None','None','None','None',"None","None"]) +
                    cycler(color=["#000000","#8A2BE2","#3399ff","#f05053","#00b75b","#daa520"]))

    if fig_width is None:
        fig_width = 3.39 if columns==1 else 6.9 # width in inches

    if fig_height is None:
        golden_mean = (np.sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              #'text.latex.preamble': ['\usepackage{gensymb}'],
              'axes.labelsize': 15, # fontsize for x and y labels (was 10)
              'axes.titlesize': 15,
              'font.size': 15,
              'legend.handlelength': 1,
              'legend.handletextpad': 0.4,
              'legend.frameon': True,
              'legend.markerscale': 1,
              'legend.fontsize': 10,
              'xtick.labelsize': 15,
              'ytick.labelsize': 15,
              #'text.usetex': True,
              #'axis.grid': True,
              'grid.linestyle': ':',
              'grid.alpha': 0.7,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif',
              'mathtext.fontset':'cm',
              "axes.prop_cycle": default_cycler,
    }

    mpl.rcParams.update(params)

latexify(None,None,2)

filename="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_2_step_symplectic_euler.txt"

t = np.genfromtxt(filename,usecols=(0),skip_header=0,delimiter='\t')
x_sun = np.genfromtxt(filename,usecols=(1),skip_header=0,delimiter='\t')
y_sun = np.genfromtxt(filename,usecols=(2),skip_header=0,delimiter='\t')
x_earth = np.genfromtxt(filename,usecols=(3),skip_header=0,delimiter='\t')
y_earth = np.genfromtxt(filename,usecols=(4),skip_header=0,delimiter='\t')
x_Moon = np.genfromtxt(filename,usecols=(5),skip_header=0,delimiter='\t')
y_Moon = np.genfromtxt(filename,usecols=(6),skip_header=0,delimiter='\t')
x_Mars = np.genfromtxt(filename,usecols=(7),skip_header=0,delimiter='\t')
y_Mars = np.genfromtxt(filename,usecols=(8),skip_header=0,delimiter='\t')
x_Venus = np.genfromtxt(filename,usecols=(9),skip_header=0,delimiter='\t')
y_Venus = np.genfromtxt(filename,usecols=(10),skip_header=0,delimiter='\t')
x_Jupiter = np.genfromtxt(filename,usecols=(11),skip_header=0,delimiter='\t')
y_Jupiter = np.genfromtxt(filename,usecols=(12),skip_header=0,delimiter='\t')

def plot2():
    plt.ylim(-1.5,4)
    plt.plot(x_earth,y_earth,label="Earth",markersize=0.1,linestyle='solid')
    plt.plot(x_Moon,y_Moon,label="Moon",markersize=0.1,linestyle='solid')
    plt.plot(x_sun,y_sun,label="Sun",markersize=0.1,linestyle='solid')
    plt.plot(x_Mars,y_Mars,label="Mars",markersize=0.1,linestyle='solid')
    plt.plot(x_Venus,y_Venus,label="Venus",markersize=0.1,linestyle='solid')
    plt.plot(x_Jupiter,y_Jupiter,label="Jupiter",markersize=0.1,linestyle='solid')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(loc='best',markerfirst=True,shadow=True)
    plt.tight_layout()
    plt.savefig("/home/jens/Desktop/SimMeth/Exercise1/outfiles/3_2_symplectic_euler.pdf",format='pdf')
    plt.show()

plot2()