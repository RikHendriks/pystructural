"""
pystructural.solver.components.support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the support class.
"""
from .degree_of_freedom import *

__all__ = ['Support']


class Support(DOF):
    """The support class inherits the DOF class. If a DOF is inactive in the support class then that means that the
    degree of freedom is fixed and it is thus not a degree of freedom. The other difference with the DOF class is
    that every DOF is set to active in the initialization of the class.

    :param displacement_x: DOF for the displacement in the x axis.
    :param displacement_y: DOF for the displacement in the y axis.
    :param displacement_z: DOF for the displacement in the z axis.
    :param rotation_x: DOF for the rotation around the x axis.
    :param rotation_y: DOF for the rotation around the y axis.
    :param rotation_z: DOF for the rotation around the z axis.
    """

    def __init__(self, displacement_x=True, displacement_y=True, displacement_z=True,
                 rotation_x=True, rotation_y=True, rotation_z=True):
        # Get the list of the dof's corresponding to the
        dof_id_list = []
        if displacement_x:
            dof_id_list.append("displacement_x")
        if displacement_y:
            dof_id_list.append("displacement_y")
        if displacement_z:
            dof_id_list.append("displacement_z")
        if rotation_x:
            dof_id_list.append("rotation_x")
        if rotation_y:
            dof_id_list.append("rotation_y")
        if rotation_z:
            dof_id_list.append("rotation_z")
        # Initialize the DOF
        super().__init__(*dof_id_list)
