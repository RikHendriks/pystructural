import numpy as np
import catecs

from ..solver.components import element_geometries, elements, geometries, loads, materials, support
from ..solver.systems import LinearAnalysis

__all__ = ['Structure2D']


# TODO make the inputs for the positions also an id and check which is which
class Structure2D:
    def __init__(self):
        self.world = catecs.World()

    def search_for_point(self, position, error=0.001):
        for entity, point in self.world.get_component(geometries.Point2D):
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
        return self.world.add_entity(geometries.Point2D(position[0], position[1]))

    def add_frame_element(self, start_position, end_position, youngs_modulus, mass_density, cross_section_area,
                          moment_of_inertia):
        entity_start_id = self.position_to_id(start_position)
        entity_end_id = self.position_to_id(end_position)

        if entity_start_id is None:
            entity_start_id = self.add_node(start_position)

        if entity_end_id is None:
            entity_end_id = self.add_node(end_position)

        return self.world.add_entity(geometries.Line2D(entity_start_id, entity_end_id), elements.FrameElement2D(),
                                     materials.LinearElasticity2DMaterial(youngs_modulus, mass_density),
                                     element_geometries.BeamElementGeometry(cross_section_area, moment_of_inertia))

    def add_support(self, position, displacement_x=True, displacement_y=True, rotation_z=True):
        entity_id = self.position_to_id(position)
        if entity_id is not None:
            self.world.add_component(entity_id, support.Support(displacement_x=displacement_x,
                                                                displacement_y=displacement_y, rotation_z=rotation_z))

    def add_point_load(self, position, load):
        entity_id = self.position_to_id(position)
        if entity_id is not None:
            self.world.add_component(entity_id, loads.PointLoad2D(load))

    def solve_linear_system(self):
        # Add linear calculation system
        s_id = self.world.add_system(LinearAnalysis())

        # Process linear calculation system
        self.world.process_systems(s_id)
