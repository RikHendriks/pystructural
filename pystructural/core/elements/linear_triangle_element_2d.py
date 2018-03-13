from pystructural.core_components import Element
from pystructural.core_components import DOF

from pystructural.geometries import *

__all__ = ['LinearTriangleElement2D']


class LinearTriangleElement2D(Element):
    compatible_geometry = Triangle2D
    compatible_materials = []
    compatible_element_geometries = []

    def __init__(self):
        super().__init__()

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True)

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