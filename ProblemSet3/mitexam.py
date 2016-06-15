import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 50
CURRENTFOXPOP = 300

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    if CURRENTRABBITPOP < MAXRABBITPOP:
        pRabbitRepro = 1.0 - (CURRENTRABBITPOP/float(MAXRABBITPOP))
        if random.random() <= pRabbitRepro:
            CURRENTRABBITPOP += 1
    
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    # TO DO
    
    pFoxEats = CURRENTRABBITPOP/float(MAXRABBITPOP)
    if (CURRENTRABBITPOP - int(CURRENTFOXPOP * pFoxEats) > 10):
        CURRENTRABBITPOP -= int(CURRENTFOXPOP * pFoxEats)
        CURRENTFOXPOP += int(CURRENTFOXPOP/float(3))
    else :
        if (CURRENTFOXPOP - int(CURRENTFOXPOP/float(10)) > 10):
            CURRENTFOXPOP -= int(CURRENTFOXPOP/float(10))
            
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations = []
    fox_populations = []
    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)
    
    pylab.title('Total')
    pylab.xlabel('Total Fox')
    pylab.ylabel('Total Rabbit')
    #pylab.plot(range(200), rabbit_populations, label = "Rabbit")
    pylab.plot(range(200), fox_populations, label = "Fox")
    extX = pylab.array(range(200))
    a,b,c,d = pylab.polyfit(range(200), rabbit_populations, 3)
    estYVals = a*(extX**3) + b*extX**2 + c*extX + d
    pylab.plot(extX, estYVals, label = 'Cubic fit')
    pylab.legend(loc = 'best')
    
    pylab.legend(loc='upper right')
    pylab.show()
    return (rabbit_populations, fox_populations)
    
print runSimulation(200)

