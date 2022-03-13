"""
Third attempt at implementing PSO for a minimisation problem

Global communication

Date: 07/03/22
"""
import time
import random
import numpy as np

def f(x, y):
    "Defines objective function"
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2

# Define boundaries
# Position boundaries
lb = -5
ub = 5

# Define hyper-parameters
c1 = 0.2    # Personal best constant
c2 = 0.2    # Global best constant
w0 = 1      # Initial weight 
w = 1
lbda = 1    # exponential decay constant

# Initialize PSO population
particle_number = 50
particle_solution = []
particle_value = []
particle_velocity = []

for i in range(particle_number):
    particle_solution.append(np.random.uniform(lb, ub, [2,1]))
    particle_value.append(float(f(particle_solution[i][0], particle_solution[i][1])))
    particle_velocity.append(np.random.uniform(-1, 1, [2,1]))

# Determine personal best
pbest = []
pbest_value = []
for i in range(len(particle_solution)):
    pbest.append(particle_solution[i])
    pbest_value.append(particle_value[i])

# Determine global best
gbest_value = min(particle_value)
gbest = particle_solution[particle_value.index(gbest_value)]

iter_count = 0
max_iter = 10000

time_start = time.time()
while iter_count < max_iter:
    
    # Weight decay (Exponential decay)
    w = w0 * np.exp(-lbda*iter_count)

    for i in range(particle_number):

        # Update particle velocity and position
        for j in range(2):
            r1 = np.random.uniform(-1, 1)
            r2 = np.random.uniform(-1, 1)
            particle_velocity[i][j] = w*particle_velocity[i][j] + c1 * r1 * (pbest[i][j] - particle_solution[i][j]) + c2 * r2 * (gbest[j] - particle_solution[i][j])
            particle_solution[i][j] = particle_solution[i][j] + particle_velocity[i][j]
        
        # Calculate particle fitness
        particle_value[i] = f(particle_solution[i][0], particle_solution[i][1])

        # Update particle best
        if particle_value[i] < pbest_value[i]:
            pbest[i] = particle_solution[i]
            pbest_value[i] < particle_value[i]
    
    # Update global best
    min_val = min(pbest_value)
    if min_val < gbest_value:
        gbest_value = min_val
        gbest = particle_solution[particle_value.index(min_val)]

    # Iteration counter
    iter_count += 1
time_end = time.time()

print(
    f"""
    Particle Swarm Optimization Solution
    Best solution found = {gbest[0]}, {gbest[1]}
    Value of best = {gbest_value}
    No. iterations = {max_iter}
    Time elasped = {time_end - time_start}s
    """
)