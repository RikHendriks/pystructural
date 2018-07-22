"""
pystructural.solver.components.element_geometry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the various element geometries.
"""
__all__ = ['ElementGeometry',
           'BeamElementGeometry']


class ElementGeometry:
    """The basic element geometry class which each element geometry needs to inherit.
    """

    def __init__(self):
        pass


class BeamElementGeometry(ElementGeometry):
    """The beam element geometry which inherits from the element geometry class.

    :param cross_section_area: The cross section area of the element geometry.
    :param moment_of_inertia: The moment of inertia of the element geometry.
    """

    def __init__(self, cross_section_area, moment_of_inertia):
        self.cross_section_area = cross_section_area
        self.moment_of_inertia = moment_of_inertia
        super().__init__()
