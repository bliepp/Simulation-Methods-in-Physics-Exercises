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


def avg_after_time(arr, t_eq):
    slic = arr[:int(t_eq/(DT*SAMPLING_STRIDE))]
    return np.nansum(slic)/len(slic)


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
    plt.rcParams.update({"font.size": 14})

    singular = {
        "pressures": "pressure",
        "temperatures": "temperature",
        "energies": "energy"
    }


    with PdfPages("plots/ex_6.pdf") as pdf:
        for observable, invert_y in {
            "pressures": False,
            "temperatures": False,
            "energies": True
            }.items():
            d = data[observable]
            times = np.linspace(0, len(d)*DT*SAMPLING_STRIDE, len(d))

            # plot running averages
            for wsize, color in (
                (0, "tab:blue"),
                (10,"red"), 
                (100, "black"),
                ):
                print(f"Plotting {observable}, M = {wsize}")
                avg = list(running_average(d, wsize))

                plt.xlabel("time t")
                plt.ylabel(f"{singular[observable]}")
                plotsettings = {
                    "label": "Raw observable",
                    "color": color
                    }
                if wsize != 0:
                    plotsettings["label"] = f"M = {wsize}"
                    plotsettings["linewidth"] = 0.5*np.log10(wsize)
                
                plt.plot(times, avg,
                    **plotsettings
                    )

                if invert_y:
                    plt.legend(loc="upper right")
                else:
                    plt.legend(loc="lower right")

            pdf.savefig(bbox_inches="tight")
            plt.close()

            print(f"Plotting average of {observable}")
            # plot average
            avg = np.empty_like(times)
            for i in range(1, len(times)):
                avg[i] = avg_after_time(d, times[i])
        
            plt.xlabel("time t")
            plt.ylabel(f"average {singular[observable]}")
            plt.plot(times, avg)
            pdf.savefig(bbox_inches="tight")
            plt.close()


