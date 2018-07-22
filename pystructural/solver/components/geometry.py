"""
pystructural.solver.components.geometry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the various geometries.
"""
import numpy as np

__all__ = ['Geometry',
           'Point2D', 'Line2D', 'Triangle2D']


class Geometry:
    """The basic geometry class which each geometry needs to inherit. Each geometry is defined by a list of points,
    where each geometry has a list of the id's and of the coordinates of each point.

    :param point_id_list: A list of the id's of each point used in the geometry.
    :param point_list: A list of the coordinates of each point used in the geometry.
    """

    def __init__(self, point_id_list, point_list):
        self.point_id_list = point_id_list
        self.point_list = point_list

    def compute_geometry_properties(self):
        """Computes the properties of the geometry.
        """
        pass


class Point2D(Geometry):
    """The point 2D geometry class, which is an instance of the Geometry class.

    :param x: The x coordinate of the point.
    :param y: The y coordinate of the point.
    """

    def __init__(self, x, y):
        super().__init__(None, np.array([[x, y]]))


class Line2D(Geometry):
    """The line 2D geometry class, which is an instance of the Geometry class.

    :param point_id_1: The id of the start point of the line.
    :param point_id_2: The id of the end point of the line.
    """

    def __init__(self, point_id_1, point_id_2):
        self.length = None
        self.angle = None
        self.global_to_local_matrix = None
        super().__init__([point_id_1, point_id_2], None)

    def compute_geometry_properties(self):
        """Computes the properties of the line 2D geometry.
        """
        # Compute the length of the line
        self.length = np.linalg.norm(self.point_list[0] - self.point_list[1])
        # Compute the angle of the line
        n = self.point_list[1] - self.point_list[0]
        self.angle = np.arctan2(n[1], n[0])
        # Global to local matrix
        self.compute_global_to_local_matrix()

    def compute_global_to_local_matrix(self):
        """Compute and get the local to global matrix.

        :return: Returns the local to global matrix of the element as a NumPy matrix.
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


class Triangle2D(Geometry):
    """The triangle 2D geometry class, which is an instance of the Geometry class.

    :param point_id_1: The id of the first point of the triangle.
    :param point_id_2: The id of the second point of the triangle.
    :param point_id_3: The id of the third point of the triangle.
    """

    def __init__(self, point_id_1, point_id_2, point_id_3):
        self.area = None
        super().__init__([point_id_1, point_id_2, point_id_3], None)

    def compute_geometry_properties(self):
        """Computes the properties of the triangle 2D geometry.
        """
        self.area = abs(0.5 * np.linalg.det(np.array([self.point_list[1] - self.point_list[0],
                                                      self.point_list[2] - self.point_list[0]])))
