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
        return [maxWeight-totalWeight,maxWeight-totalWeight]

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

#create the initial solution
def initial_solution():
    x=[0 for i in range(n)]              #start with empty knapsack
    for i in range(myPRNG.randint(0,n)): #add random number of items
        j = myPRNG.randint(0,n-1)        #get random index
        x[j] = 1                         #add that item to knapsack

    if evaluate(x)[1]<0:        #Check for valid solution
        x = initial_solution()  #if not, get valid solution

    return x

def initial_temp(nbr, p=.8):
    """
    Calculate T based on min and max values of initial neighborhood.
    Where parameter p is our desired probability to accept even the worst solution.
    """
    vals = [evaluate(x)[0] for x in nbr]
    mx = max(vals)
    mn = min(vals)
    delta = mx-mn
    t = -delta/np.log(p)

    return t

def P(x_current,s2,t):
    """
    Calculate Probability that a worse solution is selected.
    x_current = solution we are comparing to
    s2 = solution we are calculating probabilty P of accepting
    t = current temp
    """

    delta = evaluate(x_current)[0]-evaluate(s2)[0] #Note: our values are switched from lecture because we are searching for max not min
    exponent = -delta/t

    return np.e**exponent

#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution
x_best = x_curr[:]           #x_best will hold the best solution
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]
print(f"Initial best is v = {f_best[0]}, w = {f_best[1]}")

#begin local search overall logic ----------------
Neighborhood = neighborhood(x_curr)
T = initial_temp(Neighborhood, p=.8) #Get initial temp where any solution is accepted with at least .8
init_t = T              #Store value so we can print it (T changes)
M = 20                  #Solutions at each temp
min_t = .1            #Stopping Criterion
cooling_schedule = .95  #Cooling per M iterations
k=0                     #Temp counter
while k < 50000:
    m=0
    while m < M:
        Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
        s = Neighborhood[myPRNG.randint(0,len(Neighborhood)-1)] #get random solution from neighborhood

        if evaluate(s)[0] > f_best[0]:
            x_best = s[:]                 #Store S as best solution
            f_best = evaluate(s)[:]       #and store its evaluation
            x_curr = s[:]                 #Store S as current solution
            f_curr = evaluate(s)[:]       #and store its evaluation

        elif evaluate(s)[0] > f_curr[0]:  #If better than current solution, but not the best
            x_curr = s[:]                 #Store S as current solution
            f_curr = evaluate(s)[:]       #and store its evaluation

        else:                             #If worse than current solution
            a = myPRNG.random()           #get value to compare to P
            if a < P(x_curr,s,T):         #If within our probabilty
                x_curr = s[:]             #set solution as current
                f_curr = evaluate(s)[:]   #and store its evaluation
        solutionsChecked += 1
        m += 1
    #T *= cooling_schedule   #When using alpha*Tk-1 cooling method
    k += 1                  #used in T0/(1+.9k) cooling method
    T = init_t/(1+.9*k)    #T0/(1+.9k)
    print(f"T: {T}    K: {k}     T > {min_t}: {T > min_t}")

print("Initial T:",init_t)
print("# of temps:",k)
print("Iterations:",solutionsChecked)
print("Items Selected:",sum(x_best))
print("Weight:",f_best[1])
print("Value:",f_best[0])
