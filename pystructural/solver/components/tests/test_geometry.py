import math

import numpy as np

from pystructural.solver.components.geometry import *


###########
# LINE 2D #
###########

def test_line_2d_geometry_properties_length():
    line_2d = Line2D(0, 1)
    line_2d.point_list = [np.array([0.0, 0.0]), np.array([10.0, 10.0])]

    line_2d.compute_geometry_properties()

    assert line_2d.length == 10.0 * 2.0 ** 0.5


def test_line_2d_geometry_properties_angle():
    line_2d = Line2D(0, 1)
    line_2d.point_list = [np.array([0.0, 0.0]), np.array([10.0, 10.0])]

    line_2d.compute_geometry_properties()

    assert line_2d.angle == (45 / 180) * math.pi

    line_2d.point_list = [np.array([0.0, 0.0]), np.array([10.0, -10.0])]

    line_2d.compute_geometry_properties()

    assert line_2d.angle == (315 / 180) * math.pi - 2 * math.pi


def test_compute_global_to_local_matrix():
    line_2d = Line2D(0, 1)
    line_2d.point_list = [np.array([0.0, 0.0]), np.array([10.0, 10.0])]

    line_2d.compute_geometry_properties()

    assert np.allclose(np.matmul(line_2d.global_to_local_matrix, np.array([10.0, 0.0, 5.0, 10.0, 0.0, 5.0])),
                       np.array([10.0 / (2.0 ** 0.5), -10.0 / (2.0 ** 0.5), 5.0,
                                 10.0 / (2.0 ** 0.5), -10.0 / (2.0 ** 0.5), 5.0]))


###############
# TRIANGLE 2D #
###############

def test_triangle_2d_geometry_properties_area():
    triangle_2d = Triangle2D(0, 1, 2)
    triangle_2d.point_list = [np.array([0.0, 0.0]), np.array([1.0, 0.0]), np.array([0.0, 1.0])]

    triangle_2d.compute_geometry_properties()

    assert triangle_2d.area == 0.5

    triangle_2d.point_list = [np.array([0.0, 0.0]), np.array([0.0, 1.0]), np.array([1.0, 0.0])]

    triangle_2d.compute_geometry_properties()

    assert triangle_2d.area == 0.5
