"""
Artificial bee colony

Date: 13/03/22
"""
from re import X
import time
from typing import Any
import numpy as np

class ABC():
    """
    Artificial bee colony for minimisation problems
    """

    def __init__(self, xBounds: list[float], yBounds: list[float], population: int = 50, maxIter: int = 1000):
        """
        Initialize optimization bounds
        
        xBounds = x-axis boundaries
        
        yBounds = y-axis boundaries

        population = Number of employed or onlooker bees in swarm (default: 50)
        
        maxIter = Maximum number of iterations (default: 1000)
        """
        # x boundaries
        self.xlb = min(xBounds)
        self.xub = max(xBounds)

        # y boundaries
        self.ylb = min(yBounds)
        self.yub = max(yBounds)

        # Swarm population size
        self.population = population

        # Maximum iterations
        self.maxIter = maxIter
    
    def initialize(self, f):
        """
        Initialize random starting positions
        """
        self.solutions = []
        self.sol_value = []

        # Initialize abandoned food list
        self.abandon = [0 for i in range(self.population)]

        for i in range(self.population):
            # Initialize random solution
            x = np.random.uniform(self.xlb, self.xub)
            y = np.random.uniform(self.ylb, self.yub)

            self.solutions.append(np.array([x,y]))

            # Calculate objective function of solution
            self.sol_value.append(float(f(x,y)))
        
        # Initialize best solution and value
        self.best_value = min(self.sol_value)
        self.best_solution = self.solutions[self.sol_value.index(self.best_value)]
        
        return self.abandon
    
    def replace_best(self, new_solution, new_sol_value, i):
        """
        Determines the best solution for each bee
        """
        # Determine best solution 
        if new_sol_value < self.sol_value[i]:
            self.solutions[i] = new_solution
            self.sol_value[i] = new_sol_value
        else:
            # If solution is worse, iter abandon food counter
            self.abandon[i] += 1

    def employed_bee(self, f, i):
        """
        Employed bee looks for new solutions and values
        """
        # Randomly finds solutions
        x = np.random.uniform(self.xlb, self.xub)
        y = np.random.uniform(self.ylb, self.yub)    
        
        # Update function
        rx = np.random.uniform(-1, 1)
        ry = np.random.uniform(-1, 1)
        new_x = self.solutions[i][0] + rx * (self.solutions[i][0] - x)
        new_y = self.solutions[i][1] + ry * (self.solutions[i][1] - y)

        # Store new solution and solution value
        new_solution = np.array([new_x, new_y])
        new_sol_value = float(f(new_x, new_y))

        return new_solution, new_sol_value

    def onlooker_bee(self, f, i):
        """
        Onlooker bee selects solutions via a roulette wheel selection system and 
        searches for better solutions in the neighbourhood
        """
        # Onlooker bees generate a new solution using random neighbourhood search
        # x bounds for neighbourhood search
        xlb = self.solutions[i][0] - self.solutions[i][0] * 0.1
        xub = self.solutions[i][0] + self.solutions[i][0] * 0.1
        
        # y bounds for neighbourhood serach
        ylb = self.solutions[i][1] - self.solutions[i][1] * 0.1
        yub = self.solutions[i][1] + self.solutions[i][1] * 0.1

        x = np.random.uniform(xlb, xub)
        y = np.random.uniform(ylb, yub)
            
        # Update function
        rx = np.random.uniform(-1, 1)
        ry = np.random.uniform(-1, 1)
        new_x = self.solutions[i][0] + rx * (self.solutions[i][0] - x)
        new_y = self.solutions[i][1] + ry * (self.solutions[i][1] - y)

        # Store new solution and solution value
        new_solution = np.array([new_x, new_y])
        new_sol_value = float(f(new_x, new_y))

        return new_solution, new_sol_value
        
    def scout_bee(self, f, i):
        """
        Scout bee finds new solutions if current solution is considered
        'abandoned'
        """
        # Scout bee will generate new solution in provided bounds
        rx = np.random.uniform(0, 1)
        ry = np.random.uniform(0, 1)
        x = self.xlb + rx * (self.xub - self.xlb)
        y = self.ylb + ry * (self.yub - self.ylb)

        # Replaces old solution with new solution found
        self.solutions[i] = np.array([x, y])
        self.sol_value[i] = float(f(x, y))

        # Restarts abandon counter
        self.abandon[i] = 0

    def find_best(self):
        """
        Finds best solution of the swarm and stores it

        Also returns best solution found by swarm so far
        """
        # Determines best solution of swarm
        min_sol = min(self.sol_value)

        if min_sol < self.best_value:
            self.best_value = min_sol
            self.best_solution = self.solutions[self.sol_value.index(min_sol)]
    
    def algorithm(self, f: Any, print_output: bool = True):
        """
        Artificial bee colony algorithm

        f = Objective function (input a python function)

        print_output = Prints final solution, objective function of solution, number of iterations, and time elapsed (default: True)
        """
        best_val_list = []

        self.initialize(f)

        nIter = 0
        time_start = time.time()
        while nIter < self.maxIter:
            for i in range(self.population):
                # Employed bee
                new_solution, new_sol_value = self.employed_bee(f, i)
                self.replace_best(new_solution, new_sol_value, i)

                # Generate and store solution probability
                sol_prob = float(self.sol_value[i] / sum(self.sol_value))

                # Picks a solution based on a roulette wheel selection system
                pr = np.random.uniform(0, 1/(self.population))
                if pr > sol_prob:
                    # Onlooker bee
                    new_solution, new_sol_value = self.onlooker_bee(f, i)
                    self.replace_best(new_solution, new_sol_value, i)

                # Scout bee
                if self.abandon[i] > 10:
                    self.scout_bee(f, i)

            # Determines best solution found
            self.find_best()

            # Stores best solution found in each iteration
            best_val_list.append(self.best_value)

            # Iteration counter
            nIter += 1
        time_end = time.time()

        if print_output == True:
            print(
    f"""
    Artificial Bee Colony Solution
    Best solution found = {self.best_solution[0]}, {self.best_solution[1]}
    Value of best = {self.best_value}
    No. iterations = {nIter}
    Time elasped = {time_end - time_start}s
    """
                )
        
        return best_val_list

if __name__=="__main__":
    
    def f(x,y):
        return x**2 + y**2 
    
    xBounds = [-3,3]
    yBounds = [-3,3]

    test = ABC(xBounds, yBounds, population=50, maxIter=1e4)
    test.algorithm(f)

