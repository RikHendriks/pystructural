import numpy as np

from pystructural.solver.core_components import Geometry

__all__ = ['Point2D']


class Point2D(Geometry):

    def __init__(self, x, y):
        super().__init__(None, np.array([[x, y]]))

    def compute_area(self):
        self.area = 0.0
