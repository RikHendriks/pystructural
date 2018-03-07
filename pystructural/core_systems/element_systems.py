import cecs

from pystructural.core import DOF
from pystructural.geometry import Line2D, Triangle2D
from pystructural.elements import FrameElement2D, LinearTriangleElement2D

__all__ = ["element_subclasses_2d", "UpdateElements"]


# List of all Element subclasses
element_subclasses_2d = [[Line2D, FrameElement2D], [Triangle2D, LinearTriangleElement2D]]


class UpdateElements(cecs.System):
    def process(self):
        # Process all the 2d elements
        for element_class_list in element_subclasses_2d:
            for entity, components in self.world.get_components(element_class_list[0], element_class_list[1]):

                # Compute the matrices of the elements
                components[1].compute_matrices()

                # Add the dof of the element to the dof of the nodes of the element
                # For every point in the element
                for point_entity in components[0].point_id_list:
                    # Check if the point has a DOF component, if not then add it
                    if not self.world.has_component(point_entity, DOF):
                        self.world.add_component(point_entity, DOF())
                    # Get the dof from the elements and update the node dof
                    self.world.get_component_from_entity(point_entity, DOF).updage_dof(components[1].get_dof())