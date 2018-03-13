from pystructural.core.core_components.element_geometry import *

__all__ = ['BeamElementGeometry']


class BeamElementGeometry(ElementGeometry):
    def __init__(self, cross_section_area, moment_of_inertia):
        self.cross_section_area = cross_section_area
        self.moment_of_inertia = moment_of_inertia
        super().__init__()