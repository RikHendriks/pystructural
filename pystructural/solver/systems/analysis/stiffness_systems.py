import numpy as np
import catecs

import copy

from pystructural.solver.components.additional_components.calculation_components import *
from pystructural.solver.components.connections.spring import Spring
from pystructural.solver.systems.analysis.element_systems import element_subclasses_2d
from pystructural.solver.systems.analysis.load_systems import load_subclasses_2d, imposed_load_subclasses_2d

__all__ = ['ExecuteLinearCalculation',
           'UpdateGlobalAndReducedStiffnessMatrices',
           'UpdateLoadCombinations',
           'UpdateDisplacementAndLoadVectors']


# TODO See Asana entry in the Results section <- the load combinations need to be done inside the data components
class ExecuteLinearCalculation(catecs.System):
    def __init__(self, result_entity_id, load_combinations):
        self.dof_calculation_component = None
        self.linear_calculation_component = None
        self.reduced_load_vectors_component = None
        self.displacement_and_load_vectors_component = None
        self.result_entity_id = result_entity_id
        self.load_combinations = load_combinations
        super().__init__()

    def initialize(self):
        # If the result entity doesn't have the dof calculation component then add it
        if not self.world.has_component(self.result_entity_id, DOFCalculationComponent):
            self.world.add_component(self.result_entity_id, DOFCalculationComponent())
        self.dof_calculation_component = self.world.get_component_from_entity(self.result_entity_id,
                                                                              DOFCalculationComponent)

        # If the result entity doesn't have the linear calculation component then add it
        if not self.world.has_component(self.result_entity_id, LinearCalculationComponent):
            self.world.add_component(self.result_entity_id, LinearCalculationComponent())
        self.linear_calculation_component = self.world.get_component_from_entity(self.result_entity_id,
                                                                                 LinearCalculationComponent)

        # If the result entity doesn't have the linear calculation component then add it
        if not self.world.has_component(self.result_entity_id, ReducedLoadVectorsComponent):
            self.world.add_component(self.result_entity_id, ReducedLoadVectorsComponent())
        self.reduced_load_vectors_component = self.world.get_component_from_entity(self.result_entity_id,
                                                                                   ReducedLoadVectorsComponent)

        # If the result entity doesn't have the linear calculation component then add it
        if not self.world.has_component(self.result_entity_id, DisplacementAndLoadVectorsComponent):
            self.world.add_component(self.result_entity_id, DisplacementAndLoadVectorsComponent())
        self.displacement_and_load_vectors_component =\
            self.world.get_component_from_entity(self.result_entity_id, DisplacementAndLoadVectorsComponent)

    def process(self):
        # Run system instance: update global and reduced stiffness matrices
        self.world.run_system(UpdateGlobalAndReducedStiffnessMatrices(self.dof_calculation_component,
                                                                      self.linear_calculation_component))
        # Run system instance: update load combinations
        self.world.run_system(UpdateLoadCombinations(self.dof_calculation_component, self.linear_calculation_component,
                                                     self.reduced_load_vectors_component))
        # Run system instance: update displacement and load vectors
        self.world.run_system(UpdateDisplacementAndLoadVectors(self.dof_calculation_component,
                                                               self.linear_calculation_component,
                                                               self.reduced_load_vectors_component,
                                                               self.displacement_and_load_vectors_component,
                                                               self.load_combinations))


class UpdateGlobalAndReducedStiffnessMatrices(catecs.System):
    def __init__(self, dof_calculation_component, linear_calculation_component):
        self.dof_calculation_component = dof_calculation_component
        self.linear_calculation_component = linear_calculation_component
        super().__init__()

    def process(self):
        # Determine the global stiffness matrix
        # Initialize the global stiffness matrix
        dim_global_stiffness_matrix = len(self.dof_calculation_component.global_to_local_dof_dict)
        self.linear_calculation_component.global_stiffness_matrix = \
            np.zeros([dim_global_stiffness_matrix, dim_global_stiffness_matrix])
        # Process all the 2d elements and put its local stiffness matrices in the global stiffness matrix
        for element_class in element_subclasses_2d:
            for entity, components in self.world.get_components(element_class.compatible_geometry, element_class):
                # For each dof in the element
                for data in components[1].stiffness_matrix_dof_generator():
                    i = self.dof_calculation_component.local_to_global_dof_dict[data[0][0][0]][data[0][0][1]]
                    j = self.dof_calculation_component.local_to_global_dof_dict[data[0][1][0]][data[0][1][1]]
                    self.linear_calculation_component.global_stiffness_matrix[i][j] += data[1]

        # Add the connection springs to the global stiffness matrix
        for entity, component in self.world.get_component(Spring):
            for dof, spring_value in component.spring_dof_generator():
                if entity in self.dof_calculation_component.local_to_global_dof_dict:
                    if dof in self.dof_calculation_component.local_to_global_dof_dict[entity]:
                        global_id = self.dof_calculation_component.local_to_global_dof_dict[entity][dof]
                        self.linear_calculation_component.global_stiffness_matrix[global_id][global_id] += spring_value

        # Determine the reduced global stiffness matrix
        # Initialize the reduced global stiffness matrix as a copy of the global stiffness matrix
        self.linear_calculation_component.reduced_global_stiffness_matrix = \
            copy.deepcopy(self.linear_calculation_component.global_stiffness_matrix)
        # Initialize the remove id list
        remove_id_list = []
        # Get the id's that need to be removed from the global stiffness matrix
        # to get the reduced global stiffness matrix
        for i in range(0, len(self.linear_calculation_component.global_stiffness_matrix)):
            if i not in self.dof_calculation_component.global_to_reduced_dof_dict:
                remove_id_list.append(i)
        # Remove the rows and columns to get the reduced global stiffness matrix
        self.linear_calculation_component.reduced_global_stiffness_matrix = \
            np.delete(self.linear_calculation_component.reduced_global_stiffness_matrix, remove_id_list, 0)
        self.linear_calculation_component.reduced_global_stiffness_matrix = \
            np.delete(self.linear_calculation_component.reduced_global_stiffness_matrix, remove_id_list, 1)


class UpdateLoadCombinations(catecs.System):
    def __init__(self, dof_calculation_component, linear_calculation_component, reduced_load_vectors_component):
        self.dof_calculation_component = dof_calculation_component
        self.linear_calculation_component = linear_calculation_component
        self.reduced_load_vectors_component = reduced_load_vectors_component
        super().__init__()

    def process(self):
        # TODO Change how this works based on forces that act where supports are and other edge cases that are not covered.
        # TODO Such one edge case is if a dof load is applied where the dof is not in the reduced vector.
        # Determine the reduced load vector
        # Process all the 2d loads and put them into the reduced load vector
        for load_class in load_subclasses_2d:
            for entity, components in self.world.get_components(load_class.compatible_geometry, load_class):
                # For each dof in the load
                for data in components[1].load_dof_generator():
                    i = self.dof_calculation_component.local_to_global_dof_dict[data[0][0]][data[0][1]]
                    # If the load is in the reduced load vector then add it
                    if i in self.dof_calculation_component.global_to_reduced_dof_dict:
                        r_i = self.dof_calculation_component.global_to_reduced_dof_dict[i]
                        # Add the load to the correct load combinations and use the correct factors
                        for load_combination_id, factor in self.world.load_combinations_component.load_case_generator(
                                components[1].load_case_id):
                            if load_combination_id not in self.reduced_load_vectors_component.reduced_load_vectors:
                                self.reduced_load_vectors_component.reduced_load_vectors[load_combination_id] =\
                                    np.zeros([len(self.linear_calculation_component.reduced_global_stiffness_matrix)])
                            self.reduced_load_vectors_component.reduced_load_vectors[load_combination_id][r_i] +=\
                                factor * data[1]


class UpdateDisplacementAndLoadVectors(catecs.System):
    def __init__(self, dof_calculation_component, linear_calculation_component, reduced_load_vectors_component,
                 displacement_and_load_vectors_component, load_combinations):
        self.dof_calculation_component = dof_calculation_component
        self.linear_calculation_component = linear_calculation_component
        self.reduced_load_vectors_component = reduced_load_vectors_component
        self.displacement_and_load_vectors_component = displacement_and_load_vectors_component
        self.load_combinations = load_combinations
        super().__init__()

    def process(self):
        if isinstance(self.load_combinations, list):
            for load_combination_id in self.load_combinations:
                self.solve_system_for_load_case(load_combination_id)
        else:
            self.solve_system_for_load_case(self.load_combinations)

    def solve_system_for_load_case(self, load_combination_id):
        # Compute the reduced displacement vector
        self.displacement_and_load_vectors_component.reduced_displacement_vectors[load_combination_id] = \
            np.linalg.solve(self.linear_calculation_component.reduced_global_stiffness_matrix,
                            self.reduced_load_vectors_component.reduced_load_vectors[load_combination_id])

        # Determine the displacement vector
        # Initialize the displacement vector
        if load_combination_id not in self.displacement_and_load_vectors_component.displacement_vectors:
            self.displacement_and_load_vectors_component.displacement_vectors[load_combination_id] = \
                np.zeros([len(self.linear_calculation_component.global_stiffness_matrix)])
        # Put the values of the reduced displacement vector in the displacement vector
        for i in range(0, len(self.displacement_and_load_vectors_component.reduced_displacement_vectors[load_combination_id])):
            self.displacement_and_load_vectors_component.displacement_vectors[load_combination_id][
                self.dof_calculation_component.reduced_to_global_dof_dict[i]] = \
                self.displacement_and_load_vectors_component.reduced_displacement_vectors[load_combination_id][i]

        # Determine the load vector
        self.displacement_and_load_vectors_component.load_vectors[load_combination_id] = \
            np.matmul(self.linear_calculation_component.global_stiffness_matrix,
                      self.displacement_and_load_vectors_component.displacement_vectors[load_combination_id])

        # Subtract the imposed loads from the load vector
        # For each imposed load
        for load_class in imposed_load_subclasses_2d:
            for entity, components in self.world.get_components(load_class.compatible_geometry, load_class):
                # For each dof in the load
                for data in components[1].load_dof_generator():
                    i = self.dof_calculation_component.local_to_global_dof_dict[data[0][0]][data[0][1]]
                    factor = self.world.load_combinations_component.load_combinations[load_combination_id][
                        components[1].load_case_id]
                    # Subtract the imposed load from the load vector
                    self.displacement_and_load_vectors_component.load_vectors[load_combination_id][i] -= \
                        factor * data[1]
