import numpy as np
import copy

from .canvas import Canvas

from pystructural.solver.components.geometries import Line2D
from pystructural.pre_processor.components import LineElementSortComponent

from pystructural.solver.results import LinearAnalysisResults2D

__all__ = ['PostProcessor']


# TODO change this to a 2D processor
class PostProcessor:
    def __init__(self, structure, analysis_system):
        # Set the structure variable
        self.structure = structure
        # Initialize the linear analysis results for the given analysis system id
        self.linear_analysis_results = LinearAnalysisResults2D(self.structure, analysis_system)
        # Get the line element sort component
        self.line_element_sort = self.structure.get_component_from_entity(self.structure.general_entity_id,
                                                                          LineElementSortComponent)
        # Initialize a canvas instance
        self.canvas = Canvas()

    def draw_structure(self, color='black'):
        for _, line in self.structure.get_component(Line2D):
            self.canvas.draw_line(line.point_list[0], line.point_list[1], color)

    def draw_displacements(self, scale=1.0, decimal_rounding=2, color='blue'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator():
            # Point of interest detector class instance
            poid = PointOfInterestDetector()
            # Initialize the variable for the previous position vector
            previous_position_vector = None
            previous_position_value_vector = None
            # For every line in the group of line elements
            for position_vector, displacement_vector in self.linear_analysis_results.displacement_generator(group_id):
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
    def draw_dof(self, dof, scale=1.0, decimal_rounding=2, color='red'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator():
            # Point of interest detector class instance
            poid = PointOfInterestDetector()
            # Get the tangent vector for the group of line elements
            tangent_vector = self.linear_analysis_results.group_tangent_vector(group_id)
            # Initialize the variable for the previous dof value
            previous_dof_vector = None
            previous_dof_value_vector = None
            for position_vector, dof_value in self.linear_analysis_results.global_dof_generator(group_id, dof):
                # Scale the dof value
                dof_value *= scale
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

    def draw_structure_results(self, draw_displacements=False, draw_shear_force=False, draw_normal_force=False,
                               draw_torque=False, scale=1.0, decimal_rounding=2):
        if draw_displacements:
            self.draw_displacements(scale, decimal_rounding, 'purple')
        if draw_normal_force:
            self.draw_dof(0, scale, decimal_rounding, 'blue')
        if draw_shear_force:
            self.draw_dof(1, scale, decimal_rounding, 'green')
        if draw_torque:
            self.draw_dof(2, scale, decimal_rounding, 'red')

    def show_structure(self, plot_window):
        # Show the structure with matplotlib
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)

    def save_as_svg(self, path):
        # Save the structure as an svg
        self.canvas.save_as_svg(path + '.svg')


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
