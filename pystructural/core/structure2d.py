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
    def __init__(self):
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

    def search_for_point(self, position, error=0.001):
        for entity, point in self.get_component(geometries.Point2D):
            if np.linalg.norm(position - point.point_list[0]) < error:
                return entity
        else:
            return None

    def position_to_id(self, position):
        if isinstance(position, list):
            return self.search_for_point(position)
        else:
            return position

    def add_node(self, position):
        return self.add_entity(geometries.Point2D(position[0], position[1]))

    def add_component_at_position(self, position, component_instance, unique=True):
        # Determine the entity based on the position
        entity_id = self.position_to_id(position)
        if entity_id is None:
            entity_id = self.add_node(position)

        # Add the component to the entity
        self.add_component_at_entity(entity_id, component_instance, unique)

    def add_component_at_entity(self, entity_id, component_instance, unique=True):
        # If there is a component with the type in the entity
        if self.has_component(entity_id, type(component_instance)) and unique:
            self.get_component_from_entity(entity_id, type(component_instance)) + component_instance
        else:
            self.add_component(entity_id, component_instance)

    def add_frame_element(self, start_position, end_position, youngs_modulus, mass_density, cross_section_area,
                          moment_of_inertia):
        entity_start_id = self.position_to_id(start_position)
        entity_end_id = self.position_to_id(end_position)

        if entity_start_id is None:
            entity_start_id = self.add_node(start_position)

        if entity_end_id is None:
            entity_end_id = self.add_node(end_position)

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

    def add_support(self, position, displacement_x=True, displacement_y=True, rotation_z=True):
        # Create the support component
        support_component = support.Support(displacement_x=displacement_x, displacement_y=displacement_y,
                                            rotation_z=rotation_z)
        # Add the component to the position
        self.add_component_at_position(position, support_component)

    def add_spring(self, position, spring_x=None, spring_y=None, rotation_spring_z=None):
        # Create the spring component
        spring_component = connections.Spring(spring_x=spring_x, spring_y=spring_y, rotation_spring_z=rotation_spring_z)
        # Add the component to the position
        self.add_component_at_position(position, spring_component)

    def add_load_combination(self, load_combination_name, load_cases):
        # Add a new load combination to the
        self.load_combinations_component.add_load_combination(load_combination_name, load_cases, True)

    def add_point_load(self, position, point_load, load_case=None):
        # Create the spring component
        lc_id = self.load_combinations_component.add_load_case(load_case)
        point_load_component = loads.PointLoad2D(point_load, lc_id)
        # Add the component to the position
        self.add_component_at_position(position, point_load_component, unique=False)

    def add_global_q_load(self, entity_id, q_load, load_case=None):
        def q_load_func(x):
            return q_load
        self.add_global_q_load_func(entity_id, q_load_func, load_case)

    def add_global_q_load_func(self, entity_id, q_load_func, load_case=None):
        if entity_id in self.entities:
            lc_id = self.load_combinations_component.add_load_case(load_case)
            self.add_component_at_entity(entity_id, loads.QLoad2D(q_load_func, lc_id), unique=False)

    def solve_linear_system(self, minimum_element_distance=0.1):
        # If there is no load combination defined
        if len(self.load_combinations_component.load_combinations) is 0:
            # Add the generic load combination
            self.load_combinations_component.add_generic_load_combination()

        # Run the system: preprocessor 2D
        self.run_system(PreProcessor2D(minimum_element_distance))
        # Add linear calculation system and solve
        self.linear_analysis_system_id =\
            self.add_system(LinearAnalysis("linear_calculation",
                                           list(self.load_combinations_component.load_combinations.keys())))
        # Process linear calculation system
        self.process_systems(self.linear_analysis_system_id)

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

    def show_structure(self, load_combination='generic_load_combination', plot_window=None, path_svg=None, scale=1.0):
        # Create an instance of the post processor for this structure with the linear analysis
        pp = PostProcessor2D(self, self.get_system(self.linear_analysis_system_id))
        # Draw the structure
        pp.draw_structure()
        # Draw the supports
        pp.draw_supports(0.25)
        # Draw the structure results
        load_combination_id = self.load_combinations_component.load_combination_names[load_combination]
        pp.draw_structure_results(load_combination_id, True, True, True, True, scale)
        # Show the structure
        if plot_window is None:
            pp.show_structure(self._determine_plot_window())
        else:
            pp.show_structure(plot_window)
        # If there is a path given for the svg then save the structure as an svg
        if path_svg is not None:
            pp.save_as_svg(path_svg)
