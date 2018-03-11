from pystructural.core_components import Element
from pystructural.core_components import DOF

from pystructural.geometries import *
from pystructural.materials import *
from pystructural.element_geometries import *

__all__ = ['FrameElement2D']


class FrameElement2D(Element):
    compatible_geometry = Line2D
    compatible_materials = [LinearElasticity2DMaterial]
    compatible_element_geometries = [BeamElementGeometry]

    def __init__(self):
        self.length = None
        self.angle = None
        self.ea = None
        self.ei = None
        super().__init__()

    def get_dof(self):
        return DOF(displacement_x=True, displacement_y=True, rotation_z=True)

    def compute_element_properties(self):
        pass

    def shape_function(self):
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