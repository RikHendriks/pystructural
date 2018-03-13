__all__ = ['Element']


class Element:
    compatible_geometry = None
    compatible_materials = None
    compatible_element_geometries = None

    def __init__(self):
        # geometries
        self.geometry = None
        # material and geometries element
        self.material = None
        self.element_geometry = None
        # Matrices
        self.strain_matrix = None
        self.stiffness_matrix = None
        self.mass_matrix = None
        self.nodal_force_vector = None

    def get_dof(self):
        pass

    def compute_element(self):
        # Compute all the matrices
        # Element properties
        self.compute_element_properties()
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

    def compute_element_properties(self):
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