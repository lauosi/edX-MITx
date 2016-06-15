# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 
#from ps3b_precompiled_27 import *  
import numpy
import random
import pylab
import copy

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """


class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        number = random.random()
        if self.getClearProb() == 0:
            return False
        elif number <= self.getClearProb():
            return True
        return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # probability of virus particle reproduce
        prob = self.maxBirthProb * (1 - popDensity)
        number = random.random()
        # if virus reproduce create new instance instance
        # if not raise an exception
        if prob > 0 and number <= prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        
    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)        

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # get the list of viruses
        listOfViruses = self.getViruses()

        # determine whether each virus survives
        for virus in listOfViruses:
            if virus.doesClear():
                # if do not survive - remove it
                self.viruses.remove(virus)
        newListOfViruses = copy.deepcopy(self.getViruses())

        #if survives try to reproduce
        for virusLeft in newListOfViruses:
            try:
                virusOff = virusLeft.reproduce(float(self.getTotalPop())/self.getMaxPop())
                # check if the population does not extend the maximum value
                if self.getTotalPop() < self.getMaxPop():
                    self.viruses.append(virusOff)
            except NoChildException:
                pass
                
        return self.getTotalPop()
             
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    viruses = []
    # populate the viruses list
    for i in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))

    # keep track of the total number of viruses         
    totalPop = []
    
    for trial in range(numTrials):
        # instantiate the patient
        patient = Patient(viruses, maxPop)
        
        if trial == 0:
            # run simulation for 300 timesteps
            for timeStep in range(300):
                totalPop.append(float(patient.update()))
        else:
            # run simulation for 300 timesteps
            for timeStep in range(300):
                totalPop[timeStep] += patient.update()
                
    # get average virus population            
    for element in totalPop:
        element = (element/numTrials)
    
    getPlot(list(range(300)), totalPop)


def getPlot(time, totalPop):        
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.plot(time, totalPop)
    pylab.legend(loc='upper right')
    pylab.show()
                
#print simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        dic = self.getResistances() 
        if drug in dic.keys():
            return self.getResistances()[drug]
        return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # get the resistances for this virus
        dic = self.getResistances()
        reproduces = True


        for key, value in dic.items():
            # check if is resistant to all drugs
            if (key in activeDrugs) and (value == False):
                reproduces = False
                break
            # mutation - change the resistancy
            if random.random() <= self.getMutProb():
                    if value == True:
                        self.resistances[key] = False
                    else:
                        self.resistances[key] = True
                    
        if not reproduces:
            raise NoChildException
        # if it meets the conditions - reproduce            
        if random.random() <= self.maxBirthProb * (1 - popDensity):          
            return ResistantVirus(self.maxBirthProb, self.clearProb, self.getResistances(), self.getMutProb())
        else:
            raise NoChildException
                            
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.activeDrugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.activeDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        virusesResistTotal = 0

        # check all the viruses if they are resistant to the drugs
        for virus in self.getViruses():
            oneVirusResistence = 0
            #if empty all are resistant
            if drugResist == []:
                return len(self.viruses)
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    oneVirusResistence += 1
            if oneVirusResistence == len(drugResist):
               virusesResistTotal += 1
               
        return virusesResistTotal    
             

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        #update virus population
        for virus in self.getViruses():
            if virus.doesClear():
                self.viruses.remove(virus)
                
        newListOfViruses = copy.deepcopy(self.getViruses())
        # if virus survived check if it reproduces 
        for virusLeft in newListOfViruses:
            try:
                virusOff = virusLeft.reproduce(float(self.getTotalPop())/self.getMaxPop(), self.getPrescriptions())
                if self.getTotalPop() < self.getMaxPop():
                    self.viruses.append(virusOff)
            except NoChildException:
                pass
                
        return self.getTotalPop()


def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    totalPop = []
    totalPopGutt = []
    timesteps = 300

    for trial in range(numTrials):
        viruses = []
        # populate list with viruses
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, copy.deepcopy(resistances), mutProb))

        # instantiate the patient  
        patient = TreatedPatient(viruses, maxPop)

        # if the first trial    
        if trial == 0:
            for timeStep in range(timesteps):
                if timeStep == 150:
                    #apply the drug
                    patient.addPrescription("guttagonol")
                totalPop.append(float(patient.update()))
                totalPopGutt.append(float(patient.getResistPop(["guttagonol"])))
                
        else:
            for timeStep in range(timesteps):
                if timeStep == 150:
                    #apply the drug
                    patient.addPrescription("guttagonol")
                totalPop[timeStep] += patient.update()
                totalPopGutt[timeStep] += patient.getResistPop(["guttagonol"])
                
    totalPop[:] = [x / numTrials for x in totalPop]
    totalPopGutt[:] = [x / numTrials for x in totalPopGutt]                  
    getPlot2(list(range(timesteps)), totalPop, totalPopGutt)

def getPlot2(time, totalPop, totalPopGutt):        
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Populations ')
    pylab.plot(time, totalPop, label = "Average total virus population")
    pylab.plot(time, totalPopGutt, label = "Average population of guttagonol-resistant")
    pylab.legend(loc='upper right')
    pylab.show()

#simulationWithDrug(450, 300, 100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 5)
#simulationWithDrug(300, 150, 100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 5)
#simulationWithDrug(225, 75, 100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 5)
#simulationWithDrug(150, 0, 100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 5)        
#simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
#simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
      
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
        # populate list with viruses
        viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': True}, 0.005) for i in range(100)]
        # instantiate the patient
        patient = TreatedPatient(viruses, 1000)
        for timeStep in range(timesteps):
            if timeStep == prescriptionStep:
                #apply the drug
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
        # populate list with viruses
        viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.05) for i in range(100)]
        # instantiate the patient
        patient = TreatedPatient(viruses, 1000)
        
        for timeStep in range(timesteps):
            #apply two drugs
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
#simulationTwoDrugsDelayedTreatment(300, 150, 150, 10)
