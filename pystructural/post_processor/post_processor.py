from .canvas import Canvas

from ..solver.components.geometries import Line2D

__all__ = ['PostProcessor']


class PostProcessor:
    def __init__(self, structure, analysis_system):
        self.structure = structure
        self.canvas = Canvas()
        self.linear_analysis_results = analysis_system

    def draw_structure(self, color='black'):
        for _, line in self.structure.get_component(Line2D):
            self.canvas.draw_line(line.point_list[0], line.point_list[1], color)

    def show_structure(self, plot_window):
        self.draw_structure()
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)
