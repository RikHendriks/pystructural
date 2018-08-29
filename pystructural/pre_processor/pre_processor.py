import catecs

from .systems import CheckOverlappingNodes2D, AddSplitNodes2D, SplitLine2D, LineElementSort2D, PreProcessorDofSystems

__all__ = ['PreProcessor2D']


class PreProcessor2D(catecs.System):
    def __init__(self, minimum_node_distance=0.001, minimum_element_distance=0.1):
        # Initialize the system
        super().__init__()
        # Initialize the variables of the pre processor
        self.minimum_node_distance = minimum_node_distance
        self.minimum_element_distance = minimum_element_distance

    def process(self):
        # Run system instance: check overlapping nodes 2d
        self.world.run_system(CheckOverlappingNodes2D(self.minimum_node_distance))
        # Run system instance: split line 2d
        self.world.run_system(SplitLine2D())
        # Run system instance: add split nodes 2d
        self.world.run_system(AddSplitNodes2D(self.minimum_element_distance))
        # Run system instance: split line 2d
        self.world.run_system(SplitLine2D())
        # Run system instance: line element sort 2d
        self.world.run_system(LineElementSort2D())
        # Run system instance: pre processor dof systems
        self.world.run_system(PreProcessorDofSystems())
