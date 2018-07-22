import numpy as np

from pystructural.core.math_ps import *


def test_is_near_point():
    p1 = np.array([0.0, 0.0])
    p2 = np.array([0.0, 0.00099])
    p3 = np.array([0.0, 1.0])

    assert point_is_near_point(p1, p1)
    assert point_is_near_point(p1, p2)
    assert not point_is_near_point(p1, p3)


def test_point_line_projection():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])
    p3 = np.array([-2.0, 0.0])

    assert np.allclose(p1, point_line_projection(p1, l1, l2))
    assert np.allclose(-p1, point_line_projection(-p1, l1, l2))
    assert np.allclose(np.array([0.0, 0.0]), point_line_projection(p2, l1, l2))
    assert np.allclose(np.array([-1.0, -1.0]), point_line_projection(p3, l1, l2))


def test_point_line_projection_distance():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])
    p3 = np.array([-2.0, 0.0])

    assert -0.001 < point_line_projection_distance(p1, l1, l2) < 0.001
    assert -0.001 < point_line_projection_distance(-p1, l1, l2) < 0.001
    assert 2 ** 0.5 - 0.001 < point_line_projection_distance(p2, l1, l2) < 2 ** 0.5 + 0.001
    assert 2 ** 0.5 - 0.001 < point_line_projection_distance(p3, l1, l2) < 2 ** 0.5 + 0.001


def test_point_is_on_line():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])

    assert point_is_on_line(p1, l1, l2)
    assert not point_is_on_line(-p1, l1, l2)
    assert not point_is_on_line(p2, l1, l2)

    assert not point_is_on_line(np.array([5.0, 0.0]), np.array([0.0, 0.0]), np.array([10.0, 10.0]))


def test_point_projection_is_on_line():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])
    p3 = np.array([-2.0, 0.0])

    assert point_projection_is_on_line(p1, l1, l2)
    assert not point_projection_is_on_line(-p1, l1, l2)
    assert point_projection_is_on_line(p2, l1, l2)
    assert not point_projection_is_on_line(p3, l1, l2)


def test_is_collinear():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])

    assert is_collinear(p1, l1, l2)
    assert is_collinear(-p1, l1, l2)
    assert not is_collinear(p2, l1, l2)


def test_line_to_unit_interval():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])
    p2 = np.array([-1.0, 1.0])

    assert line_to_unit_interval(p1, l1, l2) == 0.5
    assert line_to_unit_interval(0.5 * p1, l1, l2) == 0.25

    assert line_to_unit_interval(p2, l1, l2) is None


def test_line_embedding():
    l1 = np.array([0.0, 0.0])
    l2 = np.array([1.0, 1.0])

    p1 = np.array([0.5, 0.5])

    assert np.allclose(line_embedding(0.5, l1, l2), p1)
    assert np.allclose(line_embedding(0.25, l1, l2), 0.5 * p1)

    assert line_embedding(-0.1, l1, l2) is None
    assert line_embedding(1.1, l1, l2) is None


def test_quotient_set_of_equivalence_relation():
    def equivalence_relation(e_1, e_2):
        return e_1 % 2 == e_2 % 2

    quotient_set = quotient_set_of_equivalence_relation(range(10), equivalence_relation)

    assert quotient_set[0] == [0, 2, 4, 6, 8]
    assert quotient_set[1] == [1, 3, 5, 7, 9]
