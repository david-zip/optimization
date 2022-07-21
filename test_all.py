import time
import numpy as np
import matplotlib.pyplot as plt

from algorithms.artificial_bee_colony import ABC
from algorithms.simulated_annealling import SA
from algorithms.particle_swarm_optimization import PSO
from algorithms.genetic_algorithm import GA

from algorithms.test_equations.other import f

# Bounds
xBounds = [-5, 5]
yBounds = [-5, 5] 

iterNumber = 50
maxIteration = 100

print(f"\nAlgorithms started for {maxIteration} iterations")

# Simulated Annealing
print(f"\nSA algorithm started - {iterNumber} times")
SA_time_s = time.time()

SA_best = []

SA_1 = SA(xBounds, yBounds, maxIter=maxIteration)

for i in range(iterNumber):
    SA_values = SA_1.algorithm(f, print_output=False)
    SA_best.append(SA_values)

SA_mean = []
SA_std = []

for i in range(SA_1.maxIter):
    SA_value_list = []

    for j in range(iterNumber):
        SA_value_list.append(SA_best[j][i])

    SA_mean.append(np.mean(SA_value_list))
    SA_std.append(np.std(SA_value_list))

SA_error_low = []
SA_error_high = []

for i in range(SA_1.maxIter):
    SA_error_low.append(SA_mean[i] - SA_std[i])
    SA_error_high.append(SA_mean[i] + SA_std[i])

SA_time_e = time.time()

print(f"""
    SA finished
        Time: {(SA_time_e - SA_time_s)/60} min
""")

# Particle Swarm Optimization
print(f"\nPSO algorithm started - {iterNumber} times")
PSO_time_s = time.time()

PSO_gbest_list = []

PSO_1 = PSO(xBounds, yBounds, maxIter=maxIteration)

for i in range(iterNumber):
    PSO_values = PSO_1.algorithm(f, print_output=False)
    PSO_gbest_list.append(PSO_values)

PSO_mean = []
PSO_std = []

for i in range(PSO_1.maxIter):
    PSO_value_list = []

    for j in range(iterNumber):
        PSO_value_list.append(PSO_gbest_list[j][i])

    PSO_mean.append(np.mean(PSO_value_list))
    PSO_std.append(np.std(PSO_value_list))

PSO_error_low = []
PSO_error_high = []

for i in range(PSO_1.maxIter):
    PSO_error_low.append(PSO_mean[i] - PSO_std[i])
    PSO_error_high.append(PSO_mean[i] + PSO_std[i])

PSO_time_e = time.time()

print(f"""
    PSO finished
        Time: {(PSO_time_e - PSO_time_s)/60} min
""")

# Artificial Bee Colony
print(f"\nABC algorithm started - {iterNumber} times")
ABC_time_s = time.time()

ABC_best = []

ABC_1 = ABC(xBounds, yBounds, maxIter=maxIteration)

for i in range(iterNumber):
    ABC_values = ABC_1.algorithm(f, print_output=False)
    ABC_best.append(ABC_values)

ABC_mean = []
ABC_std = []

for i in range(ABC_1.maxIter):
    ABC_value_list = []

    for j in range(iterNumber):
        ABC_value_list.append(ABC_best[j][i])

    ABC_mean.append(np.mean(ABC_value_list))
    ABC_std.append(np.std(ABC_value_list))

ABC_error_low = []
ABC_error_high = []

for i in range(ABC_1.maxIter):
    ABC_error_low.append(ABC_mean[i] - ABC_std[i])
    ABC_error_high.append(ABC_mean[i] + ABC_std[i])

ABC_time_e = time.time()

print(f"""
    ABC finished
        Time: {(ABC_time_e - ABC_time_s)/60} min
""")

# Genetic Algorithm
print(f"\nGA algorithm started - {iterNumber} times")
GA_time_s = time.time()

GA_best = []

GA_1 = GA(xBounds, yBounds, maxiter=maxIteration)

for i in range(iterNumber):
    GA_values =GA_1.algorithm(f, print_output=False)
    GA_best.append(GA_values)

GA_mean = []
GA_std = []

for i in range(GA_1.maxiter):
    GA_value_list = []

    for j in range(iterNumber):
        GA_value_list.append(GA_best[j][i])

    GA_mean.append(np.mean(GA_value_list))
    GA_std.append(np.std(GA_value_list))

GA_error_low = []
GA_error_high = []

for i in range(GA_1.maxiter):
    GA_error_low.append(GA_mean[i] - GA_std[i])
    GA_error_high.append(GA_mean[i] + GA_std[i])

GA_time_e = time.time()

print(f"""
    GA finished
        Time: {(GA_time_e - GA_time_s)/60} min
""")

# Plot graphs
fig = plt.figure()
plt.suptitle(f"Optimization Algorithms for Other - {iterNumber} Iterations")

plt.plot(range(SA_1.maxIter), SA_mean, 'r-', label='Simulated Annealing')
plt.fill_between(range(SA_1.maxIter), SA_error_high, SA_error_low, alpha=0.3, edgecolor='r', facecolor='r')

plt.plot(range(PSO_1.maxIter), PSO_mean, 'g-', label='Particle Swarm Optimization')
plt.fill_between(range(PSO_1.maxIter), PSO_error_high, PSO_error_low, alpha=0.3, edgecolor='g', facecolor='g')

plt.plot(range(ABC_1.maxIter), ABC_mean, 'y-', label='Artificial Bee Colony')
plt.fill_between(range(ABC_1.maxIter), ABC_error_high, ABC_error_low, alpha=0.3, edgecolor='y', facecolor='y')

plt.plot(range(GA_1.maxiter), GA_mean, 'b-', label='Genetic Algorithm')
plt.fill_between(range(GA_1.maxiter), GA_error_high, GA_error_low, alpha=0.3, edgecolor='b', facecolor='b')

plt.xlabel("Number of Iterations")
plt.ylabel("Objective Function")
plt.legend(loc="upper right")

plt.savefig(f'plots/comparisons/Other Equation - {iterNumber} Iterations.png')

plt.show()

print("\nTotal process completed")
print(f"\tTime elapsed: {(ABC_time_e - SA_time_s)/60} min")
