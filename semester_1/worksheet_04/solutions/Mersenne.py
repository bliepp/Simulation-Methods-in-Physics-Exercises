import numpy as np
import matplotlib.pyplot as plt

def BoxMuller(mu=0, sigma=1):
    while True:
        u1 = np.random.rand()
        u2 = np.random.rand()
        n1 = np.sqrt(-2*np.log(u1))*np.cos(1*np.pi*u2)
        n2 = np.sqrt(-2*np.log(u1))*np.sin(1*np.pi*u2)

        yield mu + sigma*n1
        yield mu + sigma*n2

def TaskOne(N=10000):
    rng = BoxMuller()
    output = []

    for i in range(N):
        x = next(rng)
        output.append(x)

    return output

def Gaussian(N=10000):
    rng = BoxMuller()
    output = []

    for i in range(N):
        vx, vy, vz = next(rng), next(rng), next(rng)
        v_abs = np.sqrt(vx*vx + vy*vy + vz*vz)

        output.append(v_abs)

    return output



def normal(x, mu=1, sigma=4):
    return (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-1/2*((x-mu)/sigma)**2)

def MB(x):
    return  4*np.pi*(1/np.sqrt(2*np.pi))**3 * x**2 * np.exp(-x**2/2)

def plot():
    n = np.linspace(0,7,100)

    plt.hist(Gaussian(), 25, density=True, facecolor='purple', alpha=0.75, label='RNG')
    #plt.hist(TaskOne(), 50, density=True, facecolor='purple', alpha=0.75, label='RNG')
    plt.plot(n, MB(n), markersize='0', linestyle='solid', color='black', label='Theory curve')
    plt.xlabel(r'X')
    plt.ylabel(r'Y')
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(markerfirst=True)
    plt.tight_layout()
    plt.savefig("plots/MaxwellBoltzmann.pdf",format="pdf")
    plt.show()

#plot()
