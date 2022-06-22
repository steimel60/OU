import math
from random import Random, choice
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

#--------------------- PSO CLasses -----------------------#
"""
Adjust the Particle or Swarm class here.
"""

class Particle:
    """
    Particle Class built for Particle Swarm Optimization.
    Stores postion, value, and velocity.
    Update method moves the particle and get's its new value.
    """
    def __init__(self, dimensions):
        """
        int dimensions = Length of position array. Ex) 2 = [x,y], 3 = [x,y,z]
        """
        self.start_pos = np.array([myPRNG.uniform(lowerBound,upperBound) for n in range(dimensions)]) #Random val in bounds for each dimension
        self.current_pos = self.start_pos.copy() #Start pos is initial current pos
        self.best_pos = self.start_pos.copy()    #Start pos is initial best pos
        self.velocity = np.array([myPRNG.uniform(-velocityMax,velocityMax) for n in range(dimensions)]) #Random velocity for each direction
        self.current_val = self.evaluate(self.current_pos) #Calculate initial val
        self.best_val = self.evaluate(self.best_pos)       #Initial val is initial best val

    def update_pos(self):
        """
        Move the particles position by adding the current velocity vector.
        Then checks if new position is better than the current best.
        """
        self.current_pos += self.velocity                   #Update position
        self.current_val = self.evaluate(self.current_pos)       #Update value
        if self.current_val < self.best_val:             #If new best
            self.best_pos = self.current_pos.copy()      #Copy position
            self.best_val = self.evaluate(self.best_pos)      #Save best val

    def update_vel(self, best_social_pos):
        """
        Calculates and saves new velocity based.
        """
        r1 = myPRNG.random()    #Generate random value in (0,1)
        r2 = myPRNG.random()    #Generate random value in (0,1)
        #Update Velocity
        self.velocity = inertiaWeight*self.velocity + p1*r1*(self.best_pos-self.current_pos) + p2*r2*(best_social_pos-self.current_pos)
        self.velocity[self.velocity>velocityMax] = velocityMax      #If velocity too high (pos), set to max
        self.velocity[self.velocity<-velocityMax] = -velocityMax    #If velocity too high (min), set to -max

    def evaluate(self, pos):
        """
        Evaluates value of a postion.
        """
        val = 0
        d = len(pos)
        penalty = 0
        for i in range(d):
            val = val + pos[i]*math.sin(math.sqrt(abs(pos[i])))
            if pos[i] < lowerBound:
                penalty += (lowerBound - pos[i])*100
            if pos[i] > upperBound:
                penalty += (pos[i] - upperBound)*100

        val = 418.9829*d - val + penalty

        return val

    def update(self, best_social_pos):
        """
        Move then update velocity.
        """
        self.update_pos()                   #Update position based on current velocity
        self.update_vel(best_social_pos)     #Set next velocity

class Swarm:
    """
    Swarm Class built for Particle Swarm Optimization.
    Stores Particle Class objects in it's population.
    Has methods to iterate through the population and update each Particle's position.
    Stores the global best value and corresponding postion found in the population.
    """
    def __init__(self, size=10, dimensions=2, updateMethod='global', n_neighborhoods=1, **kwargs):
        """
        int size = Number of Particles in the Swarm
        int dimensions = Dimension of each particle
        str updateMethod = Name of desired update method
        int n_neighborhoods = Used in ceratin update methods - number of neighborhoods to create when using local best. Must be less than size.
        """
        self.kwargs = kwargs    #Keyword arguements for update method
        self.population = [Particle(dimensions) for n in range(size)] #Create list of particles
        self.best_val = self.get_best_val(self.population)            #Get first best val
        self.best_pos = self.get_best_pos(self.population)            #Get first best pos
        self.updateMethod = updateMethod                              #Get update method
        self.neighborhoods = self.build_neighborhoods(n_neighborhoods)#Get n neighborhoods

    def get_best_pos(self, particles):
        """
        Finds and returns the best position in a list of particles.
        If multiple positions return the best value, randomly selects from those positions.
        """
        best_val = self.get_best_val(particles) #Get best value of the list

        return choice([p.best_pos.copy() for p in particles if p.best_val == best_val]) #Return copy of best position

    def get_best_val(self, particles):
        """
        Returns the minimum best_val for a passed list of Particles
        """
        return min([p.best_val for p in particles])

    def build_neighborhoods(self, n):
        """
        Returns a list of n subsets of the population.
        It creates each list by starting at indices 1 through n then iterating through the population with step size n.
        Ex) Population = [P1, P2, P3, P4, P5]
            subset_1 = [P1, P3, P5]
            subset_2 = [P2, P4]
            returns [subset_1, subset_2]
        """
        neighborhoods = []
        for i in range(n):
            particles = self.population[i::n]            #Get subset neighborhood
            neighborhoods.append(particles.copy())       #Add to list of neighborhoods

        return neighborhoods

    def check_for_new_best(self):
        """
        Checks the best_val of every Particle in the population.
        Stores the minimum best_val as global best.
        Gets then stores corresponding best_pos
        """
        self.best_val = min([p.best_val for p in self.population]) #Get best val of all particles best vals
        self.best_pos = self.get_best_pos(self.population) #Get corresponding best position

    def update(self):
        self.updateMethod(swarm=self, **self.kwargs)
        self.check_for_new_best()


#----------------------------- UPDATE METHODS ---------------------------------#
"""
Add or adjust any swarm update methods here.

Note:
All update methods should call Particle.update() for all particles in the swarm.
Particle.update() needs best_social_pos as a parameter - determined by each specific update method below.
This is the purpose of these methods.
We do not determine how to calculate the best value or position here, that is done in Swarm object.
See below for examples.
"""

def global_update(swarm):
    """
    Passes global best as the best_social_pos parameter in the Particle.update() method.
    """
    for p in swarm.population:
        p.update(swarm.best_pos)

def star_update(swarm, focal_index):
    """
    best_social_pos parameter determined by finding the best_pos between a given Particle and the Focal Particle.
    If the given Particle is the Focal Particle best_social_pos is the best pos of all Particles in neighborhood.

    Params:
    int focal_index: Index used to get Particle from neighborhood to use as focal point
    """
    for n in swarm.neighborhoods:
        focal_particle = n[focal_index]
        for p in n:
            if p != focal_particle:                                 #If not focal particle
                best_pos = swarm.get_best_pos([p, focal_particle])  #Get best pos between self and focal particle
            else:
                best_pos = swarm.get_best_pos(n)    #If focal particle, best pos is best_pos of neighborhood
            p.update(best_pos)

def ring_update(swarm):
    """
    Gets best position from adjacent Particles.
    Passes that value as the best_social_pos parameter in the Particle.update() method.
    """
    for neighborhood in swarm.neighborhoods:
        for i in range(len(neighborhood)):
            p = neighborhood[i] #Current Particle to update
            ring_neighbor_indices = [(i+j)%len(neighborhood) for j in [-1,0,1]] #Get adjacent indices in ring
            ring_neighbors = [neighborhood[j] for j in ring_neighbor_indices]   #Get corresponding particles
            best_pos = swarm.get_best_pos(ring_neighbors)                        #Get best position of those particles
            p.update(best_pos)

def von_neumann_update(swarm, n, m):
    """
    Create a nxm neighborhood that gets best_pos from both vertical and horizontal neighbors.
    nxm should be greater than or equal to neighborhood size (swarm size / n_neighbors).

    Params:
    int n: Number of rows
    int m: number of cols
    """
    z = 0 #counter
    for nbr in swarm.neighborhoods:
        #Small matrix warning
        if n*m < len(nbr):
            warnings.warn("Warning: nxm < size(neighborhood). Not all particles will be updated.")
        #Put neighborhood into nxm matrix
        size = len(nbr)
        vn = [[None for j in range(m)] for i in range(n)]
        #Fill vn with Particles in neighborhood
        i = 0
        while i < size:
            vn[i//m][i - (i//m)*m] = nbr[i]
            i += 1
        #Remove nulll values in vn
        for i in range(n):
            while None in vn[i]:
                vn[i].remove(None)
        while [] in vn:
            vn.remove([])
        #Connect adjacent Particles
        for i in range(m):
            rows = [row for row in vn if len(row) > i]#Get rows with at least i cols
            #Get neighbors
            for j in range(len(rows)):
                last_row = rows[j-1]
                curr_row = rows[j]
                next_row = rows[(j+1)%len(rows)]
                horiz_indices = [(i+h)%len(rows[j]) for h in [-1,0,1]]
                horiz_neighbors = [curr_row[k] for k in horiz_indices]
                vert_neighbors = [last_row[i], curr_row[i], next_row[i]]
                adj_neighbors = horiz_neighbors + vert_neighbors
                #Get best pos and update particle
                best_pos = swarm.get_best_pos(adj_neighbors)
                swarm.neighborhoods[z][j*m+i].update(best_pos)
        #increment neighborhood counter
        z += 1


#--------------------------- Animation ------------------------------#
"""
Adjust how the graph looks here.
"""

def animate(frame):
    ax.clear()  #Clear Plot
    i = 0       #Track which neighborhood we are in
    for nbrhd in swarm.neighborhoods:   #For Each neighborhood
        neighbor_count = len(nbrhd)     #Get num neighbors
        color = colors[i]               #Get color
        for n in range(neighbor_count):     #For each particle in neighborhood
            p = swarm.neighborhoods[i][n]   #Get particle
            ax.scatter(p.current_pos[0], p.current_pos[1], s=particle_size, color=color) #Plot particle
        i += 1  #Increment neighborhood tracker
    ax.set_xlim([-500,500])
    ax.set_ylim([-500,500])
    #Make title pretty
    ax.set_title(f"PSO Animation\n{updateMethod.__name__}  Frame {frame} / {iterations}")
    #update swarm each frame
    swarm.update()


#---------------------------- User Setup -----------------------------------#
"""
Change any desired settings for your animation here.
"""

#Particle Variables
lowerBound = -500  #bounds for Schwefel Function search space
upperBound = 500   #bounds for Schwefel Function search space
p1 = 1             #acceleration constant for cognitive component
p2 = 1             #acceleration constant for social component
inertiaWeight = 1  #Importance of current direction
velocityMax = 5    #Velocity Maximum

#Swarm Initialization Values
dimensions = 2              #number of dimensions of problem
swarmSize = 50              #number of particles in swarm
n_neighborhoods = 3         #number of neighborhoods in the Swarm, only effects local update methods

#Update Method Settings
updateMethod = von_neumann_update   #update method for swarm
kwargs = {'n':10, 'm':5}          #store any needed update method parameters here, excluding the swarm parameter.
#Ex) star_update_method takes "focal_index" as parameter, we want focal_index to equal 1.
#kwargs = {"focal_index":1}

#Animation Variables
iterations = 1000      #Number of times Swarm is updated
interval = 1      #Time between updates in Milliseconds
particle_size = 50  #Size of particles on plot
colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1]] #RGB Colors used for neighborhoods
for n in range(5,n_neighborhoods):
    colors.append([myPRNG.random(),myPRNG.random(),myPRNG.random()]) #Add more colors if over 5 neighborhoods

#Create Swarm and animate
swarm = Swarm(size=swarmSize, dimensions=dimensions, updateMethod=updateMethod, n_neighborhoods=n_neighborhoods, **kwargs)
fig, ax = plt.subplots()
ani = FuncAnimation(fig, animate, frames=iterations, interval=interval)
plt.show()
