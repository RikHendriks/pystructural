from pystructural.core import Element

__all__ = ['LinearTriangleElement2D']


class LinearTriangleElement2D(Element):

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