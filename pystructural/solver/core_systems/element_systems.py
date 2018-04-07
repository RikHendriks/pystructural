import catecs

from pystructural.solver.core_components import DOF
from pystructural.solver.elements import FrameElement2D, LinearTriangleElement2D

__all__ = ["element_subclasses_2d", "UpdateElements"]


# List of all Element subclasses
element_subclasses_2d = [FrameElement2D, LinearTriangleElement2D]


# TODO add errors when no geometry, material and element_geometry is found
class UpdateElements(catecs.System):
    def process(self):
        # Process all the 2d elements
        for element_class in element_subclasses_2d:
            for entity, components in self.world.get_components(element_class.compatible_geometry, element_class):

                # Determine the geometry of the element
                components[1].geometry = components[0]

                # Determine the material of the element
                for material_class in element_class.compatible_materials:
                    if self.world.has_component(entity, material_class):
                        components[1].material = self.world.get_component_from_entity(entity, material_class)
                        break

                # Determine the element_geometry of the element
                for element_geometry_class in element_class.compatible_element_geometries:
                    if self.world.has_component(entity, element_geometry_class):
                        components[1].element_geometry = self.world.get_component_from_entity(entity, element_geometry_class)
                        break

                # Compute the matrices of the elements
                components[1].compute_element()

                # Add the dof of the element to the dof of the nodes of the element
                # For every point in the element
                for point_entity in components[0].point_id_list:
                    # Check if the point has a DOF component, if not then add it
                    if not self.world.has_component(point_entity, DOF):
                        self.world.add_component(point_entity, DOF())
                    # Get the dof from the elements and update the node dof
                    self.world.get_component_from_entity(point_entity, DOF).update_dof(components[1].get_dof())
