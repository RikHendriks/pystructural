__all__ = ["GroupComponent", "DOFCalculationComponent", "LinearCalculationComponent"]


class GroupComponent:
    def __init__(self):
        # The general group
        self.groups = {}
        self.entities = {}
        # Current group id
        self.current_group_id = 0

    def create_group(self):
        # Create a group
        self.groups[self.current_group_id] = []
        self.current_group_id += 1
        return self.current_group_id - 1

    def add_entity_to_group(self, entity_id, group_id):
        # If the group id is created
        if group_id in self.groups:
            # Add the entity id to the given group
            self.groups[group_id].append(entity_id)
            self.entities[entity_id] = group_id

    def remove_entity(self, entity_id):
        # If the entity is in any group then delete that entity from the structure group component
        if entity_id in self.entities:
            self.groups[self.entities[entity_id]].remove(entity_id)
            del self.entities[entity_id]

    def get_group_id_from_entity(self, entity_id):
        # If the group id exists
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None


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
