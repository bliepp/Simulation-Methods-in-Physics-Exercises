import matplotlib.pyplot as plt

#Bad random Number generator
def LCG():
    a = 1103515245
    c = 12345
    m = 2*10**(32)
    LCG.random = (a * LCG.random + c) % m
    return LCG.random/m

LCG.random=1

#Test Generator
#for i in range(10):
#    print(LCG())

#Random Walk

def Walk(N):
    x = 0
    y = 0

    Step = [x]
    position = [y]
    
    for i in range (1,N+1):
        y +=  LCG() - 0.5
        x += 1

        Step.append(x)
        position.append(y)

    return[Step,position]

dat = Walk(1000)

def plot():
        plt.figure(0)
        plt.plot(dat[0],dat[1],markersize='0',linestyle='solid')
        plt.xlabel(r'Steps')
        plt.ylabel(r'Position')
        plt.grid(alpha=0.7,linestyle=":")
        #plt.legend(markerfirst=True,shadow=True)
        plt.tight_layout()
        #plt.savefig("/home/jens/Desktop/GlassTransitions/plots/KoaxRef.pdf",format="pdf")
        plt.show()
    
plot()


