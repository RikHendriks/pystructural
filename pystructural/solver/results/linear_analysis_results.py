import numpy as np

import copy

from pystructural.solver.components.calculation_components import *

from pystructural.solver.systems.analysis.element_systems import element_subclasses_2d
from pystructural.solver.components.geometry import Point2D
from pystructural.solver.components.element import line_elements
from pystructural.pre_processor.components import LineElementSortComponent
from pystructural.solver.systems.analysis.load_systems import imposed_load_subclasses_2d

from .results import *

__all__ = ['LinearAnalysisResults2D']


class LinearAnalysisResults2D:
    def __init__(self, structure, result_entity_id):
        self.structure = structure
        self.result_entity_id = result_entity_id
        self.dof_calculation_component = self.structure.get_component_from_entity(self.result_entity_id,
                                                                                  DOFCalculationComponent)
        self.linear_calculation_component = self.structure.get_component_from_entity(self.result_entity_id,
                                                                                     LinearCalculationComponent)
        self.displacement_and_load_vectors_component =\
            self.structure.get_component_from_entity(self.result_entity_id, DisplacementAndLoadVectorsComponent)
        # Get the line element sort component
        self.line_element_sort = self.structure.get_component_from_entity(self.structure.general_entity_id,
                                                                          LineElementSortComponent)
        # Initialize the line results dict
        self.line_results = {}
        # Initialize the linear phase analysis results
        self.linear_phase_analysis_results = []

    def add_linear_phase_analysis_result(self, linear_phase_analysis_result, load_combinations):
        # Add the linear phase analysis results to the list
        self.linear_phase_analysis_results.append([linear_phase_analysis_result, load_combinations])

    # def update_linear_phase_analysis_results(self):
    #     # If a linear analysis results is given then add the results to the results of the current analysis
    #     for phase_analysis, load_combinations in self.linear_phase_analysis_results:
    #         for load_combination in load_combinations:
    #             # For each element in the displacement vector
    #             for i in self.dof_calculation_component.global_to_local_dof_dict:
    #                 # Get the global dof
    #                 entity_id, dof = self.dof_calculation_component.global_to_local_dof_dict[i]
    #                 # If the same dof exists in the linear analysis result
    #                 if entity_id in phase_analysis.dof_calculation_component.local_to_global_dof_dict:
    #                     if dof in phase_analysis.dof_calculation_component.local_to_global_dof_dict[entity_id]:
    #                         j = phase_analysis.dof_calculation_component.local_to_global_dof_dict[entity_id][dof]
    #                         self.displacement_and_load_vectors_component.displacement_vectors[load_combination][i] += \
    #                             phase_analysis.displacement_and_load_vectors_component.displacement_vectors[
    #                                 load_combination][j]
    #                 # If the same dof exists in the linear analysis result
    #                 if entity_id in phase_analysis.dof_calculation_component.local_to_global_dof_dict:
    #                     if dof in phase_analysis.dof_calculation_component.local_to_global_dof_dict[entity_id]:
    #                         j = phase_analysis.dof_calculation_component.local_to_global_dof_dict[entity_id][dof]
    #                         self.displacement_and_load_vectors_component.load_vectors[load_combination][i] += \
    #                             phase_analysis.displacement_and_load_vectors_component.load_vectors[
    #                                 load_combination][j]

    def calculate_line_result(self, group_id):
        line_start = self.structure.get_component_from_entity(self.line_element_sort.groups[group_id][0][1],
                                                              Point2D)
        line_end = self.structure.get_component_from_entity(self.line_element_sort.groups[group_id][-1][1], Point2D)
        self.line_results[group_id] = LineResults(line_start.point_list[0], line_end.point_list[0])

        # For each load combination add the line values of the group
        for load_combination in self.structure.load_combinations_component.load_combinations:
            line_values = []
            for position_vector, dof_value in self.global_dof_generator(group_id, load_combination):
                line_values.append([position_vector, dof_value, load_combination])
            # Add the line values to the LineResults instance
            self.line_results[group_id].add_line_values(line_values)

    def group_tangent_vector(self, group_id):
        # Get the generator for the group
        line_element_generator = self.line_element_sort.line_element_id_generator(group_id)
        # Get the id's of the first and the second node
        first_node_tuple = next(line_element_generator)
        second_node_tuple = next(line_element_generator)
        # Get the position of the first and the second node
        first_node_position = self.structure.get_component_from_entity(first_node_tuple[1], Point2D).point_list[0]
        second_node_position = self.structure.get_component_from_entity(second_node_tuple[1], Point2D).point_list[0]
        # Get the vector from the first to the second node
        vector = second_node_position - first_node_position
        # Get the tangent vector
        tangent_vector = np.zeros(2)
        tangent_vector[0] = vector[1]
        tangent_vector[1] = -vector[0]
        # Return the normalized tangent vector
        return tangent_vector / np.linalg.norm(tangent_vector)

    def displacement_generator(self, group_id, load_combination):
        # For every line in the group of line elements
        for node_tuple in self.line_element_sort.line_element_id_generator(group_id):
            # Get the corresponding element of the line
            element = None
            for line_element_class in line_elements:
                if self.structure.get_component_from_entity(node_tuple[0], line_element_class):
                    element = self.structure.get_component_from_entity(node_tuple[0], line_element_class)
                    break
            # Get the displacement vector of the element
            displacement_vector = self.get_element_displacement_vector(element, load_combination)
            # Get the first or last three items depending on if the node is the first or the second node in the line
            if node_tuple[2] == 0:
                displacement_vector = displacement_vector[:3]
            else:
                displacement_vector = displacement_vector[-3:]
            # Yield the position of the node and the displacement
            yield self.structure.get_component_from_entity(node_tuple[1], Point2D).point_list[0], displacement_vector[
                                                                                                  :2]

    def global_dof_generator(self, group_id, load_combination):
        # For every line in the group of line elements
        for node_tuple in self.line_element_sort.line_element_id_generator(group_id):
            # Get the corresponding element of the line
            element = None
            for line_element_class in line_elements:
                if self.structure.get_component_from_entity(node_tuple[0], line_element_class):
                    element = self.structure.get_component_from_entity(node_tuple[0], line_element_class)
                    break
            # Get the local force vector
            local_force_vector = self.get_element_local_force_vector(element, load_combination)
            # Get the first or last three items depending on if the node is the first or the second node in the line
            # The minus for the 1 case is that for the plotting the values are all on one side
            if node_tuple[2] == 0:
                local_force_vector = local_force_vector[:3]
            else:
                local_force_vector = -local_force_vector[-3:]
            # Yield the position of the node and the value of the dof
            yield self.structure.get_component_from_entity(node_tuple[1], Point2D).point_list[0], local_force_vector

    # TODO define a load combination variable that automatically deletes every load combination not in the variable
    # from the yield
    def global_dof_enveloping_generator(self, group_id):
        # Initialize a LineResult instance if the group id doesn't have one yet
        if group_id not in self.line_results:
            self.calculate_line_result(group_id)

        # For each combined line value
        for position_vector, dof_value_list, load_combination_list in self.line_results[group_id]\
                .combined_line_value_generator():
            yield position_vector, dof_value_list, load_combination_list

    def get_node_displacement_vector(self, node_instance, load_combination, phased=True):
        # Initialize the node displacement vector
        node_displacement_vector = np.zeros([3])

        # Determine the entity id
        node_id = node_instance.point_id_list[0]

        # Determine the node displacement vector
        for i in range(3):
            j = copy.deepcopy(i)
            if j == 2:
                j = 5
            global_id = self.dof_calculation_component.local_to_global_dof_dict[node_id][j]
            node_displacement_vector[i] += \
                self.displacement_and_load_vectors_component.displacement_vectors[load_combination][global_id]

        # If linear phased analysis results are added to the node displacement vector then add it
        if phased:
            # For every load combination in every phase analysis
            for phase_analysis, load_combinations in self.linear_phase_analysis_results:
                if load_combination in load_combinations:
                    try:
                        node_displacement_vector += phase_analysis.get_node_displacement_vector(node_instance,
                                                                                                load_combination)
                    except KeyError:
                        pass
        # Return the node displacement vector
        return node_displacement_vector

    def get_node_global_force(self, node_instance, load_combination, phased=True):
        # Initialize the node global force vector
        node_force_vector = np.zeros([3])

        # Determine the entity id
        node_id = node_instance.point_id_list[0]

        # Determine the node displacement vector
        for i in range(3):
            j = copy.deepcopy(i)
            if j == 2:
                j = 5
            global_id = self.dof_calculation_component.local_to_global_dof_dict[node_id][j]
            node_force_vector[i] += \
                self.displacement_and_load_vectors_component.load_vectors[load_combination][global_id]

        # If linear phased analysis results are added to the node force vector then add it
        if phased:
            # For every load combination in every phase analysis
            for phase_analysis, load_combinations in self.linear_phase_analysis_results:
                if load_combination in load_combinations:
                    try:
                        node_force_vector += phase_analysis.get_node_global_force_vector(node_instance,
                                                                                         load_combination)
                    except KeyError:
                        pass
        # Return the node global force vector
        return node_force_vector

    def get_support_node_global_force(self, node_instance, load_combination, phased=True):
        # Initialize the support force vector
        support_force_vector = np.zeros(3)

        # For all elements in the structure
        for element_class in element_subclasses_2d:
            for entity, components in self.structure.get_components(element_class.compatible_geometry, element_class):
                # Check if the node_instance is used in the element
                for i in range(len(components[1].geometry.point_id_list)):
                    if node_instance.entity_id == components[1].geometry.point_id_list[i]:
                        support_force_vector += self.get_element_global_force_vector(components[1], load_combination)[
                            3*i:3*i+3]
                        break

        # If linear phased analysis results are added to the support force vector then add it
        if phased:
            # For every load combination in every phase analysis
            for phase_analysis, load_combinations in self.linear_phase_analysis_results:
                if load_combination in load_combinations:
                    try:
                        support_force_vector += phase_analysis.get_support_node_global_force(node_instance,
                                                                                             load_combination)
                    except KeyError:
                        pass
        # Return the support global force vector
        return support_force_vector

    def get_element_displacement_vector(self, element_instance, load_combination, phased=True):
        # Determine the dimension of the element displacement vector
        dim = element_instance.element_dimension

        # Initialize the element displacement vector
        element_displacement_vector = np.zeros([dim])

        # Determine the element displacement vector
        # For every point in the element
        for i in range(dim):
            entity, dof_id = element_instance.get_stiffness_coordinate_to_node_and_dof_variable(i)
            global_id = self.dof_calculation_component.local_to_global_dof_dict[entity][dof_id]
            element_displacement_vector[i] +=\
                self.displacement_and_load_vectors_component.displacement_vectors[load_combination][global_id]

        # If linear phased analysis results are added to the element displacement vector then add it
        if phased:
            # For every load combination in every phase analysis
            for phase_analysis, load_combinations in self.linear_phase_analysis_results:
                if load_combination in load_combinations:
                    try:
                        element_displacement_vector += phase_analysis.get_element_displacement_vector(element_instance,
                                                                                                      load_combination)
                    except KeyError:
                        pass
        # Return the element displacement vector
        return element_displacement_vector

    def get_element_global_force_vector(self, element_instance, load_combination, phased=True):
        # Get the displacement vector of the element
        element_displacement_vector = self.get_element_displacement_vector(element_instance, load_combination, False)
        # Calculate the global force vector of the element
        element_global_force_vector = np.matmul(element_instance.stiffness_matrix, element_displacement_vector)
        # Subtract the imposed loads from the force vector
        # For each imposed load
        for load_class in imposed_load_subclasses_2d:
            components = self.structure.get_all_component_types_from_entity(element_instance.entity_id,
                                                                            load_class.compatible_geometry, load_class)
            if components is not None:
                for imposed_load in components[1]:
                    # For each dof in the load
                    for data in imposed_load.load_dof_generator():
                        i = element_instance.get_node_and_dof_variable_to_stiffness_coordinate(data[0][0], data[0][1])
                        if imposed_load.load_case_id in \
                                self.structure.load_combinations_component.load_combinations[load_combination]:
                            factor = self.structure.load_combinations_component.load_combinations[load_combination][
                                imposed_load.load_case_id]
                            # Subtract the imposed load from the load vector
                            element_global_force_vector[i] -= factor * data[1]

        # If linear phased analysis results are added to the element global force vector then add it
        if phased:
            # For every load combination in every phase analysis
            for phase_analysis, load_combinations in self.linear_phase_analysis_results:
                if load_combination in load_combinations:
                    try:
                        element_global_force_vector += phase_analysis.get_element_global_force_vector(element_instance,
                                                                                                      load_combination)
                    except KeyError:
                        pass
        # Return the element global force vector
        return element_global_force_vector

    def get_element_local_force_vector(self, element_instance, load_combination, phased=True):
        # Return the element local force vector
        return np.matmul(element_instance.geometry.global_to_local_matrix,
                         self.get_element_global_force_vector(element_instance, load_combination, phased))
