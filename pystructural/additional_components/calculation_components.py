__all__ = ["GeneralComponent", "DOFCalculationComponent"]


class GeneralComponent:
    pass


class DOFCalculationComponent:
    def __init__(self):
        # id_stiffness[node_id][variable_id] = stiffness_matrix_id
        self.local_to_global_dof_dict = {}
        # id_node[stiffness_matrix_id] = [node_id, variable_id]
        self.global_to_local_dof_dict = {}
        # id_reduced_stiffness[stiffness_matrix_id] = reduced_stiffness_matrix_id
        self.global_to_reduced_dof_dict = {}
        # id_node_reduced[reduced_stiffness_matrix_id] = [stiffness_matrix_id]
        self.reduced_to_global_dof_dict = {}


class LinearCalculationComponent:
    def __init__(self):
        # stiffness matrices
        self.global_stiffness_matrix = None
        self.reduced_global_stiffness_matrix = None
        # Displacement vectors
        self.displacement_vector = None
        self.reduced_displacement_vector = None
        # Load vectors
        self.load_vector = None
        self.reduced_load_vector = None
        # Dof calculation component
        self.dof_calculation_component = None

    # TODO implement this function inside a system
    def compute_linear_calculation(self, dof_calculation_component):
        # Determine the reduced global stiffness vector and the reduced load vector

        # Compute the reduced displacement vector

        # Determine the displacement vector

        # Determine the load vector
        pass