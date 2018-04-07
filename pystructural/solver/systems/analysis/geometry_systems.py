import numpy as np
import catecs

from pystructural.solver.components.geometries import Point2D, Line2D, Triangle2D

__all__ = ['geometry_subclasses_2d', 'UpdateGeometries']


# List of geometries subclasses
geometry_subclasses_2d = [Point2D, Line2D, Triangle2D]


class UpdateGeometries(catecs.System):
    def process(self):
        # Process all the 2d geometries subclasses
        for geometry_class in geometry_subclasses_2d:
            for entity, component in self.world.get_component(geometry_class):

                # Compute the point lists of the geometries
                if geometry_class is Point2D:
                    component.point_id_list = [entity]
                else:
                    point_list = []
                    for point_id in component.point_id_list:
                        point_list.append(self.world.get_component_from_entity(point_id, Point2D).point_list[0])
                    # Set the point list for the geometries subclass component
                    component.point_list = np.array(point_list)

                # Compute the area's of the geometries
                component.compute_area()
