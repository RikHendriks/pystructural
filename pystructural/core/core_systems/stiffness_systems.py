import cecs

from pystructural.core.additional_components.calculation_components import *

__all__ = ["ExecuteLinearCalculation"]


class ExecuteLinearCalculation(cecs.System):
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

        # Determine the reduced global stiffness matrix

        # Determine the reduced load vector

        # Compute the reduced displacement vector

        # Determine the displacement vector

        # Determine the load vector
        pass
