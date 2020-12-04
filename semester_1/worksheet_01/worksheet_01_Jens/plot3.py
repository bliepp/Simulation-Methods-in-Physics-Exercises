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

filename1="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_2_step_euler.txt"
filename2="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_2_step_symplectic_euler.txt"
filename3="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_3_2_step_velocity_verlet.txt"

t1 = np.genfromtxt(filename1,usecols=(0),skip_header=0,delimiter='\t')
t2 = np.genfromtxt(filename2,usecols=(0),skip_header=0,delimiter='\t')
t3 = np.genfromtxt(filename3,usecols=(0),skip_header=0,delimiter='\t')

x_earth1 = np.genfromtxt(filename1,usecols=(3),skip_header=0,delimiter='\t')
y_earth1 = np.genfromtxt(filename1,usecols=(4),skip_header=0,delimiter='\t')
x_Moon1 = np.genfromtxt(filename1,usecols=(5),skip_header=0,delimiter='\t')
y_Moon1 = np.genfromtxt(filename1,usecols=(6),skip_header=0,delimiter='\t')

x_earth2 = np.genfromtxt(filename2,usecols=(3),skip_header=0,delimiter='\t')
y_earth2 = np.genfromtxt(filename2,usecols=(4),skip_header=0,delimiter='\t')
x_Moon2 = np.genfromtxt(filename2,usecols=(5),skip_header=0,delimiter='\t')
y_Moon2 = np.genfromtxt(filename2,usecols=(6),skip_header=0,delimiter='\t')

x_earth3 = np.genfromtxt(filename3,usecols=(3),skip_header=0,delimiter='\t')
y_earth3 = np.genfromtxt(filename3,usecols=(4),skip_header=0,delimiter='\t')
x_Moon3 = np.genfromtxt(filename3,usecols=(5),skip_header=0,delimiter='\t')
y_Moon3 = np.genfromtxt(filename3,usecols=(6),skip_header=0,delimiter='\t')


def plot2():
    #plt.xlim(-0.06,0.06)
    #plt.ylim(-0.06,0.06)
    plt.plot(x_Moon1-x_earth1,y_Moon1-y_earth1,label="Euler Step",markersize=0,linestyle='solid')
    plt.plot(x_Moon2-x_earth2,y_Moon2-y_earth2,label="Symp. Euler",markersize=0,linestyle='solid')
    plt.plot(x_Moon3-x_earth3,y_Moon3-y_earth3,label="Vel. Verlet",markersize=0,linestyle='solid')
    plt.xlabel("x [au]")
    plt.ylabel("y [au]")
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(loc='best',markerfirst=True,shadow=True)
    plt.tight_layout()
    plt.savefig("/home/jens/Desktop/SimMeth/Exercise1/outfiles/3_2_Moon.pdf",format='pdf')
    plt.show()

plot2()