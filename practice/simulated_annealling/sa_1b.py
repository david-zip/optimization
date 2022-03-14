"""
Initial attempt on implementing Simulated Annealling 

Date: 13/03/22
"""
import time
import numpy as np

# Define function
def f(x, y):
    "Defines objective function"
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2

# Define boundaries
# Position boundaries
lb = -5
ub = 5

# Initialize algorithm parameters
Ti = 1        # Inital temperature
Tf = 0.1      # Final temperature

# Initialize algorithm's position
best_solution = np.random.uniform(lb, ub, [2,1])
best_value = f(best_solution[0], best_solution[1])

T = Ti
niter = 0
max_iter = 1000

# Epsiltion value
eps = 1 - (Tf/Ti)**(max_iter**-1)

time_start = time.time()
while T > Tf:
    
    # Neighbourhood search
    new_solution = np.random.uniform(lb, ub, [2,1])
    new_value = f(new_solution[0], new_solution[1])

    # Identify best solution
    if new_value < best_value:
        best_solution = new_solution
        best_value = new_value
    else:
        # Metropolis acceptance probability
        r = np.random.uniform()
        if r < np.exp((best_value - new_value)/T):
            best_solution = new_solution
            best_value = new_value
    
    # Cooling schedule (Logarithmic)
    num = Ti * Tf * (np.log10(max_iter + 1) - np.log10(2))
    den = Tf * np.log10(max_iter + 1) - Ti * np.log10(2) + (Ti - Tf) * np.log10(niter + 1)
    
    T = num/den

    niter += 1
time_end = time.time()

print(
    f"""
    Simulated Annealling Solution
    Best solution found = {best_solution[0]}, {best_solution[1]}
    Value of best = {float(best_value)}
    No. iterations = {niter}
    Time elasped = {time_end - time_start}s
    """
)
