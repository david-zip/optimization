"""
Run optimization algorithms on test functions

Date 13/03/22
"""
from algorithms.simulated_annealling import SA
from test_equations import rosenbrock

# Simulated annealling
xBounds = [-5,5]
yBounds = [-5,5]

sim_ann = SA(xBounds, yBounds)
sim_ann.algorithm(rosenbrock.f)