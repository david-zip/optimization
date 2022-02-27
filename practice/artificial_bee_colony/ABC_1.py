"""
Initial attempt on implementing Artificial Bee Colony into Python

Date: 27/02/22
"""
import numpy as np
import matplotlib.pyplot as plt

# Define fitness function
def f(x,y):
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x)**2

# Create employed bee and provide inital solution
beehive_population = 100

employed_bee_militia = {}
employed_bee_solutions = {}

for i in range(int(beehive_population/2)):
    bee_name = "Employed Bee {}".format(i+1)
    employed_bee_militia[bee_name] = np.random.rand(2,1)
    
    x, y = employed_bee_militia[bee_name][0], employed_bee_militia[bee_name][0]
    employed_bee_solutions[bee_name] = f(x,y)

# Shows solution found by each emplyed bee
"""
for name, array in employed_bee_militia.items():
    print("{}\t:\t{}\n\t\t\t{}\n".format(name, array[0], array[1]))
"""

iter_count = 0
itermax = 100
while iter_count < itermax:
    for key in employed_bee_militia.keys():
        

    iter_count += 1







