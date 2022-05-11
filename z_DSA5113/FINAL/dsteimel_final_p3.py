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
import math


#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132021
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#change anything you like below this line ------------------------------------
#some of the provided functions are intetionally incomplete
#also, you may wish to restructure the approach entirely -- this is NOT the world's best Python code


#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
    x1 = x[0]
    x2 = x[1]

    return x1*math.cos(x1)*math.sin(x2)+.5*x2


#Provided neighborhood
def neighborhood(x):
    x1 = x[0]
    x2 = x[1]
    nbrhood = [[x1+1, x2], [x1-1, x2], [x1, x2+1], [x1, x2-1]]

    return nbrhood


#create the initial solution
def initial_solution():
    x = [-1, -3]

    return x

#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution
x_best = x_curr[:]           #x_best will hold the best solution
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton
f_best = f_curr
b = [-3, -1]


#begin local search overall logic ----------------
done = 0

while done == 0:

    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr

    for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s) < f_best:
            x_best = s[:]                 #find the best member and keep track of that solution
            f_best = evaluate(s)          #and store its evaluation

    distances = [math.pow(math.pow(n[0]-b[0],2) + math.pow(n[1]-b[1],2), .5) for n in Neighborhood]
    min_dist = min(distances)
    next_x = Neighborhood[distances.index(min_dist)]
    x_curr = next_x

    if b == x_curr:               #if there were no improving solutions in the neighborhood
        done = 1
    else:

        #x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution

    print ("\nTotal number of solutions checked: ", solutionsChecked)
    print ("Solutions checked this iteration: ", Neighborhood)
    print ("Next position: ", x_curr)
    print ("Best value found so far: ", f_best)
    print ("Best solution fo far: ", x_best)
    print ("Reached B: ", done==1)

print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best)
print ("Best solution: ", x_best)
