import matplotlib.pyplot as plt

# bad random Number generator
def LCG(seed = 0):
    a = 1103515245
    c = 12345
    m = 1 << 32 # 2**32, bit shifted magic
    random = seed
    while True:
        random = (a * random + c) % m
        yield random/m


# random Walk
def walk(N):
    x = 0
    y = 0

    steps = [x]
    positions = [y]
    
    for i in range (1,N+1):
        x += 1
        y +=  LCG(1337) - 0.5

        steps.append(x)
        positions.append(y)

    return [steps, positions]


def plot(data):
    plt.figure(0)
    plt.plot(dat[0],dat[1],markersize='0',linestyle='solid')
    plt.xlabel(r'Steps')
    plt.ylabel(r'Position')
    plt.grid(alpha=0.7,linestyle=":")
    #plt.legend(markerfirst=True,shadow=True)
    plt.tight_layout()
    plt.savefig("RWalk.pdf",format="pdf")
    plt.show()

if __name__ == "__main__":
    plot(walk(1000))


