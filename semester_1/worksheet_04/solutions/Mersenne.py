import numpy as np
import matplotlib.pyplot as plt

x = []
mu,sigma = 1,4

def BoxMuller():

    N=10000

    for i in range(N):

        u1 = np.random.rand()
        u2 = np.random.rand()

        n1 = np.sqrt(-2*np.log(u1))*np.cos(1*np.pi*u2)
        n1 = mu + sigma*n1
        #n2 = np.sqrt(-2*np.log(u1))*np.sin(1*np.pi*u2)

        x.append(n1)

def box_muller(mu=0, sigma=1):
    while True:
        u1 = np.random.rand()
        u2 = np.random.rand()
        n1 = np.sqrt(-2*np.log(u1))*np.cos(1*np.pi*u2)
        n2 = np.sqrt(-2*np.log(u1))*np.sin(1*np.pi*u2)

        yield mu + sigma*n1
        yield mu + sigma*n2

#BoxMuller()

def Gaussian():
    
    N = 100000

    v = []
    rng = box_muller()

    for i in range(N):

        vx_n = next(rng)
        vy_n = next(rng)
        vz_n = next(rng)

        v_abs = (np.sqrt(vx_n**2 + vy_n**2 + vz_n**2))**2

        v.append(v_abs)


    return v



def normal(x):
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-1/2*((x-mu)/sigma)**2)

def MB(x):
    return  4*np.pi*(1/(2*np.pi))**(3/2) * x**2 * np.exp(-x**2/2)

n = np.linspace(0,15,100)

def plot():
    plt.hist(Gaussian(), 50, density=True, facecolor='purple', alpha=0.75,label='RNG')
    plt.plot(n,MB(n),markersize='0',linestyle='solid',color='black',label='Theory curve')
    plt.xlabel(r'X')
    plt.ylabel(r'Y')
    plt.grid(alpha=0.7,linestyle=":")
    #plt.legend(markerfirst=True,shadow=True)
    plt.tight_layout()
    #plt.savefig("BoxMueller.pdf",format="pdf")
    plt.show()
    
plot()