# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *
      
def simulationDelayedTreatment(timesteps, prescriptionStep, numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    totalPop = [0 for s in range(numTrials)]
    
    for trial in range(numTrials):
        viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': True}, 0.005) for i in range(100)]
        patient = TreatedPatient(viruses, 1000)
        for timeStep in range(timesteps):
            if timeStep == prescriptionStep:
                patient.addPrescription("guttagonol")
            populationTrial = patient.update()
        totalPop[trial] = populationTrial
    
    under50 = 0
    for number in totalPop:
        if number < 50:
            under50 += 1
    print under50        
    #getHist(totalPop)
        
                 
def getHist(totalPop):        
    pylab.title('TotalVirus simulation')
    pylab.xlabel('Total Virus Population')
    pylab.ylabel('Number of trials')
    pylab.hist(totalPop, bins = 50)
    #pylab.plot(time, totalPop, label = "Average total virus population")
    #pylab.plot(time, totalPopGutt, label = "Average population of guttagonol-resistant")
    pylab.legend(loc='upper right')
    pylab.show()
   

#simulationDelayedTreatment(150, 0, 500)
#simulationDelayedTreatment(225, 75, 500)
#simulationDelayedTreatment(300, 150, 100)
#simulationDelayedTreatment(450, 300, 00)


def simulationTwoDrugsDelayedTreatment(timesteps, prescriptionStep1, prescriptionStep2, numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    totalPop = [0 for s in range(numTrials)]
    timesteps
    prescriptionStep1
    prescriptionStep2
    
    for trial in range(numTrials):
        viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': True}, 0.005) for i in range(100)]
        patient = TreatedPatient(viruses, 1000)
        for timeStep in range(timesteps):
            if timeStep == prescriptionStep1:
                patient.addPrescription("guttagonol")
            if timeStep == prescriptionStep2:
                patient.addPrescription("grimpex")
            populationTrial = patient.update()
        totalPop[trial] = populationTrial
    
    under50 = 0
    for number in totalPop:
        if number < 50:
            under50 += 1
    print under50        
    #getHist(totalPop)

#simulationTwoDrugsDelayedTreatment(600, 150, 450, 10)
#simulationTwoDrugsDelayedTreatment(450, 150, 300, 10)
#simulationTwoDrugsDelayedTreatment(375, 150, 225, 10)
simulationTwoDrugsDelayedTreatment(300, 150, 150, 10)
