"""
Differential evolution first attempt for Rosenbrock equation

https://machinelearningmastery.com/differential-evolution-from-scratch-in-python/

Date: 31/07/22
"""
import numpy as np

# Define fitness function
def f(x):
    global a, b
    a = 1
    b = 100
    return (a - x[0])**2 + b*(x[1] - x[0]**2)**2

def check_bounds(mutated, bounds):
    mutated_bound = [np.clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound

# mutation operator
def mutation(x, F):
    return x[0] + F * (x[1] - x[2])

# crossover operator
def crossover(mutated, target, dims, cr):
    # generate a uniform random solution
    p = np.random.rand(dims)

    # generate trial vector by binomial crossover
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]

    return trial

# algorithm
def differential_evolution(pop_size, bounds, iter, F, cr):
    # initialise population
    pop = bounds[:,0] + (np.random.rand(pop_size, len(bounds)) * (bounds[:,1] - bounds[:,0]))

    # evaluate initial population
    obj_all = [f(sol) for sol in pop]

    # find the best performing vector of initial population
    best_solutions = pop[np.argmin(obj_all)]
    best_obj = min(obj_all)
    prev_obj = best_obj

    # run algorithm
    for i in range(itermax):
        # iterate over population
        for j in range(pop_size):

            # choose three candidates that is not the current
            candidates = [candidate for candidate in range(pop_size) if candidate != j]
            a, b, c = pop[np.random.choice(candidates, 3, replace=False)]

            # mutation operator
            mutated = mutation([a, b, c], F)

            # crossover operator
            trial = crossover(mutated, pop[j], len(bounds), cr)

            # compute objective functino for target value
            obj_target = f(pop[j])

            # compute objective function for trial vector
            obj_trial = f(trial)

            # perform selection
            if obj_trial < obj_target:
                # replace solution and fitness of solution
                pop[j] = trial
                obj_all[j] = obj_trial
            
            # find the best performing vector at each iteration
            best_obj = min(obj_all)

            # store best objective functon
            if best_obj < prev_obj:
                best_solutions = pop[np.argmin(obj_all)]
                prev_obj = best_obj
            
                print('Iteration: %d f([%s]) = %.5f' % (i, np.around(best_solutions, decimals=5), best_obj))
    
    return [best_solutions, best_obj]

if __name__=="__main__":
        
    # define hyperparameters
    population_size = 100   # population size
    itermax = 1000          # max number of iterations
    F = 0.5                 # scale factor
    mut_cr = 0.7            # crossover rate

    # define solution bounds
    bounds = np.asarray([(-5, 5), (-5, 5)])

    # perform differential evolution
    solution = differential_evolution(population_size, bounds, iter, F, mut_cr)
    print('\nSolution: f([%s]) = %.5f' % (np.around(solution[0], decimals=5), solution[1]))