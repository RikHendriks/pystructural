"""
pystructural.solver.components.degree_of_freedom
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the degree of freedom class.
"""
__all__ = ['dof_conversion_dict', 'DOFHolder', 'DOF']


dof_conversion_dict = {0: "displacement_x", 1: "displacement_y", 2: "rotation_z"}


class DOFHolder:

    def __init__(self):
        self.dof_dict = {}
        self.current_dof_id = 0

    def add_dof(self, dof):
        if dof not in self.dof_dict:
            self.dof_dict[dof] = self.current_dof_id
            self.current_dof_id += 1
        return self.dof_dict[dof]


class DOF:
    """The DOF (degree of freedom) class which holds the information of which kinds of DOFs are active for
    a given entity.

    :param *dof_list: A list of degrees of freedom.
    """

    def __init__(self, *dof_list):
        self.dof_set = set(dof_list)
        # Initialize the dof id dict
        self.dof_id_dict = {}

    def update_dof(self, other_dof):
        self.dof_set |= other_dof.dof_set
        self.dof_id_dict.update(other_dof.dof_id_dict)

    def check_dof(self, dof):
        return dof in self.dof_set
