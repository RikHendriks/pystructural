from pystructural.core import Element
from pystructural.geometry import Line2D

__all__ = ['FrameElement2D']


class FrameElement2D(Element):

    def __init__(self, line_geometry):
        # Check if the triangle_geometry variable is of the correct type.
        if not isinstance(line_geometry, Line2D):
            raise TypeError("The triangle_geometry variable is not an instance of Triangle2D")
        # Initialize the geometry.
        super().__init__(line_geometry)

    def shape_function(self):
        pass

    def compute_strain_matrix(self):
        pass

    def compute_stiffness_matrix(self):
        pass

    def compute_mass_matrix(self):
        pass

    def compute_nodal_force_vector(self):
        pass