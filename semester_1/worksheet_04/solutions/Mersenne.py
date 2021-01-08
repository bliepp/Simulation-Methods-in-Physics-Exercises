import numpy as np
import matplotlib.pyplot as plt

x = []
mu, sigma = 1, 4

def BoxMuller():

    N=10000

    for i in range(N):

        u1 = np.random.rand()
        u2 = np.random.rand()

        n1 = np.sqrt(-2*np.log(u1))*np.cos(1*np.pi*u2)
        n1 = mu + sigma*n1
        #n2 = np.sqrt(-2*np.log(u1))*np.sin(1*np.pi*u2)

        x.append(n1)

BoxMuller()



#x = mu + sigma * np.random.randn(10000)


def normal(n):
    return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-1/2*((n-mu)/sigma)**2)

n = np.linspace(-15,15,100)

def plot():
    plt.figure(0)
    plt.hist(x, 50, density=True, facecolor='purple', alpha=0.75,label='RNG')
    plt.plot(n,normal(n),markersize='0',linestyle='solid',color='black',label='Theory curve')
    plt.xlabel(r'X')
    plt.ylabel(r'Y')
    plt.grid(alpha=0.7,linestyle=":")
    plt.legend(markerfirst=True,shadow=True)
    plt.tight_layout()
    plt.savefig("RWalk.pdf",format="pdf")
    plt.show()
    
plot()