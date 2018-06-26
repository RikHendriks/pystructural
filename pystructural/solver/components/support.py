from .degree_of_freedom import *

__all__ = ['Support']


class Support(DOF):
    def __init__(self, displacement_x=True, displacement_y=True, displacement_z=True,
                 rotation_x=True, rotation_y=True, rotation_z=True):
        super().__init__(displacement_x, displacement_y, displacement_z, rotation_x, rotation_y, rotation_z)

    def __add__(self, other):
        return (DOF.__add__(self.__neg__(), other.__neg__())).__neg__()
