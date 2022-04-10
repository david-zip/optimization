"""
Genetic algorithm first attempt for OneMax Equation

https://www.youtube.com/watch?v=CZE86BPDqCI&ab_channel=SteveBrunton
https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/

Second link provided the code for this example
Date: 07/04/22
"""
import numpy as np

### OBJECTIVE FUNCTION ###
def f(x):
    # onemax sum
    return -sum(x)

### TOURNAMENT SELECTION ###
def selection(pop, scores, k=3):
    # first random selection
    selection_ix = np.random.randint(len(pop))
    for ix in np.random.randint(0, len(pop), k-1):
        # check if there is better
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

### CROSSOVER OPERATOR ###
def crossover(p1, p2, r_cross):
    # crossover two parents to make two copies
    # by default, both childern are just copies of the parents
    c1, c2 = p1.copy(), p2.copy()

    # check for recombination
    if np.random.rand() < r_cross:
        # select crossover point that is not at the end of the string
        pt = np.random.randint(1, len(p1)-2)

        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p1[:pt] + p2[pt:]

    return [c1, c2]

### MUTATION OPERATOR ###
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check if there will be a mutation
        if np.random.rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

### GENETIC ALGORITHM ###
def genetic_algorithm(f, n_bits, n_iter, n_pop, r_cross, r_mut):
    # inital population of random bitstrings
    pop = [np.random.randint(0, 2, n_bits).tolist() for _ in range(n_pop)]

    # keep track of best solution
    best, best_eval = 0, f(pop[0])

    # enumerate generations
    for gen in range(n_iter):

        # evaluate all candidates in the population
        scores = [f(c) for c in pop]

        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))

        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]

        # create next generation
        children = []
        for i in range(0, n_pop, 2):

            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]

            # crossover and mutation
            for c in crossover(p1, p2, r_cross):

                # mutation
                mutation(c, r_mut)

                # store next generation
                children.append(c)

        # replace poplation
        pop = children
    
    return [best, best_eval]

if __name__=="__main__":
    ### HYPERPARAMETERS ###
    # define the total iterations
    n_iter = 1000
    # bits
    n_bits = 20
    # define the population size
    n_pop = 100
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 1.0 / float(n_bits)
    
    # perform the genetic algorithm search
    best, score = genetic_algorithm(f, n_bits, n_iter, n_pop, r_cross, r_mut)
    print('Done!')
    print('f(%s) = %f' % (best, score))
