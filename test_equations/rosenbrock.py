"""
Rosenbrock test function (a=1, b=100)

Date: 13/03/22
"""
from algorithms.simulated_annealling import SA

def f(x, y):
    "Defines objective function"
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2

if __name__=="__main__":
    xBounds = [-5,5]
    yBounds = [-5,5]

    sim_ann = SA(xBounds, yBounds)
    sim_ann.algorithm(f)