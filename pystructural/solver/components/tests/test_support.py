from pystructural.solver.components.support import *


def test_support_init():
    support_0 = Support()
    support_1 = Support(False, False, False, False, False, False)

    assert len(support_0.dof_id_list) is 6
    assert support_0.dof_id_list == [0, 1, 2, 3, 4, 5]

    assert len(support_1.dof_id_list) is 0
    assert support_1.dof_id_list == []