import numpy as np

from pystructural.solver.components import Geometry

__all__ = ['Point2D']


class Point2D(Geometry):

    def __init__(self, x, y):
        super().__init__(None, np.array([[x, y]]))
