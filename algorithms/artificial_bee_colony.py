"""
Artificial bee colony Class

Date: 13/03/22
"""
import time
import numpy as np

class ABC():
    """
    Artificial bee colony class
    """

    def __init__(self, xBounds, yBounds):
        """
        Initialize optimization bounds
        """
        self.xlb = min(xBounds)
        self.xub = max(xBounds)

        self.ylb = min(yBounds)
        self.yub = max(yBounds)