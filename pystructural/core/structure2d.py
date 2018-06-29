import numpy as np
import catecs

from ..solver.components import element_geometries, elements, geometries, connections, loads, materials, support,\
    additional_components

from ..solver.components.load_combination import LoadCombinationsComponent
from ..solver.systems import LinearAnalysis

from pystructural.pre_processor.pre_processor import PreProcessor2D

from pystructural.post_processor.post_processor import PostProcessor2D

__all__ = ['Structure2D']


class Structure2D(catecs.World):
    def __init__(self, minimum_element_distance=0.1):
        # Initialize the world
        super().__init__()
        # Initialize the general entity for all the static components of the structure
        self.general_entity_id = self.add_entity(additional_components.GroupComponent())
        # Get the group component
        self.group_component = self.get_component_from_entity(self.general_entity_id,
                                                              additional_components.GroupComponent)
        # Get the load combinations component
        self.load_combinations_component = self.add_component(self.general_entity_id, LoadCombinationsComponent())
        # Initialize the id of the linear system
        self.linear_analysis_system_id = None
        # Initialize the post processor
        self.post_processor = None
        # Initialize the variables of the structure
        self.minimum_element_distance = minimum_element_distance

    def search_for_point(self, coordinate, error=0.001):
        for entity, point in self.get_component(geometries.Point2D):
            if np.linalg.norm(coordinate - point.point_list[0]) < error:
                return entity, point
        else:
            return None

    def position_to_id(self, coordinate):
        if isinstance(coordinate, list):
            tuple = self.search_for_point(coordinate)
            if tuple is None:
                return tuple
            else:
                return tuple[0]
        else:
            return coordinate

    def add_node(self, position):
        return self.add_entity(geometries.Point2D(position[0], position[1]))

    def add_component_at_coordinate(self, coordinate, component_instance, unique=True):
        # Determine the entity based on the position
        entity_id = self.position_to_id(coordinate)
        if entity_id is None:
            entity_id = self.add_node(coordinate)

        # Add the component to the entity
        self.add_component_at_entity(entity_id, component_instance, unique)

    def add_component_at_entity(self, entity_id, component_instance, unique=True):
        # If there is a component with the type in the entity
        if self.has_component(entity_id, type(component_instance)) and unique:
            self.get_component_from_entity(entity_id, type(component_instance)) + component_instance
        else:
            self.add_component(entity_id, component_instance)

    def add_frame_element(self, start_coordinate, end_coordinate, youngs_modulus, mass_density, cross_section_area,
                          moment_of_inertia):
        entity_start_id = self.position_to_id(start_coordinate)
        entity_end_id = self.position_to_id(end_coordinate)

        if entity_start_id is None:
            entity_start_id = self.add_node(start_coordinate)

        if entity_end_id is None:
            entity_end_id = self.add_node(end_coordinate)

        # Create the frame element entity
        frame_element_id = self.add_entity(geometries.Line2D(entity_start_id, entity_end_id),
                                           elements.FrameElement2D(),
                                           materials.LinearElasticity2DMaterial(youngs_modulus, mass_density),
                                           element_geometries.BeamElementGeometry(cross_section_area,
                                                                                  moment_of_inertia))

        # Create the group for the frame element entity
        group_id = self.group_component.create_group()
        self.group_component.add_entity_to_group(frame_element_id, group_id)

        # Return the frame element entity id
        return frame_element_id

    def add_support(self, coordinate, displacement_x=True, displacement_y=True, rotation_z=True):
        # Create the support component
        support_component = support.Support(displacement_x=displacement_x, displacement_y=displacement_y,
                                            rotation_z=rotation_z)
        # Add the component to the position
        self.add_component_at_coordinate(coordinate, support_component)

    def add_spring(self, coordinate, spring_x=None, spring_y=None, rotation_spring_z=None):
        # Create the spring component
        spring_component = connections.Spring(spring_x=spring_x, spring_y=spring_y, rotation_spring_z=rotation_spring_z)
        # Add the component to the position
        self.add_component_at_coordinate(coordinate, spring_component)

    def add_load_combination(self, load_combination_name, load_cases):
        # Add a new load combination to the
        self.load_combinations_component.add_load_combination(load_combination_name, load_cases, True)

    def add_point_load(self, coordinate, point_load, load_case=None):
        # Create the spring component
        lc_id = self.load_combinations_component.add_load_case(load_case)
        point_load_component = loads.PointLoad2D(point_load, lc_id)
        # Add the component to the position
        self.add_component_at_coordinate(coordinate, point_load_component, unique=False)

    def add_global_q_load(self, entity_id, q_load, load_case=None):
        def q_load_func(x):
            return q_load
        self.add_global_q_load_func(entity_id, q_load_func, load_case)

    def add_global_q_load_func(self, entity_id, q_load_func, load_case=None):
        if entity_id in self.entities:
            lc_id = self.load_combinations_component.add_load_case(load_case)
            self.add_component_at_entity(entity_id, loads.QLoad2D(q_load_func, lc_id), unique=False)

    def solve_linear_system(self):
        # If there is no load combination defined
        if len(self.load_combinations_component.load_combinations) is 0:
            # Add the generic load combination
            self.load_combinations_component.add_generic_load_combination()

        # Run the system: preprocessor 2D
        self.run_system(PreProcessor2D(self.minimum_element_distance))
        # Add linear calculation system and solve
        self.linear_analysis_system_id =\
            self.add_system(LinearAnalysis("linear_calculation",
                                           list(self.load_combinations_component.load_combinations.keys())))
        # Process linear calculation system
        self.process_systems(self.linear_analysis_system_id)
        # Create an instance of the post processor for this structure with the linear analysis
        self.post_processor = PostProcessor2D(self, self.get_system(self.linear_analysis_system_id))

    def _determine_plot_window(self):
        # Initialize the plot window
        plot_window = [0.0, 0.0, 0.0, 0.0]
        # For all the nodes in the structure
        for _, point in self.get_component(geometries.Point2D):
            # Get the coordinates of the point
            p = point.point_list[0]
            # If x of the point is smaller than min x in plot window
            if p[0] < plot_window[0]:
                plot_window[0] = p[0]
            # If x of the point is greater than max x in plot window
            if p[0] > plot_window[1]:
                plot_window[1] = p[0]
            # If y of the point is smaller than min y in plot window
            if p[1] < plot_window[2]:
                plot_window[2] = p[1]
            # If y of the point is greater than max y in plot window
            if p[1] > plot_window[3]:
                plot_window[3] = p[1]
        # Add margins to the plot window
        x_margin = max(2.0, 0.02 * (plot_window[1] - plot_window[0]))
        y_margin = max(2.0, 0.02 * (plot_window[3] - plot_window[2]))
        plot_window[0] -= x_margin
        plot_window[1] += x_margin
        plot_window[2] -= y_margin
        plot_window[3] += y_margin
        # Return the plot window
        return plot_window

    def get_point_displacement_vector(self, coordinate, load_combination='generic_load_combination'):
        # Get the entity id and the instance of the point
        entity_id, point = self.search_for_point(coordinate, error=self.minimum_element_distance+0.01)
        # If the point exists
        if point is not None:
            load_combination_id = self.load_combinations_component.load_combination_names[load_combination]
            return self.post_processor.linear_analysis_results.get_node_displacement_vector(point, load_combination_id)
        else:
            return None

    def get_point_global_force_vector(self, coordinate, load_combination='generic_load_combination'):
        # Get the entity id and the instance of the point
        entity_id, point = self.search_for_point(coordinate, error=self.minimum_element_distance + 0.01)
        # If the point exists
        if point is not None:
            load_combination_id = self.load_combinations_component.load_combination_names[load_combination]
            return self.post_processor.linear_analysis_results.get_node_global_force(point, load_combination_id)
        else:
            return None

    def show_structure(self, load_combination='generic_load_combination', plot_window=None, path_svg=None, scale=1.0):
        # Draw the structure
        self.post_processor.draw_structure()
        # Draw the supports
        self.post_processor.draw_supports(0.25)
        # Draw the structure results
        load_combination_id = self.load_combinations_component.load_combination_names[load_combination]
        self.post_processor.draw_structure_results(load_combination_id, True, True, True, True, scale)
        # Show the structure
        if plot_window is None:
            self.post_processor.show_structure(self._determine_plot_window())
        else:
            self.post_processor.show_structure(plot_window)
        # If there is a path given for the svg then save the structure as an svg
        if path_svg is not None:
            self.post_processor.save_as_svg(path_svg)
