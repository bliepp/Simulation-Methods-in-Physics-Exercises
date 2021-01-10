import os, time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# bad random Number generator
def LCG(seed=0):
    a = 1103515245
    c = 12345
    m = 1 << 32 # 2**32, bitshifting magic
    current = seed
    while True:
        current = (a * current + c) % m
        yield current/m


# random Walk
def random_walk(N, seed=0):
    rng = LCG(seed)
    steps, positions = [0], [0]

    for i in range (N):
        steps.append(steps[-1] + 1)
        positions.append(positions[-1] + next(rng) - 0.5)

    return [steps, positions]


def plot(filename):
    with PdfPages(filename) as pdf:
        plt.xlabel(r'Steps')
        plt.ylabel(r'Position')
        plt.grid(alpha=0.7,linestyle=":")

        for name, seed in {"Fixed": 1337, "Time": time.time(), "PID": os.getpid()}.items():
            data = random_walk(1000, seed)
            plt.plot(data[0],data[1], label=name + " {}".format(seed), markersize='0', linestyle='solid')

        plt.legend(markerfirst=True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

if __name__ == "__main__":
    plot("plots/RWalk.pdf")
