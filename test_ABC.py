import numpy as np
import matplotlib.pyplot as plt

from algorithms.artificial_bee_colony import ABC
from algorithms.test_equations import rosenbrock

ABC_best = []

xBounds = [-5, 5]
yBounds = [-5, 5]

ABC_1 = ABC(xBounds, yBounds, maxIter=1000)

for i in range(1000):
    ABC_values = ABC_1.algorithm(rosenbrock.f, print_output=False)
    ABC_best.append(ABC_values)

ABC_mean = []
ABC_std = []

for i in range(ABC_1.maxIter):
    value_list = []

    for j in range(1000):
        value_list.append(ABC_best[j][i])

    ABC_mean.append(np.mean(value_list))
    ABC_std.append(np.std(value_list))

error_low = []
error_high = []

for i in range(ABC_1.maxIter):
    error_low.append(ABC_mean[i] - ABC_std[i])
    error_high.append(ABC_mean[i] + ABC_std[i])

plt.plot(range(ABC_1.maxIter), ABC_mean, 'o-')
plt.fill_between(range(ABC_1.maxIter), error_high, error_low, alpha=0.5, edgecolor='o', facecolor='#FF9848')
plt.show()
