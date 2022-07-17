"""
Third attempt at designing genetic algorithm for optimization

Main purpose is to understand the conversion from bitstring to decimal

Date: 04/07/22
"""
import numpy as np

# Decoding bitstring to decimal
def bitstring_to_decimal(BOUNDS, NUM_BITS, bitstring):
    
    decoded = []
    largest = 2**NUM_BITS

    for i in range(len(BOUNDS)):

        # extracting substring
        start, end = i * NUM_BITS, (i * NUM_BITS) + NUM_BITS
        substring = bitstring[start:end]

        # convert bitstring to string of characters
        chars = ''.join([str(s) for s in substring])

        # convert string to integer
        integer = int(chars, 2)

        # scale integer to desired range
        value = BOUNDS[i][0] + integer/largest * (BOUNDS[i][1] - BOUNDS[i][0])

        # store value
        decoded.append(value)

    return decoded[0], decoded[1]

# Selection operator
# tournament selection
def selection(population, scores):

    # select k individuals from the population
    cut = np.random.randint(1, len(population))
    np.random.shuffle(population)
    pop_shuffled = population[:cut]

    selected_gene = pop_shuffled[0]

    # select the best individual from the k individuals
    for gene in pop_shuffled:
        
        # check for which gene is the best
        if scores[gene] < scores[selected_gene]:
            selected_gene = gene

    return selected_gene

# Crossover operator
def crossover(parent1, parent2):

    # choose crossover point
    point = np.random.randint(1, (len(parent1) - 2))

    # convert from bitstring to list
    parent1 = [int(s) for s in parent1]
    parent2 = [int(s) for s in parent2]

    # create children and perform crossover
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2
    
# Mutation operator
def mutation(gene, r_mutation):
    
    # convert bitstring into list
    gene_int = []
    for char in gene:
        gene_int.append(int(char))
    
    for i in range(len(gene_int)):

        # check if mutation should occur
        if np.random.rand() < r_mutation:
            gene_int[i] = 1 - gene_int[i]
    
    return gene_int

# genetic algorithm
def genetic_algorithm(function, BOUNDS, NUM_BITS, NUM_POPULATION, MAX_ITER, CUT, R_MUTATION):
    # Initialise algorithm
    # initial population of random bitstring
    population = []
    for i in range(NUM_POPULATION):
        gene = np.random.randint(0, 2, NUM_BITS * len(BOUNDS)).tolist()
        gene = ''.join([str(s) for s in gene])
        population.append(gene)

    # record best solution 
    x, y = bitstring_to_decimal(BOUNDS, NUM_BITS, population[0])
    best, best_eval = population[0], f(x, y)

    # iterate through multiple searchs to find optimal solution
    for generation in range(MAX_ITER):
        solutions = {}
        scores = {}
        for gene in population:
            
            # get values of bitstring
            x, y = bitstring_to_decimal(BOUNDS, NUM_BITS, gene)
            solutions[gene] = [x, y]
            
            # evaluate bitstring performance
            scores[gene] = function(x, y)

        # identify best solution in each iteration 
        best_gene_in_pop = min(scores, key=scores.get)
        if scores[best_gene_in_pop] < best_eval:
            best, best_eval = best_gene_in_pop, scores[best_gene_in_pop]
            print(f'best gene: {best}, new best f({solutions[best][0]:.2f}, {solutions[best][1]:.2f}) = {best_eval}')
        
        new_population = []
        # selection operator
        for i in range(int(len(population) * CUT)):
            selected = selection(population, scores)
            selected = ''.join([str(s) for s in selected])
            new_population.append(selected)
            removed = population.remove(selected)
        
        # crossover operator
        for i in range(0, len(new_population), 2):
            # select pairs of parents (adjacent parents)
            parent1, parent2 = new_population[i], new_population[i+1]

            # perform crossover
            child1, child2 = crossover(parent1, parent2)
            child1 = ''.join([str(s) for s in child1])
            child2 = ''.join([str(s) for s in child2])
            
            new_population.append(child1)
            new_population.append(child2)
        
        # fill in or remove population if needed
        if len(new_population) < NUM_POPULATION:
            for i in range(len(new_population), NUM_POPULATION):
                gene = np.random.randint(0, 2, NUM_BITS * len(BOUNDS)).tolist()
                gene = ''.join([str(s) for s in gene])
                new_population.append(gene)

        elif len(new_population) > NUM_POPULATION:
            for i in range(NUM_POPULATION, len(new_population)):
                np.random.shuffle(new_population)
                removed = new_population.pop(-1)

        # mutation operator
        for i in range(len(new_population)):
            gene = mutation(new_population[i], R_MUTATION)
            new_population[i] = ''.join([str(s) for s in gene])

        # define new population
        population = new_population

        if generation % 100 == 0:
            print(f"Generation {generation} complete")
    print("Training complete")

    return best, best_eval
        
if __name__=="__main__":
    
    ### OBJECTIVE FUNCTION ###
    def f(x, y):
        "'Other' test function"
        return (2*x)**2 + y**2 + (x - 3)*y

    ### HYPERPARAMETERS
    # define range for input
    BOUNDS = [[-5.0, 5.0], [-5.0, 5.0]]

    # define the total iterations
    MAX_ITER = 10000

    # bits per variable
    NUM_BITS = 16

    # define the population size
    NUM_POPULATION = 100

    # mutation rate
    R_MUTATION = 1.0 / (float(NUM_BITS) * len(BOUNDS))

    # cut rate
    CUT = 0.4

    # perform the genetic algorithm search
    best, score = genetic_algorithm(f, BOUNDS, NUM_BITS, NUM_POPULATION, MAX_ITER, CUT, R_MUTATION)
    solutions = bitstring_to_decimal(BOUNDS, NUM_BITS, best)
    print('f(%s) = %f' % (solutions, score))

        

