import numpy as np
import catecs

from ..solver.components import element_geometries, elements, geometries, loads, materials, support,\
    additional_components
from ..solver.systems import LinearAnalysis

from ..pre_processor.pre_processor import PreProcessor2D

__all__ = ['Structure2D']


class Structure2D(catecs.World):
    def __init__(self):
        # Initialize the world
        super().__init__()
        # Initialize the general entity for all the static components of the structure
        self.general_entity_id = self.add_entity(additional_components.GroupComponent())
        # Get the group component
        self.group_component = self.get_component_from_entity(self.general_entity_id,
                                                              additional_components.GroupComponent)

    def search_for_point(self, position, error=0.001):
        for entity, point in self.get_component(geometries.Point2D):
            if np.linalg.norm(position - point.point_list[0]) < error:
                return entity
        else:
            return None

    def position_to_id(self, position):
        if isinstance(position, list):
            return self.search_for_point(position)
        else:
            return position

    def add_node(self, position):
        return self.add_entity(geometries.Point2D(position[0], position[1]))

    def add_frame_element(self, start_position, end_position, youngs_modulus, mass_density, cross_section_area,
                          moment_of_inertia):
        entity_start_id = self.position_to_id(start_position)
        entity_end_id = self.position_to_id(end_position)

        if entity_start_id is None:
            entity_start_id = self.add_node(start_position)

        if entity_end_id is None:
            entity_end_id = self.add_node(end_position)

        # Create the frame element entity
        frame_element_id  = self.add_entity(geometries.Line2D(entity_start_id, entity_end_id),
                                            elements.FrameElement2D(),
                                            materials.LinearElasticity2DMaterial(youngs_modulus, mass_density),
                                            element_geometries.BeamElementGeometry(cross_section_area,
                                                                                   moment_of_inertia))

        # Create the group for the frame element entity
        group_id = self.group_component.create_group()
        self.group_component.add_entity_to_group(frame_element_id, group_id)

        # Return the frame element entity id
        return frame_element_id

    def add_support(self, position, displacement_x=True, displacement_y=True, rotation_z=True):
        entity_id = self.position_to_id(position)
        if entity_id is None:
            entity_id = self.add_node(position)
        self.add_component(entity_id, support.Support(displacement_x=displacement_x, displacement_y=displacement_y,
                                                      rotation_z=rotation_z))

    def add_point_load(self, position, load):
        entity_id = self.position_to_id(position)
        if entity_id is None:
            entity_id = self.add_node(position)
        self.add_component(entity_id, loads.PointLoad2D(load))

    def solve_linear_system(self):
        # Add a preprocessor system and run it
        pp_id = self.add_system(PreProcessor2D())
        # Process the preprocessor system
        self.process_systems(pp_id)
        # Remove the preprocessor system
        self.remove_system(pp_id)

        # Add linear calculation system
        s_id = self.add_system(LinearAnalysis("linear_calculation"))
        # Process linear calculation system
        self.process_systems(s_id)
