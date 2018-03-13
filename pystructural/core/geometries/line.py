import numpy as np

from pystructural.core.core_components import Geometry

__all__ = ['Line2D']


class Line2D(Geometry):

    def __init__(self, point_id_1, point_id_2):
        super().__init__([point_id_1, point_id_2], None)

    def compute_area(self):
        self.area = np.linalg.norm(self.point_list[0] - self.point_list[1])