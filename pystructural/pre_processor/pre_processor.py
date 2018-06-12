import catecs

from .systems import AddSplitNodes, SplitLine, LineElementSort

__all__ = ['PreProcessor2D']


class PreProcessor2D(catecs.System):
    def process(self):
        # Run system instance: add split nodes
        self.world.run_system(AddSplitNodes(0.1))
        # Run system instance: split line
        self.world.run_system(SplitLine())
        # Run system instance: line element sort
        self.world.run_system(LineElementSort())
