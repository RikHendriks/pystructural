__all__ = ['Element']


class Element:
    compatible_geometry = None
    compatible_materials = None
    compatible_element_geometries = None

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

    def get_stiffness_matrix_coordinate_to_node_and_dof_variable(self, x, y):
        pass

    def stiffness_matrix_generator(self):
        dim = self.stiffness_matrix.shape[0]
        for i in range(0, dim):
            for j in range(0, dim):
                yield self.get_stiffness_matrix_coordinate_to_node_and_dof_variable(i, j), self.stiffness_matrix[i][j]

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
