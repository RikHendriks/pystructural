import catecs

from pystructural.core.core_components import DOF, Support
from pystructural.core.additional_components.calculation_components import *

__all__ = ["support_subclasses", "UpdateDOFs", "UpdateReducedDOFs"]


# List of geometries subclasses
support_subclasses = [Support]


class UpdateDOFs(catecs.System):
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


class UpdateReducedDOFs(catecs.System):
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
        # For each global dof id
        for global_dof_id in self.dof_calculation_component.global_to_local_dof_dict:
            entity_id = self.dof_calculation_component.global_to_local_dof_dict[global_dof_id][0]
            dof_id = self.dof_calculation_component.global_to_local_dof_dict[global_dof_id][1]

            # Bool if the global_dof_id is in the reduced dof id dict
            global_in_reduced = True
            # For each support class
            for support_class in support_subclasses:
                # If the entity has an instance of the support class
                if self.world.has_component(entity_id, support_class):
                    support_class_instance = self.world.get_component_from_entity(entity_id, support_class)

                    # If the dof id is in the dof id list of the support instance
                    # then it is also in the reduced dof dict.
                    if dof_id not in support_class_instance.get_dof_id_list():
                        global_in_reduced = False

            # If the global id is in the reduced matrix then add it to the correct dicts
            if global_in_reduced:
                # Put the current_id in the global_to_reduced_dof_dict
                self.dof_calculation_component.global_to_reduced_dof_dict[global_dof_id] = current_dof_id
                # Put the global_dof_id in the reduced_to_global_dof_dict
                self.dof_calculation_component.reduced_to_global_dof_dict[current_dof_id] = global_dof_id

                current_dof_id += 1
