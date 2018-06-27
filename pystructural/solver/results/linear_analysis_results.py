import numpy as np

from pystructural.solver.components.additional_components.calculation_components import *

from pystructural.solver.components.geometries import line_elements, Point2D
from pystructural.pre_processor.components import LineElementSortComponent

__all__ = ['LinearAnalysisResults2D']


# TODO Change this class with the new components from the linear calculation component
class LinearAnalysisResults2D:
    def __init__(self, structure, analysis):
        self.structure = structure
        self.analysis = analysis
        self.result_entity_id = self.analysis.result_entity_id
        self.dof_calculation_component = self.structure.get_component_from_entity(self.result_entity_id,
                                                                                  DOFCalculationComponent)
        self.linear_calculation_component = self.structure.get_component_from_entity(self.result_entity_id,
                                                                                     LinearCalculationComponent)
        self.displacement_and_load_vectors_component =\
            self.structure.get_component_from_entity(self.result_entity_id, DisplacementAndLoadVectorsComponent)
        # Get the line element sort component
        self.line_element_sort = self.structure.get_component_from_entity(self.structure.general_entity_id,
                                                                          LineElementSortComponent)

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

    def global_dof_generator(self, group_id, dof, load_combination):
        # For every line in the group of line elements
        for node_tuple in self.line_element_sort.line_element_id_generator(group_id):
            # Get the corresponding element of the line
            element = None
            for line_element_class in line_elements:
                if self.structure.get_component_from_entity(node_tuple[0], line_element_class):
                    element = self.structure.get_component_from_entity(node_tuple[0], line_element_class)
                    break
            # Get the local force vector
            local_force_vector = self.get_element_local_force(element, load_combination)
            # Get the first or last three items depending on if the node is the first or the second node in the line
            # The minus for the 1 case is that for the plotting the values are all on one side
            if node_tuple[2] == 0:
                local_force_vector = local_force_vector[:3]
            else:
                local_force_vector = -local_force_vector[-3:]
            # Yield the position of the node and the value of the dof
            yield self.structure.get_component_from_entity(node_tuple[1], Point2D).point_list[0], local_force_vector[
                dof]

    # TODO add a dimension variable to the element class
    def get_element_displacement_vector(self, element_instance, load_combination):
        # Determine the dimension of the element displacement vector
        dim = element_instance.stiffness_matrix.shape[0]

        # Initialize the element displacement vector
        element_displacement_vector = np.zeros([dim])

        # Determine the element displacement vector
        # For every point in the element
        for i in range(dim):
            entity, dof_id = element_instance.get_stiffness_coordinate_to_node_and_dof_variable(i)
            global_id = self.dof_calculation_component.local_to_global_dof_dict[entity][dof_id]
            element_displacement_vector[i] +=\
                self.displacement_and_load_vectors_component.displacement_vectors[load_combination][global_id]

        # Return the element displacement vector
        return element_displacement_vector

    def get_element_global_force(self, element_instance, load_combination):
        # Get the displacement vector of the element
        element_displacement_vector = self.get_element_displacement_vector(element_instance, load_combination)
        # Calculate the global force vector of the element
        element_global_force_vector = np.matmul(element_instance.stiffness_matrix, element_displacement_vector)

        # Return the element global force vector
        return element_global_force_vector

    def get_element_local_force(self, element_instance, load_combination):
        # Return the element local force vector
        return np.matmul(element_instance.geometry.global_to_local_matrix,
                         self.get_element_global_force(element_instance, load_combination))
