import catecs

from pystructural.solver.components.loads import PointLoad2D

__all__ = ['UpdateLoads']


# List of all the load subclasses
load_subclasses_2d = [PointLoad2D]


class UpdateLoads(catecs.System):
    def process(self):
        # Process all the 2d loads
        for load_class in load_subclasses_2d:
            for entity, components in self.world.get_components(load_class.compatible_geometry, load_class):

                # Determine the geometry of the element
                components[1].geometry = components[0]
