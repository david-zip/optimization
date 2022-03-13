# General Notes and Questions about each Algorithm

## General Questions

- Whether it is better to have termination conditions or just maximum iteration counts?
  - Which is sufficient?
- If termination conditions are better, which ones may be recommended?

## Particle Swarm Optimization (PSO)

- Algorithm functions well and it is able to graphically show the solutions found by each particle at each iteration
- Current test shows the algorithm **struggles** to find optimal solution (unsure why)
- How can I graphically show the data?  
  - Is there another way that may be better to do this?

## Artificial Bee Colony (ABC)

- Not sure how the probability roulette wheel works so for now I will assume it works in the following manner:

> A random number is generated in the following range [0, 1]. Bees with solution probabilities above the randomly generated probability will be selected. From this new list, the solution that will be exploited will be chosen randomly

- Better to ask how this "*probability roulette wheel*" actually works
- How do I properly convert employed bees into scout bees?
- Able to effectively find optimal solutions in vicinity with only 100 iterations
- Work at implementing a termination condition instead of a iteration counter
- Possible termination criteria that states that objective function must be below 0.1 and that after 5 or more iterations of no changes, end while loop
  - Current termination condition works very wellfor Rosenbrock Equation (a=1 b=N)
  - **Test for larger values of a and/or b**
- Once termination condition works consistently, figure out how to graph data
  - Maybe graph best solution at each iteration? number of iterations?
