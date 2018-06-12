import catecs

from pystructural.core.math import point_is_near_point, point_is_on_line
from pystructural.solver.components.geometries import Line2D, Point2D

__all__ = ['SplitLine']


class SplitLine(catecs.System):
    def process(self):
        # Split a line if a point intersects it and is not currently a start of end node of a line
        # For every point for every line
        for point_id, point in self.world.get_component(Point2D):
            for line_id, line in self.world.get_component(Line2D):
                # Get the start and end node of the line
                line_start_point = self.world.get_component_from_entity(line.point_id_list[0], Point2D)
                line_end_point = self.world.get_component_from_entity(line.point_id_list[1], Point2D)

                # If the point is near a node of the line then break
                if point_is_near_point(point.point_list[0], line_start_point.point_list[0]) or \
                        point_is_near_point(point.point_list[0], line_end_point.point_list[0]):
                    break

                # Check if the point is on the line
                if point_is_on_line(point.point_list[0], line_start_point.point_list[0], line_end_point.point_list[0]):
                    # Create two new lines that exist on top of the existing line
                    line_1_id = self.world.copy_entity(line_id)
                    line_2_id = self.world.copy_entity(line_id)
                    # Set their nodes correctly
                    self.world.get_component_from_entity(line_1_id, Line2D).point_id_list[1] = point_id
                    self.world.get_component_from_entity(line_2_id, Line2D).point_id_list[0] = point_id
                    # Add the two lines to the group of the group of the original frame element entity
                    group_id = self.world.group_component.get_group_id_from_entity(line_id)
                    self.world.group_component.add_entity_to_group(line_1_id, group_id)
                    self.world.group_component.add_entity_to_group(line_2_id, group_id)
                    # Delete the original entity from the group
                    self.world.group_component.remove_entity(line_id)
                    # Delete the line from the structure
                    self.world.delete_entity(line_id, True)
                    # Break the for loop
                    break
