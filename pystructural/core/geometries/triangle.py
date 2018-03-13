import numpy as np

from pystructural.core.core_components import Geometry

__all__ = ['Triangle2D']


class Triangle2D(Geometry):

    def __init__(self, point_id_1, point_id_2, point_id_3):
        super().__init__([point_id_1, point_id_2, point_id_3], None)

    def compute_area(self):
        self.area = 0.5 * np.linalg.det(np.array([self.point_list[1] - self.point_list[0],
                                                  self.point_list[2] - self.point_list[0]]))