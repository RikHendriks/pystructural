import numpy as np
import catecs

import copy

from pystructural.core.additional_components.calculation_components import *
from pystructural.core.core_systems.element_systems import element_subclasses_2d
from pystructural.core.core_systems.load_systems import load_subclasses_2d

__all__ = ["ExecuteLinearCalculation"]


class ExecuteLinearCalculation(catecs.System):
    def __init__(self):
        self.dof_calculation_component = None
        self.linear_calculation_component = None
        super().__init__()

    def initialize(self):
        # For the general component
        for entity, _ in self.world.get_component(GeneralComponent):
            # If the general entity doesn't have the dof calculation component then add it
            if not self.world.has_component(entity, DOFCalculationComponent):
                self.world.add_component(entity, DOFCalculationComponent())
            self.dof_calculation_component = self.world.get_component_from_entity(entity, DOFCalculationComponent)

            # If the general entity doesn't have the linear calculation component then add it
            if not self.world.has_component(entity, LinearCalculationComponent):
                self.world.add_component(entity, LinearCalculationComponent())
            self.linear_calculation_component = self.world.get_component_from_entity(entity, LinearCalculationComponent)

    def process(self):
        # Determine the global stiffness matrix
        # Initialize the global stiffness matrix
        dim_global_stiffness_matrix = len(self.dof_calculation_component.global_to_local_dof_dict)
        self.linear_calculation_component.global_stiffness_matrix =\
            np.zeros([dim_global_stiffness_matrix, dim_global_stiffness_matrix])
        # Process all the 2d elements and put its local stiffness matrices in the global stiffness matrix
        for element_class in element_subclasses_2d:
            for entity, components in self.world.get_components(element_class.compatible_geometry, element_class):
                # For each dof in the element
                for data in components[1].stiffness_matrix_dof_generator():
                    i = self.dof_calculation_component.local_to_global_dof_dict[data[0][0][0]][data[0][0][1]]
                    j = self.dof_calculation_component.local_to_global_dof_dict[data[0][1][0]][data[0][1][1]]
                    self.linear_calculation_component.global_stiffness_matrix[i][j] += data[1]

        # Determine the reduced global stiffness matrix
        # Initialize the reduced global stiffness matrix as a copy of the global stiffness matrix
        self.linear_calculation_component.reduced_global_stiffness_matrix =\
            copy.deepcopy(self.linear_calculation_component.global_stiffness_matrix)
        # Initialize the remove id list
        remove_id_list = []
        # Get the id's that need to be removed from the global stiffness matrix
        # to get the reduced global stiffness matrix
        for i in range(0, len(self.linear_calculation_component.global_stiffness_matrix)):
            if i not in self.dof_calculation_component.global_to_reduced_dof_dict:
                remove_id_list.append(i)
        # Remove the rows and columns to get the reduced global stiffness matrix
        self.linear_calculation_component.reduced_global_stiffness_matrix =\
            np.delete(self.linear_calculation_component.reduced_global_stiffness_matrix, remove_id_list, 0)
        self.linear_calculation_component.reduced_global_stiffness_matrix =\
            np.delete(self.linear_calculation_component.reduced_global_stiffness_matrix, remove_id_list, 1)

        # TODO Change how this works based on forces that act where supports are and other edge cases that are not covered.
        # Determine the reduced load vector
        # Initialize the reduced load vector
        self.linear_calculation_component.reduced_load_vector =\
            np.zeros([len(self.linear_calculation_component.reduced_global_stiffness_matrix)])
        # Process all the 2d loads and put them into the reduced load vector
        for load_class in load_subclasses_2d:
            for entity, components in self.world.get_components(load_class.compatible_geometry, load_class):
                # For each dof in the load
                for data in components[1].load_dof_generator():
                    i = self.dof_calculation_component.local_to_global_dof_dict[data[0][0]][data[0][1]]
                    r_i = self.dof_calculation_component.global_to_reduced_dof_dict[i]
                    # If the load is in the reduced load vector then add it
                    if r_i:
                        self.linear_calculation_component.reduced_load_vector[r_i] += data[1]

        # Compute the reduced displacement vector
        self.linear_calculation_component.reduced_displacement_vector =\
            np.linalg.solve(self.linear_calculation_component.reduced_global_stiffness_matrix,
                            self.linear_calculation_component.reduced_load_vector)

        # Determine the displacement vector
        # Initialize the displacement vector
        self.linear_calculation_component.displacement_vector =\
            np.zeros([len(self.linear_calculation_component.global_stiffness_matrix)])
        # Put the values of the reduced displacement vector in the displacement vector
        for i in range(0, len(self.linear_calculation_component.reduced_displacement_vector)):
            self.linear_calculation_component.displacement_vector\
                [self.dof_calculation_component.reduced_to_global_dof_dict[i]] =\
                self.linear_calculation_component.reduced_displacement_vector[i]

        # Determine the load vector
        self.linear_calculation_component.load_vector =\
            np.matmul(self.linear_calculation_component.global_stiffness_matrix,
                      self.linear_calculation_component.displacement_vector)
