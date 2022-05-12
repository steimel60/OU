import math
from random import Random, choice
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

#Particle Variables
lowerBound = -500  #bounds for Schwefel Function search space
upperBound = 500   #bounds for Schwefel Function search space
p1 = 1             #acceleration constant for cognitive component
p2 = 1             #acceleration constant for social component
inertiaWeight = 1  #Importance of current direction
velocityMax = 5    #Velocity Maximum

#Swarm Initialization Values
dimensions = 2 #number of dimensions of problem
swarmSize = 50 #number of particles in swarm
n_neighborhoods = 1 #Number of neighborhoods in the Swarm

#Animation Variables
iterations = 1000      #Number of times Swarm is updated
interval = 1      #Time between updates in Milliseconds
particle_size = 50  #Size of particles on plot
colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1]] #RGB Colors used for neighborhoods

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
    def __init__(self, size=10, dimensions=2, useGlobalUpdateMethod=True, n_neighborhoods=2):
        """
        int size = Number of Particles in the Swarm
        int dimensions = Dimension of each particle
        bool useGlobalUpdateMethod = True uses global best update method, False uses local best
        int n_neighborhoods = Number of neighborhoods to create when using local best. Must be less than size.
        """
        self.population = [Particle(dimensions) for n in range(size)] #Create list of particles
        self.best_val = self.get_best_val(self.population)            #Get first best val
        self.best_pos = self.get_best_pos(self.population)            #Get first best pos
        self.update = self.get_update_method(useGlobalUpdateMethod)   #Get local or global update method
        self.neighborhoods = self.build_neighborhoods(n_neighborhoods)#Get n neighborhoods

    def get_update_method(self, useGlobalUpdateMethod):
        """
        Used to dictate which update method should be used - Global or Local.
        """
        if useGlobalUpdateMethod:
            return self.global_update_method
        else:
            return self.local_update_method

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

    def global_update_method(self):
        """
        Updates all particles of the Swarm.
        Passes global best as the best_social_pos parameter in the Particle.update() method.
        """
        for p in self.population:   #For each particle in swarm
            p.update(self.best_pos) #Update particle with global best
        self.check_for_new_best()   #Update and track global best

    def local_update_method(self):
        """
        Updates all the particles of the Swarm.
        Iterates through particles of each neighborhood.
        Gets the minimum best_val attribute of adjacent Particles - Ring Topology.
        Passes that value as the best_social_pos parameter in the Particle.update() method.
        """
        for neighborhood in self.neighborhoods:
            for i in range(len(neighborhood)):
                p = neighborhood[i] #Current Particle to update
                ring_neighbor_indices = [(i+j)%len(neighborhood) for j in [-1,0,1]] #Get adjacent indices in ring
                ring_neighbors = [neighborhood[j] for j in ring_neighbor_indices]   #Get corresponding particles
                best_pos = self.get_best_pos(ring_neighbors)                        #Get best position of those particles
                p.update(best_pos)  #Update current particle with that value
        self.check_for_new_best()   #Update and track global best

    def check_for_new_best(self):
        """
        Checks the best_val of every Particle in the population.
        Stores the minimum best_val as global best.
        Gets then stores corresponding best_pos
        """
        self.best_val = min([p.best_val for p in self.population]) #Get best val of all particles best vals
        self.best_pos = self.get_best_pos(self.population) #Get corresponding best position

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
    ax.set_title(f"Frame {frame} / {iterations}")
    swarm.update()


swarm = Swarm(size=swarmSize, dimensions=dimensions, useGlobalUpdateMethod=True, n_neighborhoods=n_neighborhoods)
fig, ax = plt.subplots()
ani = FuncAnimation(fig, animate, frames=iterations, interval=interval)
plt.show()
