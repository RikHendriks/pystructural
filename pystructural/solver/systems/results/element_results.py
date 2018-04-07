import numpy as np
import catecs

__all__ = ['ElementResults',
           'get_element_displacement_vector',
           'get_element_global_force']


class ElementResults(catecs.System):
    def __init__(self):
        self.dof_calculation_component = None
        self.linear_calculation_component = None
        super().__init__()

    def initialize(self):
        pass

    def process(self):
        pass


# TODO add a dimension variable to the element class
def get_element_displacement_vector(dof_calculation_component, linear_calculation_component, element_instance):
    # Determine the dimension of the element displacement vector
    dim = element_instance.stiffness_matrix.shape[0]

    # Initialize the element displacement vector
    element_displacement_vector = np.zeros([dim])

    # Determine the element displacement vector
    # For every point in the element
    for i in range(dim):
        entity, dof_id = element_instance.get_stiffness_coordinate_to_node_and_dof_variable(i)
        global_id = dof_calculation_component.local_to_global_dof_dict[entity][dof_id]
        element_displacement_vector[i] += linear_calculation_component.displacement_vector[global_id]

    # Return the element displacement vector
    return element_displacement_vector


def get_element_global_force(dof_calculation_component, linear_calculation_component, element_instance):
    # Get the displacement vector of the element
    element_displacement_vector = get_element_displacement_vector(dof_calculation_component,
                                                                  linear_calculation_component,
                                                                  element_instance)
    # Calculate the global force vector of the element
    element_global_force_vector = np.matmul(element_instance.stiffness_matrix, element_displacement_vector)

    # Return the element global force vector
    return element_global_force_vector
