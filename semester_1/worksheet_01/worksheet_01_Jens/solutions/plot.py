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

    default_cycler =  (cycler(marker=["o","s","D","^","."]) +
                    cycler(linestyle=['None','None','None','None',"None"]) +
                    cycler(color=["#8A2BE2","#3399ff","#f05053","#00b75b","#daa520"])) #"#BB33FF"

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
              'legend.fontsize': 15,
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

filename="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_1_out.txt"
filename2="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_2_f_nw_out.txt"
filename3="/home/jens/Desktop/SimMeth/Exercise1/outfiles/ex_2_2_f_ww_out.txt"

pt = np.genfromtxt(filename,usecols=(0),skip_header=0,delimiter='\t')
px = np.genfromtxt(filename,usecols=(1),skip_header=0,delimiter='\t')
py = np.genfromtxt(filename,usecols=(2),skip_header=0,delimiter='\t')

pt2 = np.genfromtxt(filename2,usecols=(0),skip_header=0,delimiter='\t')
px2 = np.genfromtxt(filename2,usecols=(1),skip_header=0,delimiter='\t')
py2 = np.genfromtxt(filename2,usecols=(2),skip_header=0,delimiter='\t')

pt3 = np.genfromtxt(filename3,usecols=(0),skip_header=0,delimiter='\t')
px3 = np.genfromtxt(filename3,usecols=(1),skip_header=0,delimiter='\t')
py3 = np.genfromtxt(filename3,usecols=(2),skip_header=0,delimiter='\t')

def plot():
    #ax = plt.axes(projection='3d')
    #ax.plot3D(pt, px, py, 'gray')
    #ax.scatter3D(pt, px, py, c=py, cmap='Greens')
    #ax.set_xlabel('time')
    #ax.set_ylabel('length')
    #ax.set_zlabel('height')
    plt.plot(pt,px,label="Length(t)",markersize=0.1)
    plt.plot(pt,py,label="Height(t)",markersize=0.1)
    plt.xlabel("time [s]")
    plt.ylabel("Place [m]")
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(markerfirst=True,shadow=True)
    lgnd = plt.legend(loc="upper right",numpoints=1)
    lgnd.legendHandles[0]._legmarker.set_markersize(6)
    lgnd.legendHandles[1]._legmarker.set_markersize(6)
    plt.tight_layout()
    plt.savefig("/home/jens/Desktop/SimMeth/Exercise1/outfiles/CannonbalTime.pdf",format='pdf')
    plt.show()

def plot2():
    plt.plot(px,py,label="Cannonball",markersize=0.1,linestyle='solid')
    plt.plot(px2,py2,label="Cannonball f nW",markersize=0.1,linestyle='solid')
    plt.plot(px3,py3,label="Cannonball f wW",markersize=0.1,linestyle='solid')
    plt.xlabel("Length [m]")
    plt.ylabel("Height [m]")
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(loc='best',markerfirst=True,shadow=True)
    plt.tight_layout()
    plt.savefig("/home/jens/Desktop/SimMeth/Exercise1/outfiles/CannonbalXY.pdf",format='pdf')
    plt.show()

plot()
plot2()