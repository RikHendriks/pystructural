import catecs

from pystructural.solver.results.result_components.result_components import ResultComponent
from .geometry_systems import UpdateGeometries
from .element_systems import UpdateElements
from .dof_systems import UpdateDOFs, UpdateReducedDOFs
from .load_systems import UpdateLoads
from .stiffness_systems import ExecuteLinearCalculation

__all__ = ['AnalysisSystem', 'LinearAnalysis']


class AnalysisSystem(catecs.System):
    def __init__(self, name):
        self.name = name
        self.result_entity_id = None
        super().__init__()

    def initialize(self):
        # Adds a general entity to the world, which holds the result components
        self.result_entity_id = self.world.add_entity(ResultComponent(self.name))


class LinearAnalysis(AnalysisSystem):
    def process(self):
        # Check if a linear calculation system category is in self.world then remove it
        if self.world.has_system_category(self.name):
            self.world.remove_system_category(self.name)

        # Add system -> update the geometries
        self.world.add_system(UpdateGeometries(), self.name)

        # Add system -> update the elements
        self.world.add_system(UpdateElements(), self.name)

        # Add system -> update the DOFs
        self.world.add_system(UpdateDOFs(), self.name)

        # Add system -> update the reduced DOFs
        self.world.add_system(UpdateReducedDOFs(), self.name)

        # Add system -> update the loads
        self.world.add_system(UpdateLoads(), self.name)

        # Add system -> execute linear calculation (determine reduced stuff and solve the matrix equation)
        self.world.add_system(ExecuteLinearCalculation(), self.name)

        # TODO change this to return system_category_name and process the function outside of this system
        # Process the 'linear calculation' system category
        self.world.process_system_categories(self.name)
