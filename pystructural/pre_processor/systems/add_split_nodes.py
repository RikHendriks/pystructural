import numpy as np
import catecs

from pystructural.solver.components.geometries import Line2D, Point2D

__all__ = ['AddSplitNodes']


class AddSplitNodes(catecs.System):
    def __init__(self, minimum_element_distance):
        self.minimum_distance = minimum_element_distance
        super().__init__()

    def process(self):
        # For every line the structure
        for line_id, line in self.world.get_component(Line2D):
            # Get the start and end node of the line
            line_start_point = self.world.get_component_from_entity(line.point_id_list[0], Point2D).point_list[0]
            line_end_point = self.world.get_component_from_entity(line.point_id_list[1], Point2D).point_list[0]
            # Get the vector from start to end
            line_vector = line_end_point - line_start_point
            # The amount of splits
            splits = int(np.linalg.norm(line_vector) / self.minimum_distance)
            # Add points at the splits
            for i in range(splits - 1):
                node_position = line_start_point + (i + 1) * (line_vector / float(splits))
                print(node_position)
                self.world.add_entity(Point2D(*node_position))
