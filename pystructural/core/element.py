__all__ = ['Element']


class Element:
    def __init__(self):
        self.strain_matrix = None
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.nodal_force_vector = None

    def get_dof(self):
        pass

    def compute_matrices(self):
        # Compute all the matrices
        # Shape matrix
        self.compute_shape_matrix()
        # Strain matrix
        self.compute_strain_matrix()
        # Stiffness matrix
        self.compute_stiffness_matrix()
        # Mass matrix
        self.compute_mass_matrix()
        # Nodal force vector
        self.compute_nodal_force_vector()

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