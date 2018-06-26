import catecs

from .systems import AddSplitNodes, SplitLine, LineElementSort

__all__ = ['PreProcessor2D']


class PreProcessor2D(catecs.System):
    def __init__(self, minimum_element_distance=0.1):
        # Initialize the system
        super().__init__()
        # Initialize the variables of the pre processor
        self.minimum_element_distance = minimum_element_distance

    def process(self):
        # Run system instance: split line
        self.world.run_system(SplitLine())
        # Run system instance: add split nodes
        self.world.run_system(AddSplitNodes(self.minimum_element_distance))
        # Run system instance: split line
        self.world.run_system(SplitLine())
        # Run system instance: line element sort
        self.world.run_system(LineElementSort())
