#the intial framework for a binary GA
#author: Charles Nicholson
#for ISE/DSA 5113

#need some python libraries
import copy
import math
from random import Random
import numpy as np

#to setup a random number generator, we will specify a "seed" value
seed = 5113
myPRNG = Random(seed)

#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132021
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    #value.append(round(myPRNG.expovariate(1/500)+1,1))
    value.append(round(myPRNG.triangular(150,2000,500),1))

weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(8,300,95),1))

#define max weight for the knapsack
maxWeight = 2500


#change anything you like below this line ------------------------------------

#Student name(s):
#Date:

#monitor the number of solutions evaluated
solutionsChecked = 0


populationSize = 1000 #size of GA population
Generations = 1000   #number of GA generations

crossOverRate = 0.7  #currently not used in the implementation; neeeds to be used.
mutationRate = 0.02  #currently not used in the implementation; neeeds to be used.
elitePercent = .2    #currently not used in the implementation; neeed to use some type of elitism


#create an continuous valued chromosome
def createChromosome(d):
    x=[0 for i in range(d)] #start with empty knapsack
    for i in range(myPRNG.randint(0,d)): #add random number of items
        j = myPRNG.randint(0,d-1) #get random index
        x[j] = 1    #add that item to knapsack

    return x


#create initial population by calling the "createChromosome" function many times and adding each to a list of chromosomes (a.k.a., the "population")
def initializePopulation(): #n is size of population; d is dimensions of chromosome
    population = []
    populationFitness = []

    for i in range(populationSize):
        population.append(createChromosome(n))
        populationFitness.append(evaluate(population[i]))

    tempZip = zip(population, populationFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True)

    #the return object is a reversed sorted list of tuples:
    #the first element of the tuple is the chromosome; the second element is the fitness value
    #for example:  popVals[0] is represents the best individual in the population
    #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3

    return popVals

#implement a crossover
def crossover(x1,x2):
    #i.e. two parents (x1 and x2) should produce two offsrping (offspring1 and offspring2)
    offspring1 = []
    offspring2 = []
    #with some probability (i.e., crossoverRate) perform breeding via crossover
    if myPRNG.random() < crossOverRate:
        p = myPRNG.randint(0,len(x1)) #get split point
        # --- the first part of offspring1 comes from x1, and the second part of offspring1 comes from x2
        # --- the first part of offspring2 comes from x2, and the second part of offspring2 comes from x1
        for i in range(0,p):
            offspring1.append(x1[i])
            offspring2.append(x2[i])
        for i in range(p,len(x1)):
            offspring1.append(x2[i])
            offspring2.append(x1[i])

    #if no breeding occurs, then offspring1 and offspring2 can simply be copies of x1 and x2, respectively
    else:
        offspring1 = x1
        offspring2 = x2

    return offspring1, offspring2  #two offspring are returned


#function to compute the weight of chromosome x
def calcWeight(x):

    a=np.array(x)
    c=np.array(weights)

    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    return totalWeight   #returns total weight


#function to determine how many items have been selected in a particular chromosome x
def itemsSelected(x):

    a=np.array(x)
    return np.sum(a)   #returns total number of items selected



#function to evaluate a solution x
def evaluate(x):

    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)

    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        #returns negative, but also relative to solutions value
        #this way with 2 solutions 1 pound over that with better value has higher fitness
        #but all infeasible answers are negative
        fitness = (maxWeight-totalWeight)/totalValue

    else:
        fitness  = totalValue

    return round(fitness,2)   #returns the chromosome fitness




#performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
#function returns the mating pool with size equal to the initial population
def tournamentSelection(pop,k):
    #randomly select k chromosomes; the best joins the mating pool
    matingPool = []

    while len(matingPool)<populationSize:

        ids = [myPRNG.randint(0,populationSize-1) for i in range(k)]
        competingIndividuals = [pop[i][1] for i in ids]
        bestID=ids[competingIndividuals.index(max(competingIndividuals))]
        matingPool.append(pop[bestID][0])

    return matingPool


def rouletteWheel(pop):
    matingPool = []
    tempPop = pop[:] #copy of population

    total_rank = sum(range(populationSize)) #Sum of 0-149
    p = [(populationSize-i)/total_rank for i in range(1,populationSize+1)] #Calculate % chance for each rank
    picks = np.random.choice(range(populationSize),populationSize,p=p) #Pick i with probabilty p[i] 150 times
    matingPool = [tempPop[i][0] for i in picks] #Get mating pool with repeats

    return matingPool


#function to mutate solutions
def mutate(x):
    if myPRNG.random() < mutationRate:
        #Random 1 flip
        i = myPRNG.randint(0,len(x)-1)
        if x[i] == 1:
            x[i] = 0
        else:
            x[i] = 1

    return x




#breeding -- uses the "mating pool" and calls "crossover" function
def breeding(matingPool):
    #the parents will be the first two individuals, then next two, then next two and so on

    children = []
    childrenFitness = []
    for i in range(0,populationSize-1,2):
        child1,child2=crossover(matingPool[i],matingPool[i+1])

        child1=mutate(child1)[:]
        child2=mutate(child2)[:]

        children.append(child1)
        children.append(child2)

        childrenFitness.append(evaluate(child1))
        childrenFitness.append(evaluate(child2))

    tempZip = zip(children, childrenFitness)

    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True)

    #the return object is a sorted list of tuples:
    #the first element of the tuple is the chromosome; the second element is the fitness value
    #for example:  popVals[0] is represents the best individual in the population
    #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    #print(f"popvals[0]: {popVals[0]}")
    return popVals


#insertion step
def insert(pop,kids):
    new_pop = []        #to store answer
    temp_pop = pop[:]   #get a copy of population
    temp_kids = kids[:] #get copy of kids
    while len(new_pop) < populationSize:
        if myPRNG.random() < elitePercent:  #with probabilty set above
            new_pop.append(temp_pop[0][:])  #add the best remaining element from population
            temp_pop.pop(0)                 #remove that element
        else:
            new_pop.append(temp_kids[0][:]) #add best remaining solution from kids
            temp_kids.pop(0)                #remove that solution

    popVals = sorted(new_pop, key=lambda new_pop: new_pop[1], reverse = True)

    return popVals



#perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
def summaryFitness(pop):
    a=np.array(list(zip(*pop))[1])
    return np.max(a), np.mean(a), np.min(a), np.std(a)


#the best solution should always be the first element...
def bestSolutionInPopulation(pop):
    print ("Best solution: ", pop[0][0])
    print ("Items selected: ", itemsSelected(pop[0][0]))
    print ("Value: ", pop[0][1])
    print ("Fitness: ", evaluate(pop[0][0])) #Debug
    print ("Weight: ", calcWeight(pop[0][0]))
    print ("Max Val: ", max([evaluate(x[0]) for x in pop]))



def main():
    #GA main code
    Population = initializePopulation()

    for j in range(Generations):
        mates=rouletteWheel(Population)  #<--need to replace this with roulette wheel selection, e.g.:  mates=rouletteWheel(Population)
        Offspring = breeding(mates)
        Population = insert(Population, Offspring)
        #end of GA main code
        maxVal, meanVal, minVal, stdVal=summaryFitness(Population)          #check out the population at each generation
        print("Iteration: ", j, summaryFitness(Population))                 #print to screen; turn this off for faster results



    print (summaryFitness(Population))
    bestSolutionInPopulation(Population)


if __name__ == "__main__":
    main()
