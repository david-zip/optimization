"""
Run optimization algorithms on test functions

Date 13/03/22
"""
import matplotlib.pyplot as plt

from algorithms.simulated_annealling import SA
from algorithms.particle_swarm_optimization import PSO

from test_equations import rosenbrock


xBounds = [-5,5]
yBounds = [-5,5]

# Simulated annealling
sim_ann = SA(xBounds, yBounds, maxIter=1e6)
SA_values, temperatures = sim_ann.algorithm(rosenbrock.f, temp_list=True)

# Particle swarm optimization
par_swa_op = PSO(xBounds, yBounds, maxIter=1e4)
PSO_values, weights = par_swa_op.algorithm(rosenbrock.f, wght_list=True)
