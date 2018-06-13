import numpy as np

from pystructural.solver.components import Geometry

__all__ = ['Line2D']


class Line2D(Geometry):

    def __init__(self, point_id_1, point_id_2):
        self.length = None
        self.angle = None
        self.global_to_local_matrix = None
        super().__init__([point_id_1, point_id_2], None)

    def compute_geometry_properties(self):
        # Compute the length of the line
        self.length = np.linalg.norm(self.point_list[0] - self.point_list[1])
        # Compute the angle of the line
        n = self.point_list[1] - self.point_list[0]
        self.angle = np.arctan2(n[1], n[0])
        # Global to local matrix
        self.compute_global_to_local_matrix()

    def compute_global_to_local_matrix(self):
        """Calculate the local to global matrix.

        :return: (Numpy Array) the local to global matrix of the element.
        """
        c = np.cos(self.angle)
        s = np.sin(self.angle)
        self.global_to_local_matrix = np.zeros((6, 6))
        self.global_to_local_matrix[0, 0] = c
        self.global_to_local_matrix[0, 1] = s
        self.global_to_local_matrix[1, 0] = -s
        self.global_to_local_matrix[1, 1] = c
        self.global_to_local_matrix[2, 2] = 1.0
        self.global_to_local_matrix[3, 3] = c
        self.global_to_local_matrix[3, 4] = s
        self.global_to_local_matrix[4, 3] = -s
        self.global_to_local_matrix[4, 4] = c
        self.global_to_local_matrix[5, 5] = 1.0
