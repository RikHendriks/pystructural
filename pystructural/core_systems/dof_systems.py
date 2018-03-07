import cecs

from pystructural.core import DOF

__all__ = ["UpdateDOFs"]


class UpdateDOFs(cecs.System):
    def __init__(self):
        self.local_to_global_dof_dict = {}
        self.global_to_local_dof_dict = {}
        super().__init__()

    def process(self):
        # Set the current DOF id to zero
        current_dof_id = 0
        # For each DOF instance in the world
        for entity, component in self.world.get_component(DOF):
            # dictionary value to a dictionary
            self.local_to_global_dof_dict[entity] = {}
            # Get the dof id list
            dof_id_list = DOF.get_dof_id_list()
            # Put each id of the list in the dictionary
            for dof_id in dof_id_list:
                self.local_to_global_dof_dict[entity][dof_id] = current_dof_id
                current_dof_id += 1
                # Put the current_id in the global_to_local_dof_dict
                self.global_to_local_dof_dict[current_dof_id] = [entity, dof_id]