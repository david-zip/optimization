"""
Particle Swarm Optimization

Date: 13/03/22
"""
import time
import numpy as np

class PSO():
    """
    Particle swarm optimization for minimisation problems
    """

    def __init__(self, xBounds, yBounds, c1=0.2, c2=0.2, w=1, lbda=1 ,population=50, maxIter=1000):
        """
        Initialize algorithm hyper-parameter
        
        xBounds = x-axis boundaries
        
        yBounds = y-axis boundaries
        
        c1 = Personal best influence (default: 0.2)
        
        c2 = Global best influence (default: 0.2)
        
        w = Initial weight (default: 1)
        
        lbda = Weight decay exponent (default: 1)
            
        population = Number of particles in swarm (default: 50)
        
        maxIter = Maximum number of iterations (default: 1000)
        """
        # x boundaries
        self.xlb = min(xBounds)
        self.xub = max(xBounds)

        # y boundaries
        self.ylb = min(yBounds)
        self.yub = max(yBounds)

        # Update function parameters
        self.c1 = c1        # Personal best influence
        self.c2 = c2        # Global best influence
        self.w = w          # Velocity weight
        self.w0 = w         # Initial weight value
        self.lbda = lbda    # Weight decay exponent
        
        # Swarm population size
        self.population = population

        # Maximum iterations
        self.maxIter = maxIter

    def initialize(self, f):
        """
        Initialize random starting positions and velocities
        """
        self.particle_solution = []
        self.particle_value = []
        self.particle_velocity = []

        for i in range(self.population):
            # Initialize random solutions
            x = np.random.uniform(self.xlb, self.xub)
            y = np.random.uniform(self.ylb, self.yub)

            self.particle_solution.append(np.array([x,y]))

            # Calculate objective function of solution
            self.particle_value.append(float(f(self.particle_solution[i][0], self.particle_solution[i][1])))
            
            # Initialize random particle velocity
            vx = np.random.uniform(-1, 1)
            vy = np.random.uniform(-1, 1)

            self.particle_velocity.append(np.array([vx,vy]))

            # Initialize personal best
            self.pbest = []
            self.pbest_value = []
            
        for i in range(self.population):
            self.pbest.append(self.particle_solution[i])
            self.pbest_value.append(self.particle_value[i])

        # Initialize global best
        self.gbest_value = min(self.particle_value)
        self.gbest = self.particle_solution[self.particle_value.index(self.gbest_value)]

    def find_best(self):
        """
        Determine personal and global best
        """
        # Determine personal best
        for i in range(self.population):
            if self.particle_value[i] < self.pbest_value[i]:
                self.pbest[i] = self.particle_solution[i]
                self.pbest_value[i] = self.particle_value[i]

        # Determine global best
        min_value = min(self.particle_value)

        if min_value < self.gbest_value:
            self.gbest_value = min_value
            self.gbest = self.particle_solution[self.particle_value.index(self.gbest_value)]
        
        return self.gbest, self.gbest_value

    def update(self, f):
        """
        Particle velocity and position update functions
        """
        for i in range(self.population):

            # Update particle velocity and position
            for j in range(2):
                r1 = np.random.uniform(-1, 1)
                r2 = np.random.uniform(-1, 1)

                pbest_pt = self.c1 * r1 * (self.pbest[i][j] - self.particle_solution[i][j])
                gbest_pt = self.c2 * r2 * (self.gbest[j] - self.particle_solution[i][j])
                
                self.particle_velocity[i][j] = self.w * self.particle_velocity[i][j] + pbest_pt + gbest_pt
                self.particle_solution[i][j] = self.particle_solution[i][j] + self.particle_velocity[i][j]
        
            # Calculate particle fitness
            self.particle_value[i] = f(self.particle_solution[i][0], self.particle_solution[i][1])

    def weight_decay(self, nIter):
        """
        Exponential weight decay
        """
        self.w = self.w0 * np.exp(-self.lbda*nIter)

        return self.w

    def algorithm(self, f, print_output=True, wght_list=False):
        """
        Simulated annealling algorithm

        f = Objective function (input a python function)

        print_output = Prints final solution, objective function of solution, number of iterations, and time elapsed (default: True)
        
        wght_list = Returns list of weights (default: False)
        """
        gbest_value_list = []
        weight_list = []

        self.initialize(f)

        gbest_value_list.append(self.gbest_value)
        weight_list.append(self.w)

        nIter = 0
        time_start = time.time()
        while nIter < self.maxIter:
            self.weight_decay(nIter)
            self.update(f)
            self.find_best()

            # Store value in a list
            gbest_value_list.append(self.gbest_value)
            weight_list.append(self.w)

            # Iteration counter
            nIter += 1
        time_end = time.time()

        if print_output == True:
            print(
    f"""
    Particle Swarm Optimization Solution
    Best solution found = {self.gbest[0]}, {self.gbest[1]}
    Value of best = {self.gbest_value}
    No. iterations = {nIter}
    Time elasped = {time_end - time_start}s
    """
                )
        
        return gbest_value_list, (weight_list if wght_list==True else None)

if __name__=="__main__":
    
    def f(x,y):
        return x**2 + y**2 
    
    xBounds = [-3,3]
    yBounds = [-3,3]

    test = PSO(xBounds, yBounds, c1=0.3, c2=0.3, w=0.9, lbda=0.9 ,population=100, maxIter=10000)
    test.algorithm(f)
