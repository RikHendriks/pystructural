import pytest

from pystructural.solver.components.degree_of_freedom import *


@pytest.fixture
def dof_0():
    return DOF()


@pytest.fixture
def dof_1():
    return DOF(True, True, True, True, True, True)


def test_dof_init(dof_0, dof_1):
    assert len(dof_0.dof_id_list) is 0
    assert dof_0.dof_id_list == []

    assert len(dof_1.dof_id_list) is 6
    assert dof_1.dof_id_list == [0, 1, 2, 3, 4, 5]


def test_update_dof(dof_0, dof_1):
    dof_0.update_dof(dof_0)

    assert len(dof_0.dof_id_list) is 0
    assert dof_0.dof_id_list == []

    dof_0.update_dof(dof_1)

    assert len(dof_0.dof_id_list) is 6
    assert dof_0.dof_id_list == [0, 1, 2, 3, 4, 5]


def test_check_dof_id(dof_0, dof_1):
    for i in range(6):
        assert dof_0.check_dof_id(i) is False
        assert dof_1.check_dof_id(i) is True


def test_update_dof_id_list(dof_0, dof_1):
    dof_0.displacement_x = True
    dof_1.displacement_x = False

    assert len(dof_0.dof_id_list) is 0
    assert dof_0.dof_id_list == []

    assert len(dof_1.dof_id_list) is 6
    assert dof_1.dof_id_list == [0, 1, 2, 3, 4, 5]

    dof_0.update_dof_id_list()
    dof_1.update_dof_id_list()

    assert len(dof_0.dof_id_list) is 1
    assert dof_0.dof_id_list == [0]

    assert len(dof_1.dof_id_list) is 5
    assert dof_1.dof_id_list == [1, 2, 3, 4, 5]
