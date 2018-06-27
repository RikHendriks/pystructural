from pystructural.solver.components import Load, DOF

from pystructural.solver.components.geometries import *

__all__ = ['QLoad2D']


# TODO change the class based on if a node is hinged or not
# TODO change the class such that it also has a normal force
# TODO change the class such that it is possible to choose for a global or local q_load
# and add a general direction vector
class QLoad2D(Load):
    compatible_geometry = Line2D

    def __init__(self, q_load_func, load_case_id=None):
        # Initialize the q-load function
        self.q_load_func = q_load_func
        # Initialize the init of the super class
        super().__init__(load_case_id)

    def __add__(self, other):
        self.q_load_func = lambda x: self.q_load_func(x) + other.q_load_func(x)
        return self

    def get_dof(self):
        return DOF(displacement_y=True, rotation_z=True)

    def load_dof_generator(self):
        q_1 = self.q_load_func(self.geometry.point_list[0])
        q_2 = self.q_load_func(self.geometry.point_list[1])
        for i in range(2):
            for dof in self.get_dof().get_dof_id_list():
                if i == 0:
                    if dof == 1:
                        yield [self.geometry.point_id_list[i], dof], (7 * q_1 + 3 * q_2) * self.geometry.length / 20.0
                    elif dof == 5:
                        yield [self.geometry.point_id_list[i], dof],\
                              -1 * (3 * q_1 + 2 * q_2) * self.geometry.length ** 2 / 60.0
                else:
                    if dof == 1:
                        yield [self.geometry.point_id_list[i], dof], (3 * q_1 + 7 * q_2) * self.geometry.length / 20.0
                    elif dof == 5:
                        yield [self.geometry.point_id_list[i], dof],\
                              (2 * q_1 + 3 * q_2) * self.geometry.length ** 2 / 60.0
