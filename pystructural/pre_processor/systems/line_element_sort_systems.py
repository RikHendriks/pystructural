import copy
import catecs

from pystructural.pre_processor.components import LineElementSortComponent

from pystructural.solver.components.geometries.line import Line2D

__all__ = ['LineElementSort']


class LineElementSort(catecs.System):
    def __init__(self):
        # Initialize the variables used in this system
        self.line_element_sort_component = None
        # Initialize the world
        super().__init__()

    def initialize(self):
        self.line_element_sort_component = self.world.add_component(self.world.general_entity_id,
                                                                    LineElementSortComponent())

    def process(self):
        for group_id in self.world.group_component.groups:
            # Initialize the group in the line element sort component
            self.line_element_sort_component.groups[group_id] = []
            # Initialize the start and end node list and the node list of the group
            node_list = {}
            element_list = {}
            start_end_node_list = {}
            # Determine the start and end node of a group of line elements
            for line_id in self.world.group_component.groups[group_id]:
                line = self.world.get_component_from_entity(line_id, Line2D)
                # For the first and the second node
                for point_id in line.point_id_list:
                    # Add the first or second node to the node list
                    if point_id not in node_list:
                        node_list[point_id] = []
                    node_list[point_id].append(line_id)
                    # Add or remove the node and line id if it is in or not in the list for the first or second node
                    if point_id in start_end_node_list:
                        del start_end_node_list[point_id]
                    else:
                        start_end_node_list[point_id] = line_id
                # Add the node id's to the element list
                element_list[line_id] = {}
                element_list[line_id][line.point_id_list[0]] = 0
                element_list[line_id][line.point_id_list[1]] = 1
            # Pick the first node in the group and the starting element
            node_id = list(start_end_node_list)[0]
            line_id = node_list[node_id][0]
            # iterate over the complete group and sort the group in the line element sort component
            while True:
                # Add the first node of the line to the component
                self.line_element_sort_component.groups[group_id].append(
                    copy.deepcopy((line_id, node_id, element_list[line_id][node_id])))
                # Determine if the node is the first or the second node of the element
                if element_list[line_id][node_id] == 0:
                    second_node = (1, list(element_list[line_id])[1])
                else:
                    second_node = (0, list(element_list[line_id])[0])
                # Add the second node of the line to the component
                self.line_element_sort_component.groups[group_id].append(
                    copy.deepcopy((line_id, second_node[1], second_node[0])))
                # Break if the end of the chain is reached in the group
                if second_node[1] == list(start_end_node_list)[1]:
                    break
                # Set the node id for the next iteration
                node_id = second_node[1]
                # Determine the line_id
                if node_list[node_id][0] == line_id:
                    line_id = node_list[node_id][1]
                else:
                    line_id = node_list[node_id][0]