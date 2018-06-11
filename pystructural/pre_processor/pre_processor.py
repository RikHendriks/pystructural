import catecs

from .systems import SplitLine, LineElementSort

__all__ = ['PreProcessor2D']


class PreProcessor2D(catecs.System):
    def process(self):
        # Run system instance: split line
        self.world.run_system(SplitLine())
        # Run system instance: line element sort
        self.world.run_system(LineElementSort())
