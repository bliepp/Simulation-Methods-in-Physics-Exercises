#!/usr/bin/env python3

import pickle
import argparse

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('file', help="Path to pickle file.")
args = parser.parse_args()

with open(args.file, 'rb') as fp:
    data = pickle.load(fp)


def avg_after_time(t_eq):
    pass


def running_average(O, M):
    for i in range(len(O)):
        # faster but not as beautiful
        if (i < M) or (i > len(O)-M-1):
            temp_sum = float("nan")
        else:
            temp_sum = np.sum(O[i-M:i+M+1])
            temp_sum /= (2*M+1)

#        # slower but more clear why things work
#        try:
#            temp_sum = np.sum(O[i-M:i+M+1])
#            temp_sum /= (2*M+1)
#        except IndexError:
#            temp_sum = float("nan")

        yield temp_sum


if __name__ == "__main__":
    from matplotlib.backends.backend_pdf import PdfPages

    print(f"There are {len(data['positions'][-1][0])} atoms beeing simulated.")

    DT = data["dt"]
    SAMPLING_STRIDE = data["sampling_stride"]

    singular = {
        "pressures": "pressure",
        "temperatures": "temperature",
        "energies": "energy"
    }


    with PdfPages("plots/ex_5.pdf") as pdf:
        for observable, invert in {
            "pressures": False, #(-0.25,0.42),
            "temperatures": False, #(0.1,0.88),
            "energies": True, #(-145.0,-455.0)
        }.items():
            d = data[observable]
            time = np.linspace(0, len(d)*DT*SAMPLING_STRIDE, len(d))

            for wsize, color in ((10,"tab:blue"), (100, "red")):
                print(f"Plotting {observable}, M = {wsize}")
                avg = list(running_average(d, wsize))

                plt.xlabel("time t")
                plt.ylabel(f"{singular[observable]}")
                plt.plot(time, avg,
                    label=f"M = {wsize}",
                    linewidth=0.5*np.log10(wsize),
                    color=color
                    )

                plt.legend(loc="lower right")

            pdf.savefig()
            plt.close()

