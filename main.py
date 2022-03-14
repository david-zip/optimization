"""
Run optimization algorithms on test functions

Date 13/03/22
"""
import matplotlib.pyplot as plt

from algorithms.simulated_annealling import SA
from test_equations import rosenbrock

# Simulated annealling
xBounds = [-5,5]
yBounds = [-5,5]

sim_ann = SA(xBounds, yBounds, maxIter=1e6)
best_solutions, best_values, temperatures = sim_ann.algorithm(rosenbrock.f, temp_list=True)

plt.scatter(range(len(temperatures)), temperatures, s=5)

# x-axis label
plt.xlabel('Iterations')
# frequency label
plt.ylabel('Temperature')
# plot title
plt.title('Cooling Schduele')

plt.show()
