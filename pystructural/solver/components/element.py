import numpy as np

from pystructural.solver.components.geometry import Line2D, Triangle2D
from pystructural.solver.components.degree_of_freedom import DOF
from pystructural.solver.components.material import LinearElasticity2DMaterial
from pystructural.solver.components.element_geometry import BeamElementGeometry

__all__ = ['Element',
           'FrameElement2D', 'LinearTriangleElement2D',
           'line_elements', 'triangle_elements']


class Element:
    compatible_geometry = None
    compatible_materials = None
    compatible_element_geometries = None
    element_dimension = None

    def __init__(self):
        # Geometry
        self.geometry = None
        # Material and geometries element
        self.material = None
        self.element_geometry = None
        # Matrices
        self.strain_matrix = None
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.nodal_force_vector = None

    def get_dof(self):
        pass

    def get_stiffness_coordinate_to_node_and_dof_variable(self, x):
        pass

    def get_node_and_dof_variable_to_stiffness_coordinate(self, node_id, dof_id):
        pass

    def stiffness_matrix_dof_generator(self):
        dim = self.stiffness_matrix.shape[0]
        for i in range(0, dim):
            for j in range(0, dim):
                yield [self.get_stiffness_coordinate_to_node_and_dof_variable(i),
                       self.get_stiffness_coordinate_to_node_and_dof_variable(j)],\
                      self.stiffness_matrix[i][j]

    def compute_element(self):
        # Compute all the matrices
        # Element properties
        self.compute_element_properties()
        # Stiffness matrix
        self.compute_stiffness_matrix()
        # Mass matrix
        self.compute_mass_matrix()
        # Nodal force vector
        self.compute_nodal_force_vector()

    def compute_element_properties(self):
        pass

    def compute_stiffness_matrix(self):
        pass

    def compute_mass_matrix(self):
        pass

    def compute_nodal_force_vector(self):
        pass


class FrameElement2D(Element):
    compatible_geometry = Line2D
    compatible_materials = [LinearElasticity2DMaterial]
    compatible_element_geometries = [BeamElementGeometry]
    element_dimension = 6

    def __init__(self):
        # Element properties
        self.ea = None
        self.ei = None
        # Element matrices
        self.local_stiffness_matrix = None
        self.global_to_local_matrix = None
        super().__init__()

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True, rotation_z=True)

    def get_stiffness_coordinate_to_node_and_dof_variable(self, x):
        dof_id_list = self.get_dof().get_dof_id_list()
        return self.geometry.point_id_list[x//3], dof_id_list[x % 3]

    def get_node_and_dof_variable_to_stiffness_coordinate(self, node_id, dof_id):
        if node_id == self.geometry.point_id_list[0]:
            return {0: 0, 1: 1, 5: 2}[dof_id]
        else:
            return {0: 3, 1: 4, 5: 5}[dof_id]

    def compute_element_properties(self):
        # Compute the ea
        self.ea = self.material.youngs_modulus * self.element_geometry.cross_section_area
        # Compute the ei
        self.ei = self.material.youngs_modulus * self.element_geometry.moment_of_inertia
        # Compute the local stiffness matrix and the global to local matrix
        self.calculate_local_stiffness_matrix()

    def calculate_local_stiffness_matrix(self):
        """Calculate the local stiffness matrix.

        :return: (Numpy Array) the local stiffness matrix.
        """
        self.local_stiffness_matrix = np.zeros((6, 6))
        self.local_stiffness_matrix[0, 0] = 1.0 * (self.ea / self.geometry.length)
        self.local_stiffness_matrix[0, 3] = -1.0 * (self.ea / self.geometry.length)
        self.local_stiffness_matrix[3, 0] = -1.0 * (self.ea / self.geometry.length)
        self.local_stiffness_matrix[3, 3] = 1.0 * (self.ea / self.geometry.length)
        # If node 1 is fixed and node 2 is fixed:
        # First quadrant
        self.local_stiffness_matrix[1, 1] = 12.0 * (self.ei / (self.geometry.length ** 3))
        self.local_stiffness_matrix[2, 1] = -6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[1, 2] = -6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[2, 2] = 4.0 * (self.ei / self.geometry.length)
        # Second quadrant
        self.local_stiffness_matrix[4, 1] = -12.0 * (self.ei / (self.geometry.length ** 3))
        self.local_stiffness_matrix[5, 1] = -6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[4, 2] = 6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[5, 2] = 2.0 * (self.ei / self.geometry.length)
        # Third quadrant
        self.local_stiffness_matrix[1, 4] = -12.0 * (self.ei / (self.geometry.length ** 3))
        self.local_stiffness_matrix[2, 4] = 6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[1, 5] = -6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[2, 5] = 2.0 * (self.ei / self.geometry.length)
        # Fourth quadrant
        self.local_stiffness_matrix[4, 4] = 12.0 * (self.ei / (self.geometry.length ** 3))
        self.local_stiffness_matrix[5, 4] = 6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[4, 5] = 6.0 * (self.ei / (self.geometry.length ** 2))
        self.local_stiffness_matrix[5, 5] = 4.0 * (self.ei / self.geometry.length)

    def rotate_by_local_to_global_matrix(self, input_matrix, clockwise=True):
        """Rotate the input vector or matrix by the local to global matrix.

        :param input_matrix: (Numpy Array) the input vector or matrix.
        :param clockwise: (Bool) determines if it returns clockwise or counterclockwise.
        :return: the rotated vector
        """
        if clockwise:
            return np.matmul(np.matmul(np.transpose(self.geometry.global_to_local_matrix), input_matrix),
                             self.geometry.global_to_local_matrix)
        else:
            return np.matmul(np.matmul(self.geometry.global_to_local_matrix, input_matrix),
                             np.transpose(self.geometry.global_to_local_matrix))

    def compute_stiffness_matrix(self):
        """Calculate the global stiffness matrix.

        :return: (Numpy Array) the global stiffness matrix.
        """
        self.stiffness_matrix = self.rotate_by_local_to_global_matrix(self.local_stiffness_matrix)

    def compute_mass_matrix(self):
        pass

    def compute_nodal_force_vector(self):
        pass


class LinearTriangleElement2D(Element):
    compatible_geometry = Triangle2D
    compatible_materials = []
    compatible_element_geometries = []
    element_dimension = 6

    def __init__(self):
        super().__init__()

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True)

    def get_stiffness_coordinate_to_node_and_dof_variable(self, x):
        pass

    def get_node_and_dof_variable_to_stiffness_coordinate(self, node_id, dof_id):
        pass

    def compute_element_properties(self):
        pass

    def shape_function(self, i):
        pass

    def compute_shape_matrix(self):
        pass

    def compute_strain_matrix(self):
        pass

    def compute_stiffness_matrix(self):
        pass

    def compute_mass_matrix(self):
        pass

    def compute_nodal_force_vector(self):
        pass


line_elements = [FrameElement2D]
triangle_elements = [LinearTriangleElement2D]
