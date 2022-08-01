import numpy as np
import matplotlib.pyplot as plt

from algorithms.particle_swarm_optimization import PSO
from algorithms.test_equations import rosenbrock

PSO_gbest_list = []

xBounds = [-1, 1]
yBounds = [-1, 1]

PSO_1 = PSO(xBounds, yBounds, maxIter=1000)

for i in range(10000):
    PSO_values = PSO_1.algorithm(rosenbrock.f, print_output=False)
    PSO_gbest_list.append(PSO_values)

PSO_mean = []
PSO_std = []

for i in range(PSO_1.maxIter):
    value_list = []

    for j in range(10000):
        value_list.append(PSO_gbest_list[j][i])

    PSO_mean.append(np.mean(value_list))
    PSO_std.append(np.std(value_list))

error_low = []
error_high = []

for i in range(PSO_1.maxIter):
    error_low.append(PSO_mean[i] - PSO_std[i])
    error_high.append(PSO_mean[i] + PSO_std[i])

plt.plot(range(PSO_1.maxIter), PSO_mean, 'g-')
plt.fill_between(range(PSO_1.maxIter), error_high, error_low, alpha=0.5, edgecolor='g', facecolor='#FF9848')
plt.show()
