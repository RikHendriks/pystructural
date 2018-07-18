import itertools
import copy

import catecs

from pystructural.core.math_ps import quotient_set_of_equivalence_relation, point_is_near_point
from pystructural.solver.components.geometries import Point2D, Line2D

__all__ = ['CheckOverlappingNodes2D']


class CheckOverlappingNodes2D(catecs.System):
    def __init__(self, minimum_node_distance):
        self.minimum_node_distance = minimum_node_distance
        super().__init__()

    def process(self):
        # Defines the point equivalence relation
        def point_equivalence_relation(point_0, point_1):
            return point_is_near_point(point_0[1].point_list[0], point_1[1].point_list[0], self.minimum_node_distance)

        # Get the quotient set defined by the point equivalence relation
        quotient_set = quotient_set_of_equivalence_relation(self.world.get_component(Point2D),
                                                            point_equivalence_relation)

        # Create a copy node for each equivalence class and copy the components to that node
        for equivalence_class in quotient_set:
            # Create the copied node
            equ_point = Point2D(equivalence_class[1].point_list[0][0], equivalence_class[1].point_list[0][1])
            equ_point_id = self.world.add_entity(equ_point)
            # Add all the phase_id lists to each other
            equ_point.phase_id_list = []
            for point in quotient_set[equivalence_class]:
                if hasattr(point[1], 'phase_id_list'):
                    for phase_id in point[1].phase_id_list:
                        if phase_id not in equ_point.phase_id_list:
                            equ_point.phase_id_list.append(phase_id)
                # Copy all the components that are not an instance of the point 2d class
                for component in self.world.get_all_components_from_entity(point[0]):
                    if not isinstance(component, Point2D):
                        self.world.add_component(equ_point_id, copy.deepcopy(component))
                # Set all the node id's of the line elements correctly that have a node in this equivalence class
                for line_id, line in self.world.get_component(Line2D):
                    for i in range(2):
                        if point[0] == line.point_id_list[i]:
                            line.point_id_list[i] = equ_point_id
            # Delete all the other nodes
            for point in quotient_set[equivalence_class]:
                self.world.delete_entity(point[0], True)
