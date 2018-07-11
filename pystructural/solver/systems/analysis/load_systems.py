import catecs

from pystructural.solver.components.loads import QLoad2D, PointLoad2D, ImposedLoad2D

__all__ = ['load_subclasses_2d', 'UpdateLoads']


# List of all the load subclasses
load_subclasses_2d = [QLoad2D, PointLoad2D, ImposedLoad2D]
imposed_load_subclasses_2d = [ImposedLoad2D]


class UpdateLoads(catecs.System):
    def process(self):
        # Process all the 2d loads
        for load_class in load_subclasses_2d:
            for entity, components in self.world.get_components(load_class.compatible_geometry, load_class):

                # Determine the geometry of the element
                components[1].geometry = components[0]
