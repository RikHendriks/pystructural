import cecs

from pystructural.core_components import DOF
from pystructural.additional_components.calculation_components import *

__all__ = ["UpdateDOFs"]


# TODO add the dictionaries as a component to the general entity
class UpdateDOFs(cecs.System):
    def __init__(self):
        self.dof_calculation_component = None
        super().__init__()

    def initialize(self):
        for entity, _ in self.world.get_component(GeneralComponent):
            self.world.add_component(entity, DOFCalculationComponent())
            self.dof_calculation_component = self.world.get_component_from_entity(entity, DOFCalculationComponent)

    def process(self):
        # Set the current DOF id to zero
        current_dof_id = 0
        # For each DOF instance in the world
        for entity, component in self.world.get_component(DOF):
            # dictionary value to a dictionary
            self.dof_calculation_component.local_to_global_dof_dict[entity] = {}
            # Get the dof id list
            dof_id_list = component.get_dof_id_list()
            # Put each id of the list in the dictionary
            for dof_id in dof_id_list:
                self.dof_calculation_component.local_to_global_dof_dict[entity][dof_id] = current_dof_id
                current_dof_id += 1
                # Put the current_id in the global_to_local_dof_dict
                self.dof_calculation_component.global_to_local_dof_dict[current_dof_id] = [entity, dof_id]