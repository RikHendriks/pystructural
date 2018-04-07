import numpy as np

from pystructural.solver.components import Load, DOF

from pystructural.solver.components.geometries import *

__all__ = ['PointLoad2D']


class PointLoad2D(Load):
    compatible_geometry = Point2D

    def __init__(self, point_load):
        # Check if the point load is of length 6 else give an error
        if len(point_load) != 3:
            raise TypeError("The input must be a list or numpy array with 3 elements.")
        # Initialize the init of the super class
        super().__init__(np.array(point_load))

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True, rotation_z=True)

    def get_load_value_to_node_and_dof_variable(self, i):
        dof_id_list = self.get_dof().get_dof_id_list()
        return [self.geometry.point_id_list[0], dof_id_list[i]]
