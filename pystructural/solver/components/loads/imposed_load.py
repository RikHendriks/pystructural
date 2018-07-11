import numpy as np

from pystructural.solver.components import DOF
from pystructural.solver.components.loads import ImposedLoad

from pystructural.solver.components.geometries import *

__all__ = ['ImposedLoad2D']


class ImposedLoad2D(ImposedLoad):
    compatible_geometry = Line2D

    def __init__(self, imposed_load, load_case_id=None):
        # Check if the point load is of length 3 else give an error
        if len(imposed_load) != 2:
            raise TypeError("The input must be a list or numpy array with 3 elements.")
        self.imposed_load = np.array(imposed_load)
        # Initialize the init of the super class
        super().__init__(load_case_id)

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True, rotation_z=True)

    def load_dof_generator(self):
        # Initialize the global force vector
        global_force_vector = np.array([self.imposed_load[0], 0.0, self.imposed_load[1],
                                        -self.imposed_load[0], 0.0, -self.imposed_load[1]])
        # Transform the global force vector to the local space of the element
        local_force_vector = np.matmul(np.transpose(self.geometry.global_to_local_matrix), global_force_vector)
        # Yield the load dofs
        for i in range(2):
            for dof in self.get_dof().get_dof_id_list():
                if i == 0:
                    yield [self.geometry.point_id_list[i], dof], local_force_vector[{0: 0, 1: 1, 5: 2}[dof]]
                else:
                    yield [self.geometry.point_id_list[i], dof], local_force_vector[{0: 3, 1: 4, 5: 5}[dof]]
