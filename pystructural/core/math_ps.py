import numpy as np

__all__ = ['point_is_near_point', 'point_line_projection', 'point_line_projection_distance',
           'point_is_on_line', 'point_projection_is_on_line', 'is_collinear',
           'line_to_unit_interval', 'line_embedding']


def point_is_near_point(point_0, point_1, error=0.001):
    """Return true iff the two points are near each other.

    :param point_0:
    :param point_1:
    :param error:
    :return:
    """
    return np.linalg.norm(point_0 - point_1) < error


def point_line_projection(point, line_start, line_end):
    """Return the projection of the point on the line.

    :param point:
    :param line_start:
    :param line_end:
    :return:
    """
    # Determine the projection of the point to the line
    v = line_end - line_start
    w = point - line_start
    return line_start + np.dot(v, w) * v / (np.linalg.norm(v) ** 2)


def point_line_projection_distance(point, line_start, line_end):
    """Return the distance from the point to the projection of the point on the line.

    :param point:
    :param line_start:
    :param line_end:
    :return:
    """
    # Get the projection of the point
    projection = point_line_projection(point, line_start, line_end)
    # Return the distance between the projection and the point
    return np.linalg.norm(projection - point)


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
    return abs(np.linalg.det(np.column_stack((v, w)))) < error and np.dot(v, w) >= 0


def point_projection_is_on_line(point, line_start, line_end, error=0.001):
    """Return true iff the point projection intersects the line.

    :param point:
    :param line_start:
    :param line_end:
    :param error:
    :return:
    """
    # Determine the projection of the point to the line
    return point_is_on_line(point_line_projection(point, line_start, line_end), line_start, line_end, error)


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


def line_to_unit_interval(point, line_start, line_end, error=0.001):
    """Put a point on the unit interval of a line.

    :param point:
    :param line_start:
    :param line_end:
    :param error:
    :return:
    """
    if point_is_on_line(point, line_start, line_end, error):
        return np.linalg.norm(point - line_start) / np.linalg.norm(line_end - line_start)
    else:
        return None


def line_embedding(unit, line_start, line_end):
    """Embed a unit on to the line.

    :param unit:
    :param line_start:
    :param line_end:
    :return:
    """
    if 0.0 <= unit <= 1:
        return (1 - unit) * line_start + unit * line_end
    else:
        return None
