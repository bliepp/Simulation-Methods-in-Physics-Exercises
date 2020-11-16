#!/usr/bin/env python3
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

def lowpass(index, value, threshold):
    if abs(index) < threshold:
        return value
    return 0

data = np.loadtxt("outfiles/ex_3_2_symeul.out")
t, x, y = data[:,0], data[:,5]-data[:,3], data[:,6]-data[:,4]
freq = np.fft.fftfreq(t.size, d=t[1]-t[0])

fft_x = np.fft.fft(x)
fft_x_filtered = np.array([lowpass(f, _x, 5) for f, _x in zip(freq,fft_x)])
ifft_x = np.fft.ifft(fft_x_filtered).real

fft_y = np.fft.fft(y)
fft_y_filtered = np.array([lowpass(f, _y, 5) for f, _y in zip(freq, fft_y)])
ifft_y = np.fft.ifft(fft_y_filtered).real


with open("outfiles/ex_3_2_fourier.out", "w") as outfile:
    outfile.write("#t\tx_filtered\ty_filtered\n")
    for _t, _x, _y in zip(t, ifft_x, ifft_y):
        outfile.write("{:.2f}\t{:.5f}\t{:.5f}\n".format(_t, _x, _y))
