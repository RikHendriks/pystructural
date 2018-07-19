import copy

import catecs

from pystructural.solver.results.result_components.result_components import ResultComponent
from .geometry_systems import UpdateGeometries
from .element_systems import UpdateElements
from .dof_systems import UpdateDOFs, UpdateReducedDOFs
from .load_systems import UpdateLoads
from .stiffness_systems import ExecuteLinearCalculation

__all__ = ['LinearAnalysisSystem', 'LinearPhaseAnalysisSystem']


class AnalysisSystem(catecs.System):
    def __init__(self, name, load_combinations):
        self.name = name
        self.result_entity_id = None
        self.load_combinations = load_combinations
        super().__init__()

    def initialize(self):
        # Adds a general entity to the world, which holds the result components
        self.result_entity_id = self.world.add_entity(ResultComponent(self.name))


class LinearAnalysisSystem(AnalysisSystem):
    def process(self):
        # Check if a linear calculation system category is in self.world then remove it
        if self.world.has_system_category(self.name):
            self.world.remove_system_category(self.name)

        # Add system -> update the geometries
        self.world.add_system(UpdateGeometries(), self.name)

        # Add system -> update the elements
        self.world.add_system(UpdateElements(), self.name)

        # Add system -> update the DOFs
        self.world.add_system(UpdateDOFs(self.result_entity_id), self.name)

        # Add system -> update the reduced DOFs
        self.world.add_system(UpdateReducedDOFs(self.result_entity_id), self.name)

        # Add system -> update the loads
        self.world.add_system(UpdateLoads(), self.name)

        # Add system -> execute linear calculation (determine reduced stuff and solve the matrix equation)
        self.world.add_system(ExecuteLinearCalculation(self.result_entity_id, self.load_combinations), self.name)

        # Process the 'linear calculation' system category
        self.world.process_system_categories(self.name, ordered=True)


class LinearPhaseAnalysisSystem(AnalysisSystem):
    def __init__(self, name, load_combinations, phased_analysis):
        self.phased_analysis = phased_analysis
        super().__init__(name, load_combinations)

    def process(self):
        # List of linear analysis results
        lar_list = {}
        # Previous phase id
        prev_phase_id = None
        # For every phase
        for phase_id in self.phased_analysis.phase_generator():
            # Get the structure with only the current phase
            self.world.phase_id_filter = phase_id
            self.world.phase_id_adder_list = [phase_id]
            # Solve the linear system for the structure
            if phase_id != 2:
                lar_list[phase_id] = self.world.solve_linear_system(str(self.phased_analysis.phases[phase_id]), False)
            else:
                lar_list[phase_id] = self.world.solve_linear_system(str(self.phased_analysis.phases[phase_id]), False,
                                                                    [lar_list[0], lar_list[1]])
            # Combine the phase results
            self.world.show_structure()
            # Set the previous phase id
            prev_phase_id = copy.deepcopy(phase_id)
