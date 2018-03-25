import cecs

from .geometry_systems import UpdateGeometries
from .element_systems import UpdateElements
from .dof_systems import UpdateDOFs, UpdateReducedDOFs
from .stiffness_systems import ExecuteLinearCalculation
from pystructural.core.additional_components.calculation_components import *

__all__ = ['InitializeCalculation', 'LinearCalculation']


class InitializeCalculation(cecs.System):
    def initialize(self):
        # Adds a general entity to the world, which holds the 'static' components
        self.world.add_entity(GeneralComponent())


class LinearCalculation(cecs.System):
    def process(self):
        # The name of the system category
        system_category_name = "linear calculation"
        # Check if a linear calculation system category is in self.world then remove it
        if self.world.has_system_category(system_category_name):
            self.world.remove_system_category(system_category_name)

        # Add system -> Initialize calculation
        self.world.add_system(InitializeCalculation(), system_category_name)

        # Add system -> update the geometries
        self.world.add_system(UpdateGeometries(), system_category_name)

        # Add system -> update the elements
        self.world.add_system(UpdateElements(), system_category_name)

        # Add system -> update the DOFs
        self.world.add_system(UpdateDOFs(), system_category_name)

        # Add system -> update the reduced DOFs
        self.world.add_system(UpdateReducedDOFs(), system_category_name)

        # Add system -> execute linear calculation (determine reduced stuff and solve the matrix equation)
        self.world.add_system(ExecuteLinearCalculation(), system_category_name)

        # TODO change this to return system_category_name and process the function outside of this system
        # Process the 'linear calculation' system category
        self.world.process_system_categories(system_category_name)
