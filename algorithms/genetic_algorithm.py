"""
Genetic algorithm

Date: 13/03/22
"""
import time
import copy
import numpy as np

class GA():
    """
    Genetic algorithm for 2D minimisation problems (uses binary to represent genes)
    """

    def __init__(self, xBounds: list[float], yBounds: list[float], numbits: int = 16, population: int = 100, cut: float = 0.4, maxiter: int = 1000):
        """
        Initialize algorithm hyper-parameter
        
        xBounds = x-axis boundaries
        
        yBounds = y-axis boundaries
        
        numbits = Number of bits in gene (default: 16)
        
        population = Number of genes (default: 100)
        
        cut = percent of genes operated on (default: 0.4)
        
        maxiter = Maximum number of iterations (default: 1000)
        """
        # all bounds
        self.bounds = [xBounds, yBounds]
        
        # x boundaries
        self.xlb = min(xBounds)
        self.xub = max(xBounds)

        # y boundaries
        self.ylb = min(yBounds)
        self.yub = max(yBounds)

        # hyperparameters
        self.cut           = cut
        self.numbits       = numbits
        self.population    = population
        self.mutation_rate = 1.0 / (float(self.numbits * len(self.bounds)))

        # maximum iterations
        self.maxiter = maxiter

        # create required list
        self.gene_pool      = []
        self.gene_solutions = {}
        self.gene_fitness   = {}

        # initialize best solution variables
        self.best_gene         = 0
        self.best_solution     = 0
        self.best_gene_fitness = 1e100

    def _initialize(self, f):
        """
        Initialize aglorithm, generate random solutions and creates intial genes
        """
        # generate a list of random genes
        for i in range(self.population):
            gene = np.random.randint(0, 2, self.numbits * len(self.bounds)).tolist()
            gene = ''.join([str(s) for s in gene])
            self.gene_pool.append(gene)
        
        # initialize all gene solutions and fitness
        for gene in self.gene_pool:
            
            # determine solution of gene and store in list
            x, y = self._bitstring_to_decimal(gene)
            self.gene_solutions[gene] = [x, y]

            # calculate gene fitness and store in list
            fitness = f(x, y)
            self.gene_fitness[gene] = fitness
        
        # initialize best gene
        self._find_best()

    def _bitstring_to_decimal(self, gene):
        """
        Convert binary string into float values in decimal
        """
        decoded = []
        largest = 2**self.numbits

        for i in range(len(self.bounds)):
            # extracting substring
            start, end = i * self.numbits, (i * self.numbits) + self.numbits
            substring = gene[start:end]

            # convert bitstring to string of characters
            chars = ''.join([str(s) for s in substring])

            # convert string to integer
            integer = int(chars, 2)

            # scale integer to desired range
            value = self.bounds[i][0] + integer/largest * (self.bounds[i][1] - self.bounds[i][0])

            # store value
            decoded.append(value)

        return decoded[0], decoded[1]

    def _find_best(self):
        """
        Determines the best gene and stores it
        """
        best_gene_in_generation = min(self.gene_fitness, key=self.gene_fitness.get)

        if self.gene_fitness[best_gene_in_generation] < self.best_gene_fitness:
            self.best_gene         = best_gene_in_generation
            self.best_gene_fitness = self.gene_fitness[self.best_gene]
            self.best_solution     = self.gene_solutions[self.best_gene]

    def _selection(self):
        """
        Operator to select indiviuals for crossover; tournament selection
        """
        # select k individuals from the population
        cut = np.random.randint(1, len(self.gene_pool))
        np.random.shuffle(self.gene_pool)
        shuffled_gene_pool = self.gene_pool[:cut]

        champion = shuffled_gene_pool[0]

        # select the best gene from the k individuals
        for gene in shuffled_gene_pool:
            if self.gene_fitness[gene] < self.gene_fitness[champion]:
                champion = gene

        return champion

    def _crossover(self, parent1, parent2):
        """
        Operator to create new genes from parents; single point crossover
        """
        # choose crossover point
        point = np.random.randint(1, (len(parent1) - 2))

        # convert from bitstring to list
        parent1 = [int(s) for s in parent1]
        parent2 = [int(s) for s in parent2]

        # create children and perfrom crossover
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        # convert children back into bitstrin
        child1 = ''.join([str(s) for s in child1])
        child2 = ''.join([str(s) for s in child2])

        return child1, child2

    def _mutation(self, gene):
        """
        Operator which flips bits in a gene; bit flip mutation
        """        
        # convert bitstring into list
        gene_int = []
        for char in gene:
            gene_int.append(int(char))
        
        for i in range(len(gene_int)):

            # check if mutation should occur
            if np.random.rand() < self.mutation_rate:
                gene_int[i] = 1 - gene_int[i]
        
        return gene_int

    def algorithm(self, f: any, print_output: bool = True):
        """
        Artificial bee colony algorithm

        f = Objective function (input a python function)

        print_output = Prints final solution, objective function of solution, number of iterations, and time elapsed (default: True)
        """
        # initialize algorithm
        self._initialize(f)
        best_fitness_list = []

        # start algorithm
        # loop through generations
        niter = 0
        time_start = time.time()
        while niter < self.maxiter:
            for gene in self.gene_pool:

                # get value of gene
                x, y = self._bitstring_to_decimal(gene)
                self.gene_solutions[gene] = [x, y]

                # evaluate gene fitness
                self.gene_fitness[gene] = f(x, y)

            # determine the best gene
            self._find_best()

            # selection operator
            new_gene_pool = []
            for i in range(int(len(self.gene_pool) * self.cut)):

                # tournament selection
                selected = self._selection()
                new_gene_pool.append(selected)
                self.gene_pool.remove(selected)

            # crossover operator
            for i in range(0, len(new_gene_pool), 2):
                
                # select pairs of parents
                parent1, parent2 = new_gene_pool[i], new_gene_pool[i+1]
                
                # single point crossover
                child1, child2 = self._crossover(parent1, parent2)
                new_gene_pool.append(child1)
                new_gene_pool.append(child2)

            # mutation operator
            for i in range(len(new_gene_pool)):
                gene = self._mutation(new_gene_pool[i])
                new_gene_pool[i] = ''.join([str(s) for s in gene])
            
            # fill in or remove population if needed
            if len(new_gene_pool) < self.population:
                for i in range(len(new_gene_pool), self.population):
                    gene = np.random.randint(0, 2, self.numbits * len(self.bounds)).tolist()
                    gene = ''.join([str(s) for s in gene])
                    new_gene_pool.append(gene)

            elif len(new_gene_pool) > self.population:
                for i in range(self.population, len(new_gene_pool)):
                    np.random.shuffle(new_gene_pool)
                    removed = new_gene_pool.pop(-1)
            
            # define new population; clear dictionary list
            self.gene_pool = new_gene_pool
            self.gene_solutions.clear()
            self.gene_fitness.clear()

            # Stores best solution found in each iteration
            best_fitness_list.append(self.best_gene_fitness)

            # iteration counter
            niter += 1
        time_end = time.time()

        if print_output == True:
            print(
    f"""
    Genetic Algorithm
    Best gene = {self.best_gene}
    Best solution found = {self.best_solution}
    Fitness of best = {self.best_gene_fitness}
    No. iterations = {niter}
    Time elasped = {time_end - time_start}s
    """
                )
            
        return best_fitness_list

if __name__=="__main__":
    
    def f(x,y):
        return x**2 + y**2 
    
    xBounds = [-3,3]
    yBounds = [-3,3]

    test1 = GA(xBounds, yBounds, numbits=32, population=1000, cut=0.3, maxiter= 100)
    test1.algorithm(f)

    def f(x,y):
        return (x + 2*y - 7)**2 + (2*x + y - 5)**2

    xBounds = [-10,10]
    yBounds = [-10,10]

    test2 = GA(xBounds, yBounds)
    test2.algorithm(f)


        