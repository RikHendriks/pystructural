import copy

import numpy as np

from pystructural.core.math_ps import point_is_near_point
from pystructural.pre_processor.components import LineElementSortComponent
from pystructural.solver.components.geometries import Point2D, Line2D
from pystructural.solver.components.support import Support
from pystructural.solver.results import LinearAnalysisResults2D
from . import canvas_symbols
from .canvas import Canvas

__all__ = ['PostProcessor2D']


# TODO Change this class with load combinations in mind
class PostProcessor2D:
    def __init__(self, structure, result_entity_id):
        # Set the structure variable
        self.structure = structure
        # Initialize the linear analysis results for the given analysis system id
        self.linear_analysis_results = LinearAnalysisResults2D(self.structure, result_entity_id)
        # Get the line element sort component
        self.line_element_sort = self.structure.get_component_from_entity(self.structure.general_entity_id,
                                                                          LineElementSortComponent)
        # Initialize a canvas instance
        self.canvas = Canvas()

    def draw_structure(self, color='black'):
        for _, line in self.structure.get_component(Line2D):
            self.canvas.draw_line(line.point_list[0], line.point_list[1], color)

    def draw_supports(self, scale=1.0, color='black'):
        # For every support in the structure
        for entity_id, support in self.structure.get_component(Support):
            # Get the coordinates of the support
            coordinate = self.structure.get_component_from_entity(entity_id, Point2D).point_list[0]
            # Set the offset boolean
            offset = False
            # Rotation block symbol
            if support.rotation_z is False:
                self.canvas.draw_symbol(canvas_symbols.get_rotation_block_symbol(), scale, coordinate, color)
                offset = True
            # Rotation spring symbol
            # TODO add the rotation spring symbol
            """
            elif support.rotation_spring_z is not None:
                self.canvas.draw_symbol(canvas_symbols.get_rotation_spring_symbol(), scale, coordinate, color)
                offset = True
            """
            # Displacement block symbol
            if support.displacement_x is False and support.displacement_y is False:
                if offset is True:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_block(), scale,
                                            coordinate + scale * np.array([0.0, -0.5]), color)
                else:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_block(), scale, coordinate, color)
            # Displacement free x symbol
            elif support.displacement_y is False:
                if offset is True:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_free_x(), scale,
                                            coordinate + scale * np.array([0.0, -0.5]), color)
                else:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_free_x(), scale, coordinate, color)
                # Spring x symbol
                # TODO add the spring x symbol here
            # Displacement free y symbol
            elif support.displacement_x is False:
                if offset is True:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_free_y(), scale,
                                            coordinate + scale * np.array([0.0, -0.5]), color)
                else:
                    self.canvas.draw_symbol(canvas_symbols.get_displacement_free_y(), scale, coordinate, color)
                # Spring y symbol
                # TODO add the spring y symbol here

    # TODO place the general draw function outside of the following three functions
    def draw_displacements(self, load_combination, scale=1.0, decimal_rounding=2, color='blue'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator(self.structure.phase_id_filter):
            # Point of interest detector class instance
            poid = PointOfInterestDetector()
            # Initialize the variable for the previous position vector
            previous_position_vector = None
            previous_position_value_vector = None
            # For every line in the group of line elements
            for position_vector, displacement_vector in \
                    self.linear_analysis_results.displacement_generator(group_id, load_combination):
                # Scale the displacement vector
                displacement_vector *= scale
                # Draw the line of the displacement vector
                if previous_position_value_vector is not None:
                    self.canvas.draw_line(previous_position_value_vector, position_vector + displacement_vector, color)
                else:
                    # Draw the line from zero
                    self.canvas.draw_line(position_vector, position_vector + displacement_vector, color)
                # Add the value to the point of interest detector
                poid.add_value(position_vector, position_vector + displacement_vector,
                               np.linalg.norm(displacement_vector) / scale)
                # Set the previous position dof position
                previous_position_vector = copy.deepcopy(position_vector)
                # Set the previous position vector
                previous_position_value_vector = copy.deepcopy(position_vector + displacement_vector)
            # Draw the last line
            self.canvas.draw_line(previous_position_value_vector, previous_position_vector, color)
            # Plot the point of interests
            poi = poid.get_points_of_interest()
            for _, text_position, value in poi:
                self.canvas.draw_text(text_position, str(round(value, decimal_rounding)))

    # TODO change this to local dof generator
    def draw_dof(self, dof, load_combination, scale=1.0, decimal_rounding=2, color='red'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator(self.structure.phase_id_filter):
            # Point of interest detector class instance
            poid = PointOfInterestDetector()
            # Get the tangent vector for the group of line elements
            tangent_vector = self.linear_analysis_results.group_tangent_vector(group_id)
            # Initialize the variable for the previous dof value
            previous_dof_vector = None
            previous_dof_value_vector = None
            for position_vector, dof_value in self.linear_analysis_results.global_dof_generator(group_id,
                                                                                                load_combination):
                # Scale the dof value
                dof_value = dof_value[dof] * scale
                # Draw the line of the dof value
                if previous_dof_value_vector is not None:
                    # Draw the line
                    self.canvas.draw_line(previous_dof_value_vector, position_vector + tangent_vector * dof_value,
                                          color)
                else:
                    # Draw the line from zero
                    self.canvas.draw_line(position_vector, position_vector + tangent_vector * dof_value, color)
                # Add the value to the point of interest detector
                poid.add_value(position_vector, position_vector + tangent_vector * dof_value, dof_value / scale)
                # Set the previous position dof position
                previous_dof_vector = copy.deepcopy(position_vector)
                # Set the previous position dof value position
                previous_dof_value_vector = copy.deepcopy(position_vector + tangent_vector * dof_value)
            # Draw the last line
            self.canvas.draw_line(previous_dof_value_vector, previous_dof_vector, color)
            # Plot the point of interests
            poi = poid.get_points_of_interest()
            for _, text_position, value in poi:
                self.canvas.draw_text(text_position, str(round(value, decimal_rounding)))

    def draw_dof_enveloping(self, dof, load_combinations, scale=1.0, decimal_rounding=2, color_min='red',
                            color_max='blue'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator():
            # Point of interest detector class instance for the min and the max values
            poid_min = PointOfInterestDetector()
            poid_max = PointOfInterestDetector()
            # Get the tangent vector for the group of line elements
            tangent_vector = self.linear_analysis_results.group_tangent_vector(group_id)
            # Initialize the variable for the previous dof value
            previous_dof_vector = None
            previous_dof_value_vector_min = None
            previous_dof_value_vector_max = None
            for position_vector, dof_value_list, _ in \
                    self.linear_analysis_results.global_dof_enveloping_generator(group_id):
                # Create new dof value list based on which dofs load combinations are used in the enveloping drawing
                # TODO read above ^^
                # Scale the dof value
                dof_value_min = scale * min(0, *[dof_value[dof] for dof_value in dof_value_list])
                dof_value_max = scale * max(0, *[dof_value[dof] for dof_value in dof_value_list])
                # Draw the line of the dof value min
                if previous_dof_value_vector_min is not None:
                    # Draw the line
                    self.canvas.draw_line(previous_dof_value_vector_min, position_vector + tangent_vector *
                                          dof_value_min, color_min)
                else:
                    # Draw the line from zero
                    self.canvas.draw_line(position_vector, position_vector + tangent_vector * dof_value_min, color_min)
                # Draw the line of the dof value max
                if previous_dof_value_vector_max is not None:
                    # Draw the line
                    self.canvas.draw_line(previous_dof_value_vector_max, position_vector + tangent_vector *
                                          dof_value_max, color_max)
                else:
                    # Draw the line from zero
                    self.canvas.draw_line(position_vector, position_vector + tangent_vector * dof_value_max,
                                          color_max)
                # Add the value to the point of interest detector
                poid_min.add_value(position_vector, position_vector + tangent_vector * dof_value_min, dof_value_min /
                                   scale)
                poid_max.add_value(position_vector, position_vector + tangent_vector * dof_value_max, dof_value_max /
                                   scale)
                # Set the previous position dof position
                previous_dof_vector = copy.deepcopy(position_vector)
                # Set the previous position dof value position
                previous_dof_value_vector_min = copy.deepcopy(position_vector + tangent_vector * dof_value_min)
                previous_dof_value_vector_max = copy.deepcopy(position_vector + tangent_vector * dof_value_max)
            # Draw the last line
            self.canvas.draw_line(previous_dof_value_vector_min, previous_dof_vector, color_min)
            self.canvas.draw_line(previous_dof_value_vector_max, previous_dof_vector, color_max)
            # Plot the point of interests
            poi = poid_min.get_points_of_interest()
            for _, text_position, value in poi:
                self.canvas.draw_text(text_position, str(round(value, decimal_rounding)))
            poi = poid_max.get_points_of_interest()
            for _, text_position, value in poi:
                self.canvas.draw_text(text_position, str(round(value, decimal_rounding)))

    def draw_structure_results(self, load_combination, draw_displacements=False, draw_shear_force=False,
                               draw_normal_force=False, draw_torque=False,
                               displacement_scale=1.0, dof_scale=1.0, decimal_rounding=2):
        if draw_displacements:
            self.draw_displacements(load_combination, displacement_scale, decimal_rounding, 'purple')
        if draw_normal_force:
            self.draw_dof(0, load_combination, dof_scale, decimal_rounding, 'blue')
        if draw_shear_force:
            self.draw_dof(1, load_combination, dof_scale, decimal_rounding, 'green')
        if draw_torque:
            self.draw_dof(2, load_combination, dof_scale, decimal_rounding, 'red')

    def clear_canvas(self):
        # Clear the canvas
        self.canvas.clear()

    def show_structure(self, plot_window=None):
        # Show the structure with matplotlib
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)

    def save_as_png(self, path, plot_window=None):
        # Save the structure as an png
        self.canvas.show_matplotlib(filename=path + '.png', plot_window=plot_window, show_plot=False)

    def save_as_svg(self, path):
        # Save the structure as an svg
        self.canvas.save_as_svg(path + '.svg')

    def min_max_load_combinations_generator(self, dof, coordinates):
        # For each group
        for group_id in self.line_element_sort.group_id_generator():
            # For each combined line value
            for position_vector, dof_value_list, load_combination_list in \
                    self.linear_analysis_results.global_dof_enveloping_generator(group_id):
                # Check if their is a coordinate on the given position vector
                norms = map(lambda x: point_is_near_point(position_vector, x), coordinates)
                if True in norms:
                    # Determine the dof value list of the correct dof
                    dof_value_list = [dof_value[dof] for dof_value in dof_value_list]
                    # Yield the min and max value at the position True is min False is max
                    # Yield min
                    index_min = dof_value_list.index(min(dof_value_list))
                    yield min(dof_value_list), load_combination_list[index_min], position_vector, True
                    # Yield max
                    index_max = dof_value_list.index(max(dof_value_list))
                    yield max(dof_value_list), load_combination_list[index_max], position_vector, False


class PointOfInterestDetector:
    def __init__(self, error=0.001, slope_error=0.001):
        self.values = None
        self.error = error
        self.slope_error = slope_error

    def add_value(self, position, text_position, value):
        if self.values is not None:
            for p, _, v in self.values:
                if np.linalg.norm(p - position) < self.error:
                    break
            else:
                self.values.append([position, text_position, value])
        else:
            self.values = [[position, text_position, value]]

    def get_points_of_interest(self):
        points_of_interest = []
        previous_slope = None
        for i in range(0, len(self.values)):
            if i == 0 or i == len(self.values) - 1:
                points_of_interest.append(self.values[i])
            else:
                length = np.linalg.norm(self.values[i][0] - self.values[i - 1][0])
                slope = (self.values[i][2] - self.values[i - 1][2]) / length
                if previous_slope is not None and (slope > 0.0 > previous_slope or slope < 0.0 < previous_slope)\
                        and abs(slope - previous_slope) > self.slope_error:
                    points_of_interest.append(self.values[i - 1])
                previous_slope = copy.deepcopy(slope)
        return points_of_interest
