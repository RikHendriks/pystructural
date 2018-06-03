import numpy as np
import catecs

from pystructural.solver.components.additional_components.calculation_components import *

__all__ = ['LinearAnalysisResults']


class LinearAnalysisResults:
    def __init__(self, structure, analysis_id):
        self.structure = structure
        self.analysis_id = analysis_id
        self.result_entity_id = self.structure.world.systems[self.analysis_id].result_entity_id
        self.dof_calculation_component = self.structure.world.get_component_from_entity(self.result_entity_id,
                                                                                        DOFCalculationComponent)
        self.linear_calculation_component = self.structure.world.get_component_from_entity(self.result_entity_id,
                                                                                           LinearCalculationComponent)

    # TODO add a dimension variable to the element class
    def get_element_displacement_vector(self, element_instance):
        # Determine the dimension of the element displacement vector
        dim = element_instance.stiffness_matrix.shape[0]

        # Initialize the element displacement vector
        element_displacement_vector = np.zeros([dim])

        # Determine the element displacement vector
        # For every point in the element
        for i in range(dim):
            entity, dof_id = element_instance.get_stiffness_coordinate_to_node_and_dof_variable(i)
            global_id = self.dof_calculation_component.local_to_global_dof_dict[entity][dof_id]
            element_displacement_vector[i] += self.linear_calculation_component.displacement_vector[global_id]

        # Return the element displacement vector
        return element_displacement_vector

    def get_element_global_force(self, element_instance):
        # Get the displacement vector of the element
        element_displacement_vector = self.get_element_displacement_vector(element_instance)
        # Calculate the global force vector of the element
        element_global_force_vector = np.matmul(element_instance.stiffness_matrix, element_displacement_vector)

        # Return the element global force vector
        return element_global_force_vector
