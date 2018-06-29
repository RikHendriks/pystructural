import numpy as np

__all__ = ['point_is_near_point', 'point_is_on_line', 'point_projection_is_on_line', 'is_collinear']


def point_is_near_point(point_0, point_1, error=0.001):
    """Return true iff the two points are near each other.

    :param point_0:
    :param point_1:
    :param error:
    :return:
    """
    return np.linalg.norm(point_0 - point_1) < error


def point_line_projection(point, line_start, line_end):
    """Return the point projection to the line.

    :param point:
    :param line_start:
    :param line_end:
    :return:
    """
    # Determine the projection of the point to the line
    v = line_end - line_start
    w = point - line_start
    return np.dot(v, w) * v / np.linalg.norm(v)


def point_is_on_line(point, line_start, line_end, error=0.001):
    """Return true iff the point intersects the line.

    :param point:
    :param line_start:
    :param line_end:
    :param error:
    :return:
    """
    # We take the wedge- and dot product to determine if the point intersects the line
    v = line_end - point
    w = point - line_start
    return np.linalg.det(np.column_stack((v, w))) < error and np.dot(v, w) > 0


def point_projection_is_on_line(point, line_start, line_end):
    """Return true iff the point projection intersects the line.

    :param point:
    :param line_start:
    :param line_end:
    :return:
    """
    # Determine the projection of the point to the line
    return point_is_on_line(point_line_projection(point, line_start, line_end), line_start, line_end)


def is_collinear(point_0, point_1, point_2, error=0.001):
    """Return true iff the three points are collinear.

    :param point_0:
    :param point_1:
    :param point_2:
    :param error:
    :return:
    """
    # We take the wedge product to determine if the three points are collinear
    v = point_2 - point_1
    w = point_0 - point_1
    return np.linalg.det(np.column_stack((v, w))) < error
