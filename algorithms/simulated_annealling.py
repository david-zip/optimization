"""
Simulated Annealling Class

Date: 13/03/22
"""
import time
import numpy as np

class SA():
    """
    Artificial bee colony class
    """

    def __init__(self, xBounds, yBounds, Ti=1, Tf=0.1, maxIter=1000):
        """
        Initialize algorithm hyper-parameters
        
        xBounds = x-axis boundaries
        
        yBounds = y-axis boundaries

        Ti = Initial temperature (default: 1)

        Tf = Final temperature (default: 0.1)

        maxIter = Maximum number of iterations (default: 1000)
        """
        # x boundaries
        self.xlb = min(xBounds)
        self.xub = max(xBounds)

        # y boundaries
        self.ylb = min(yBounds)
        self.yub = max(yBounds)

        # Temperatures
        self.Ti = Ti
        self.Tf = Tf
        self.T = Ti
        self.eps = 1 - (Tf/Ti)**(maxIter**(-1))

        # Maximum iterations
        self.maxIter = maxIter

    def initialize(self, f):
        """
        Initialize random starting solutions
        """
        x = np.random.uniform(self.xlb, self.xub)
        y = np.random.uniform(self.ylb, self.yub)
        
        self.best_solution = np.array([x,y])
        self.best_value = f(self.best_solution[0], self.best_solution[1])

        return self.best_solution, self.best_value

    def neighbourhood_search(self, f):
        """
        Random neighbourhood search
        """
        x = np.random.uniform(self.xlb, self.xub)
        y = np.random.uniform(self.ylb, self.yub)

        self.new_solution = np.array([x,y])
        self.new_value = f(self.new_solution[0], self.new_solution[1])

    def find_best(self):
        """
        Replaces best solution and Metropolis acceptance probability
        """
        # Identify best solution
        if self.new_value < self.best_value:
            self.best_solution = self.new_solution
            self.best_value = self.new_value
        else:
            # Metropolis acceptance probability
            r = np.random.uniform()
            if r < np.exp((self.best_value - self.new_value)/self.T):
                self.best_solution = self.new_solution
                self.best_value = self.new_value
        
        return self.best_solution, self.best_value

    def cooling_schedule(self):
        """
        Geometric cooling schedule
        """
        self.T *= (1 - self.eps)

        return self.T

    def algorithm(self, f, show=True, temp_list=False):
        """
        Simulated annealling algorithm

        print=True - Prints final solution, objective function of solution, number of iterations, and time elapsed
        """
        best_solutions = []
        best_values = []
        temperature_list = []

        self.initialize(f)

        # Store values in a list
        best_solutions.append(self.best_solution)
        best_values.append(self.best_value)
        temperature_list.append(self.T)

        nIter = 0
        time_start = time.time()
        while self.T > self.Tf:
            self.neighbourhood_search(f)
            self.find_best()
            self.cooling_schedule()

            # Store values in a list    
            best_solutions.append(self.best_solution)
            best_values.append(self.best_value)
            temperature_list.append(self.T)

            # Iteration counter
            nIter += 1
        time_end = time.time()

        if show == True:
            print(
    f"""
    Simulated Annealling Solution
    Best solution found = {self.best_solution[0]}, {self.best_solution[1]}
    Value of best = {self.best_value}
    No. iterations = {nIter}
    Time elasped = {time_end - time_start}s
    """
                )

        return best_solutions, best_values, (temperature_list if temp_list==True else None)

if __name__=="__main__":
    
    def f(x,y):
        return x**2 + y**2 
    
    xBounds = [-1,1]
    yBounds = [-1,1]

    test = SA(xBounds, yBounds, Ti=100, Tf=0.01, maxIter=10000)
    test.algorithm(f)
