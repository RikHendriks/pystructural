import cecs

from pystructural.core.core_components import DOF
from pystructural.core.additional_components.calculation_components import *

from pystructural.core.supports import Support2D

__all__ = ["support_subclasses_2d", "UpdateDOFs", "UpdateReducedDOFs"]


# List of geometries subclasses
support_subclasses_2d = [Support2D]


# TODO add the dictionaries as a component to the general entity
class UpdateDOFs(cecs.System):
    def __init__(self):
        self.dof_calculation_component = None
        super().__init__()

    def initialize(self):
        # For the general component
        for entity, _ in self.world.get_component(GeneralComponent):
            # If the general entity doesn't have the dof calculation component then add it
            if not self.world.has_component(entity, DOFCalculationComponent):
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
                # Put the current_id in the local_to_global_to_local_dof_dict
                self.dof_calculation_component.local_to_global_dof_dict[entity][dof_id] = current_dof_id
                # Put the entity id and the dof id in the global_to_local_dof_dict
                self.dof_calculation_component.global_to_local_dof_dict[current_dof_id] = [entity, dof_id]
                # Update the current dof id
                current_dof_id += 1


class UpdateReducedDOFs(cecs.System):
    def __init__(self):
        self.dof_calculation_component = None
        super().__init__()

    def initialize(self):
        # For the general component
        for entity, _ in self.world.get_component(GeneralComponent):
            # If the general entity doesn't have the dof calculation component then add it
            if not self.world.has_component(entity, DOFCalculationComponent):
                self.world.add_component(entity, DOFCalculationComponent())
            self.dof_calculation_component = self.world.get_component_from_entity(entity, DOFCalculationComponent)

    def process(self):
        # For each support component in the world
        for support_class in support_subclasses_2d:
            for entity, component in self.world.get_component(support_class):
                pass