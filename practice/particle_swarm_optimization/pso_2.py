"""
Personal first attempt at PSO algorithm

Date: 20/02/22
"""

import random
import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    "Objective function"
    return (1 - x)**2 + 100*(y - x**2)**2

# Generate particles
n_particles = 50

X = np.random.rand(2, n_particles)
V = np.random.randn(2, n_particles)

# Hyper-parameter
c1 = 0.1; c2 = 0.1
w = 0.9

# Initialize particle best and global best
pbest = X
pbest_value = f(X[0], X[1])

gbest = pbest[:, pbest_value.argmin()]
gbest_value = pbest.min()

gbest_old = pbest[:, pbest_value.argmin()]
gbest_value_old = pbest.min()

niter = 0
iter_max = 10000
while niter < iter_max:
    for particle in range(n_particles):
        for i in range(1):
            r1 = np.random.rand()
            r2 = np.random.rand()
            
            V[i][particle] = w*V[i][particle] + c1*r1*(pbest[i][particle] - X[i][particle]) + c2*r2*(gbest[i] - X[i][particle])
            X[i][particle] += V[i][particle]

        fitness = f(X[0][particle], X[1][particle])
        
        if fitness < pbest_value[particle]:
            for i in range(1):
                pbest[i][particle] = X[i][particle]
            pbest_value[particle] = fitness

            if fitness < gbest_value:
                gbest_old = gbest
                gbest_value_old = gbest_value

                for i in range(1):
                    gbest[i] = X[i][particle]
            gbest_value = fitness
    
    # Termination criterion
    niter +=1

print("""
        gbest = {}, {}
        gbest value = {}
      """.format(gbest[0], gbest[1], gbest_value))
    