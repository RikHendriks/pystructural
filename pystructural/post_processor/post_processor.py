import copy

from .canvas import Canvas

from pystructural.solver.components.geometries import Line2D
from pystructural.pre_processor.components import LineElementSortComponent

from pystructural.solver.results import LinearAnalysisResults2D

__all__ = ['PostProcessor']


# TODO change this to a 2D processor
# TODO put the code from the draw displacement in the linear analysis results component
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

    def draw_displacements(self, scale=1.0, color='blue'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator():
            # Initialize the variable for the previous position vector
            previous_position_vector = None
            # For every line in the group of line elements
            for position_vector, displacement_vector in self.linear_analysis_results.displacement_generator(group_id):
                # Scale the displacement vector
                displacement_vector *= scale
                # Draw the line of the displacement vector
                if previous_position_vector is not None:
                    self.canvas.draw_line(previous_position_vector, position_vector + displacement_vector, color)
                # Set the previous position vector
                previous_position_vector = copy.deepcopy(position_vector + displacement_vector)

    # TODO change this to local dof generator
    def draw_dof(self, dof, scale=1.0, color='red'):
        # For every group of line elements
        for group_id in self.line_element_sort.group_id_generator():
            # Get the tangent vector for the group of line elements
            tangent_vector = self.linear_analysis_results.group_tangent_vector(group_id)
            # Initialize the variable for the previous dof value
            previous_dof_value_position = None
            for position_vector, dof_value in self.linear_analysis_results.global_dof_generator(group_id, dof):
                # Scale the dof value
                dof_value *= scale
                # Draw the line of the dof value
                if previous_dof_value_position is not None:
                    # Draw the line
                    self.canvas.draw_line(previous_dof_value_position, position_vector + tangent_vector * dof_value,
                                          color)
                # Set the previous position dof value position
                previous_dof_value_position = copy.deepcopy(position_vector + tangent_vector * dof_value)

    def show_structure(self, plot_window, draw_displacements=False, draw_shear_force=False, draw_normal_force=False,
                       draw_torque=False, scale=1.0):
        self.draw_structure()
        if draw_displacements:
            self.draw_displacements(scale, 'purple')
        if draw_normal_force:
            self.draw_dof(0, scale, 'blue')
        if draw_shear_force:
            self.draw_dof(1, scale, 'green')
        if draw_torque:
            self.draw_dof(2, scale, 'red')
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)
