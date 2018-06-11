from .canvas import Canvas

from pystructural.solver.components.geometries import Line2D
from pystructural.pre_processor.components import LineElementSortComponent

from pystructural.solver.results import LinearAnalysisResults

__all__ = ['PostProcessor']


class PostProcessor:
    def __init__(self, structure, analysis_system):
        # Set the structure variable
        self.structure = structure
        # Initialize the linear analysis results for the given analysis system id
        self.linear_analysis_results = LinearAnalysisResults(self.structure, analysis_system)
        # Get the line element sort component
        self.line_element_sort_component = self.structure.get_component_from_entity(self.structure.general_entity_id,
                                                                                    LineElementSortComponent)
        # Initialize a canvas instance
        self.canvas = Canvas()

    def draw_structure(self, color='black'):
        for _, line in self.structure.get_component(Line2D):
            self.canvas.draw_line(line.point_list[0], line.point_list[1], color)

    def show_structure(self, plot_window):
        self.draw_structure()
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)
