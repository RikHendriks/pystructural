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

    :param displacement_x: DOF for the displacement in the x axis, dof id: 0.
    :param displacement_y: DOF for the displacement in the y axis, dof id: 1.
    :param displacement_z: DOF for the displacement in the z axis, dof id: 2.
    :param rotation_x: DOF for the rotation around the x axis, dof id: 3.
    :param rotation_y: DOF for the rotation around the y axis, dof id: 4.
    :param rotation_z: DOF for the rotation around the z axis, dof id: 5.
    """

    def __init__(self, displacement_x=True, displacement_y=True, displacement_z=True,
                 rotation_x=True, rotation_y=True, rotation_z=True):
        super().__init__(displacement_x, displacement_y, displacement_z, rotation_x, rotation_y, rotation_z)
