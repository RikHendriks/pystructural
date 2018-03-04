import cecs

from .geometry_systems import UpdateGeometries

__all__ = ['LinearCalculation']


class LinearCalculation(cecs.System):
    def process(self):
        # Check if a linear calculation system category is in self.world then remove it
        if self.world.has_system_category("linear calculation"):
            self.world.remove_system_category("linear calculation")

        # Add system -> update geometries
        self.world.add_system(UpdateGeometries(), "linear calculation")

        # Process the 'linear calculation' system category
        self.world.process_system_categories("linear calculation")