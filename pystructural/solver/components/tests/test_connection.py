import pytest

from pystructural.solver.components.connection import *


@pytest.fixture
def spring_0():
    return Spring()


@pytest.fixture
def spring_1():
    return Spring(1.0, 2.0, 1.0, 2.0, 1.0, 2.0)


def test_spring_init_dof(spring_0, spring_1):
    assert len(spring_0.dof_id_list) is 0
    assert spring_0.dof_id_list == []

    assert len(spring_1.dof_id_list) is 6
    assert spring_1.dof_id_list == [0, 1, 2, 3, 4, 5]


def test_spring_spring_dof_generator(spring_0, spring_1):

    for _ in spring_0.spring_dof_generator():
        assert False

    i = 0
    for dof_id, spring_value in spring_1.spring_dof_generator():
        assert dof_id == i
        assert spring_value == 1.0 if i % 2 == 0 else 2.0
        i += 1
