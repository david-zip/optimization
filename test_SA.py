import numpy as np
import matplotlib.pyplot as plt
from algorithms.particle_swarm_optimization import PSO

from algorithms.simulated_annealling import SA
from algorithms.test_equations import rosenbrock

SA_best = []

xBounds = [-1, 1]
yBounds = [-1, 1]

SA_1 = SA(xBounds, yBounds, maxIter=1000)

for i in range(10000):
    SA_values = SA_1.algorithm(rosenbrock.f, print_output=False)
    SA_best.append(SA_values)

SA_mean = []
SA_std = []

for i in range(SA_1.maxIter):
    value_list = []

    for j in range(10000):
        value_list.append(SA_best[j][i])

    SA_mean.append(np.mean(value_list))
    SA_std.append(np.std(value_list))

error_low = []
error_high = []

for i in range(SA_1.maxIter):
    error_low.append(SA_mean[i] - SA_std[i])
    error_high.append(SA_mean[i] + SA_std[i])

plt.plot(range(SA_1.maxIter), SA_mean, 'o-')
plt.fill_between(range(SA_1.maxIter), error_high, error_low, alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
plt.show()
