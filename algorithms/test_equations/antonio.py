"""
"Antonio" test function 

Date: 13/03/22
"""
from algorithms.simulated_annealling import SA

def f(x, y):
    "'Antonio' test function"
    return (2*x)**2 + y**2 + (x - 3)*y

if __name__=="__main__":
    xBounds = [-5,5]
    yBounds = [-5,5]

    sim_ann = SA(xBounds, yBounds)
    sim_ann.algorithm(f)