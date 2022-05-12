#basic hill climbing search provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson
#date revised: 3/26/2021

#NOTE: YOU MAY CHANGE ALMOST ANYTHING YOU LIKE IN THIS CODE.
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generator
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Student name:
#Date:


#need some python libraries
from random import Random   #need this for the random number generation -- do not change
import numpy as np


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
    value.append(round(myPRNG.triangular(150,2000,500),1))

weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(8,300,95),1))

#define max weight for the knapsack
maxWeight = 2500

#change anything you like below this line ------------------------------------
#some of the provided functions are intetionally incomplete
#also, you may wish to restructure the approach entirely -- this is NOT the world's best Python code


#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):

    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)

    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        return [-1,-1]

    return [totalValue, totalWeight]   #returns a list of both total value and total weight


#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x
def neighborhood(x):

    nbrhood = []

    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1

    return nbrhood


def double_flip(x):
    nbrhood = []

    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:      #If value == 1
            nbrhood[i][i] = 0       #Set to 0
        else:
            nbrhood[i][i] = 1       #If value 0, set to 1
        if nbrhood[i][(i+1)%n] == 1: #Repeat logic on i+1 index
            nbrhood[i][(i+1)%n] = 0  #Set to 0
        else:
            nbrhood[i][(i+1)%n] = 1 #If value 0, set to 1

    return nbrhood



def swap_nbr(x):
    nbr = []
    for i in range(n):
        y = x[:]
        if x[i]==1:             #If 1st item in knapsack
            for j in range(n):
                if x[j]==0:     #If 2nd item not in knapsack
                    y[i]=0      #Take out 1st item
                    y[j]=1      #Put in 2nd item
                    nbr.append(y)   #Add solution to neighborhood
    return nbr


#create the initial solution
def initial_solution(k=1):  #k variable helps avoid repition of "pseudo-random code"
    x=[0 for i in range(n)] #start with empty knapsack
    for i in range(myPRNG.randint(0,n)): #add random number of items
        j = myPRNG.randint(0,n) #get random index
        j = (j*k)%n #instance specific (for random-start problem)
        x[j] = 1    #add that item to knapsack

    if evaluate(x)[1]==-1:  #Check for valid solution
        x = initial_solution((k+1)*k)   #if not, get valid solution

    return x

def ratio_based_initial_solution():
    #Start with empty knapsack
    x = [0 for i in range(n)]
    y = x[:]
    #Calculate value:weight
    ratios = [value[i]/weights[i] for i in range(n)]
    track = ratios[:]
    #Add best ratio items until weight limit reached
    w = 0
    done = False
    while not done:
        i = track.index(max(ratios))
        w += weights[i]
        y[i] = 1
        ratios.pop(ratios.index(max(ratios)))
        if evaluate(y)[0] != -1:
            x = y[:]
        else:
            done = True
    return x





#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution
x_best = x_curr[:]           #x_best will hold the best solution
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]
print(f"Initial best is v = {f_best[0]}, w = {f_best[1]}")



#begin local search overall logic ----------------
done = 0

while done == 0:

    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr

    for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best[0]:
            x_best = s[:]                 #find the best member and keep track of that solution
            f_best = evaluate(s)[:]       #and store its evaluation

    if f_best == f_curr:               #if there were no improving solutions in the neighborhood
        done = 1
    else:
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best[:]         #evalute the current solution

        print ("\nTotal number of solutions checked: ", solutionsChecked)
        print ("Best value found so far: ", f_best)

print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
