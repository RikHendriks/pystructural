import cecs

from .geometry_systems import UpdateGeometries
from .element_systems import UpdateElements
from .dof_systems import UpdateDOFs
from pystructural.additional_components.calculation_components import *

__all__ = ['InitializeCalculation', 'LinearCalculation']


class InitializeCalculation(cecs.System):
    def initialize(self):
        # Adds a general entity to the world, which holds the 'static' components
        self.world.add_entity(GeneralComponent())


class LinearCalculation(cecs.System):
    def process(self):
        # Check if a linear calculation system category is in self.world then remove it
        if self.world.has_system_category("linear calculation"):
            self.world.remove_system_category("linear calculation")

        # Add system -> Initialize calculation
        self.world.add_system(InitializeCalculation(), "linear calculation")

        # Add system -> update the geometries
        self.world.add_system(UpdateGeometries(), "linear calculation")

        # Add system -> update the elements
        self.world.add_system(UpdateElements(), "linear calculation")

        # Add system -> update the DOFs
        self.world.add_system(UpdateDOFs(), "linear calculation")

        # Add system -> update the reduced DOFs
        # TODO add this system

        # Add system -> compute the global stiffness matrix
        # TODO add this system

        # Process the 'linear calculation' system category
        self.world.process_system_categories("linear calculation")