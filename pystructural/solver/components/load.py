import numpy as np

from pystructural.solver.components.degree_of_freedom import dof_conversion_dict, DOF
from pystructural.solver.components.geometry import Point2D, Line2D

__all__ = ['Load', 'ImposedLoad',
           'PointLoad2D', 'QLoad2D',
           'ImposedLoad2D']


class Load(DOF):
    compatible_geometry = None

    def __init__(self, load_case_id, dof_id_list):
        # Geometry
        self.geometry = None
        # Load combination id
        self.load_case_id = load_case_id
        # dof
        super().__init__(*dof_id_list)

    def load_dof_generator(self):
        pass


class ImposedLoad(Load):
    def __init__(self, load_case_id, dof_id_list):
        super().__init__(load_case_id, dof_id_list)


class PointLoad2D(Load):
    compatible_geometry = Point2D

    def __init__(self, point_load, load_case_id=None):
        # Check if the point load is of length 3 else give an error
        if len(point_load) != 3:
            raise TypeError("The input must be a list or numpy array with 3 elements.")
        self.point_load = np.array(point_load)
        # Initialize the init of the super class
        super().__init__(load_case_id, ["displacement_x", "displacement_y", "rotation_z"])

    def __add__(self, other):
        self.point_load += other.point_load_list
        return self

    def load_dof_generator(self):
        for i in range(0, len(self.point_load)):
            yield [self.geometry.point_id_list[0], self.dof_id_dict[dof_conversion_dict[i]]], self.point_load[i]


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
        super().__init__(load_case_id, ["displacement_y", "rotation_z"])

    def __add__(self, other):
        self.q_load_func = lambda x: self.q_load_func(x) + other.q_load_func(x)
        return self

    def load_dof_generator(self):
        q_1 = self.q_load_func(self.geometry.point_list[0])
        q_2 = self.q_load_func(self.geometry.point_list[1])
        for i in range(2):
            for dof in self.dof_id_dict:
                if i == 0:
                    if dof == "displacement_y":
                        yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                              (7 * q_1 + 3 * q_2) * self.geometry.length / 20.0
                    elif dof == "rotation_z":
                        yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                              -1 * (3 * q_1 + 2 * q_2) * self.geometry.length ** 2 / 60.0
                else:
                    if dof == "displacement_y":
                        yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                              (3 * q_1 + 7 * q_2) * self.geometry.length / 20.0
                    elif dof == "rotation_z":
                        yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                              (2 * q_1 + 3 * q_2) * self.geometry.length ** 2 / 60.0


class ImposedLoad2D(ImposedLoad):
    compatible_geometry = Line2D

    def __init__(self, imposed_load, load_case_id=None):
        # Check if the point load is of length 3 else give an error
        if len(imposed_load) != 2:
            raise TypeError("The input must be a list or numpy array with 3 elements.")
        self.imposed_load = np.array(imposed_load)
        # Initialize the init of the super class
        super().__init__(load_case_id, ["displacement_x", "displacement_y", "rotation_z"])

    def load_dof_generator(self):
        # Initialize the global force vector
        global_force_vector = np.array([self.imposed_load[0], 0.0, self.imposed_load[1],
                                        -self.imposed_load[0], 0.0, -self.imposed_load[1]])
        # Transform the global force vector to the local space of the element
        local_force_vector = np.matmul(np.transpose(self.geometry.global_to_local_matrix), global_force_vector)
        # Yield the load dofs
        for i in range(2):
            for dof in self.dof_id_dict:
                if i == 0:
                    yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                          local_force_vector[{"displacement_x": 0, "displacement_y": 1, "rotation_z": 2}[dof]]
                else:
                    yield [self.geometry.point_id_list[i], self.dof_id_dict[dof]],\
                          local_force_vector[{"displacement_x": 3, "displacement_y": 4, "rotation_z": 5}[dof]]
