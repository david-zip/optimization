"""
Third attempt at implementing PSO for a minimisation problem (Rosenbrock Equation)

Looking to implement directly from pseudocode rather than following a tutorial

Date: 07/03/22
"""
import imp
import time
import random
import numpy as np

def f(x, y):
    "Defines objective function"
    a = 1
    b = 100
    return (a - x)**2 + b*(y - x**2)**2


