import copy

from .canvas import Canvas

from pystructural.solver.components.additional_components.calculation_components import *

from pystructural.solver.components.geometries import line_elements, Line2D, Point2D
from pystructural.pre_processor.components import LineElementSortComponent

from pystructural.solver.results import LinearAnalysisResults

__all__ = ['PostProcessor']


# TODO change this to a 2D processor
# TODO put the code from the draw displacement in the linear analysis results component
class PostProcessor:
    def __init__(self, structure, analysis_system):
        # Set the structure variable
        self.structure = structure
        # Set the analysis system and get the dof and linear calculation components of the analysis
        self.analysis_system = analysis_system
        self.dof_calculation_component = self.structure.get_component_from_entity(self.analysis_system.result_entity_id,
                                                                                  DOFCalculationComponent)
        self.linear_calculation_component = self.structure.get_component_from_entity(
            self.analysis_system.result_entity_id, LinearCalculationComponent)
        # Initialize the linear analysis results for the given analysis system id
        self.linear_analysis_results = LinearAnalysisResults(self.structure, self.analysis_system)
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
            for node_tuple in self.line_element_sort.line_element_id_generator(group_id):
                # Get the corresponding element of the line
                element = None
                for line_element_class in line_elements:
                    if self.structure.get_component_from_entity(node_tuple[0], line_element_class):
                        element = self.structure.get_component_from_entity(node_tuple[0], line_element_class)
                        break
                # Get the displacement vector of the element
                displacement_vector = self.linear_analysis_results.get_element_displacement_vector(element)
                # Get the first or last three items depending on if the node is the first or the second node in the line
                if node_tuple[2] == 0:
                    displacement_vector = displacement_vector[:3]
                else:
                    displacement_vector = displacement_vector[-3:]
                # Scale the displacement vector
                displacement_vector = scale * displacement_vector[:2]
                # Get the position of the node
                position_vector = self.structure.get_component_from_entity(node_tuple[1], Point2D).point_list[0]
                # Draw the line of the displacement vector
                if previous_position_vector is not None:
                    self.canvas.draw_line(previous_position_vector, position_vector + displacement_vector, color)
                # Set the previous position vector
                previous_position_vector = copy.deepcopy(position_vector + displacement_vector)

    def draw_dof(self, dof, color='red'):
        pass

    def show_structure(self, plot_window, draw_displacements=False, scale=1.0):
        self.draw_structure()
        if draw_displacements:
            self.draw_displacements(scale)
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)
