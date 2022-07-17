"""
Genetic algorithm for Rosenbrock equation

https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/

Date: 10/04/22
"""
import numpy as np

### DECODER ###
# translate butstring to numbers
def decode(bounds, n_bits, bitstring):

    decoded = []
    largest = 2**n_bits
    for i in range(len(bounds)):
        
        # extract substring
        start, end = i * n_bits, (i * n_bits) + n_bits
        substring = bitstring[start:end]

        # convert bitstring to a string of chars
        chars = ''.join([str(s) for s in substring])

        # convert string to integer
        integer = int(chars, 2)

        # scale integer ro desired range
        value = bounds[i][0] + integer/largest * (bounds[i][1] - bounds[i][0])

        # store 
        decoded.append(value)
    
    return decoded[0], decoded[1]

### SELECTION OPERATOR ###
# tournament selection
def selection(pop, scores, k=3):
    
	# first random selection
	selection_ix = np.random.randint(len(pop))
	for ix in np.random.randint(0, len(pop), k-1):

		# check if better (e.g. perform a tournament)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix

	return pop[selection_ix]

### CROSSOVER OPERATOR ###
def crossover(p1, p2, r_cross):

	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if np.random.rand() < r_cross:

		# select crossover point that is not on the end of the string
		pt = np.random.randint(1, len(p1)-2)

		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]

	return [c1, c2]

### MUTATION OPERATOR ###
def mutation(bitstring, r_mut):
	for i in range(len(bitstring)):

		# check for a mutation
		if np.random.rand() < r_mut:

			# flip the bit
			bitstring[i] = 1 - bitstring[i]

def genetic_algorithm(f, bounds, n_bits, n_iter, n_pop, r_cross, r_mut):
    
    # initial population of random bitstring
    pop = [np.random.randint(0, 2, n_bits * len(bounds)).tolist() for _ in range(n_pop)]

    # keep track of best solution
    x, y = decode(bounds, n_bits, pop[0])
    best, best_eval = 0, f(x, y)

    # enumerate population
    for gen in range(n_iter):

        # decode population
        decoded = [decode(bounds, n_bits, p) for p in pop]

        # evaluate all candidates in the population
        scores = [f(c[0], c[1]) for c in decoded]

        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %f" % (gen,  decoded[i], scores[i]))
        
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

                # store for next generation
                children.append(c)
        
        # store
        pop = children
    
    return best, best_eval

if __name__=="__main__":
    
    ### OBJECTIVE FUNCTION ###
    def f(x, y):
        "Rosenbrock test function"
        a = 1
        b = 100
        return (a - x)**2 + b*(y - x**2)**2

    ### HYPERPARAMETERS
    # define range for input
    bounds = [[-5.0, 5.0], [-5.0, 5.0]]

    # define the total iterations
    n_iter = 100

    # bits per variable
    n_bits = 16

    # define the population size
    n_pop = 100

    # crossover rate
    r_cross = 0.9

    # mutation rate
    r_mut = 1.0 / (float(n_bits) * len(bounds))

    # perform the genetic algorithm search
    best, score = genetic_algorithm(f, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)
    print('Done!')
    decoded = decode(bounds, n_bits, best)
    print('f(%s) = %f' % (decoded, score))
    