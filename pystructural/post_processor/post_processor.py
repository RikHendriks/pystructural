import catecs

from .canvas import Canvas

from .components.post_processor_components import LineElementSortComponent
from .systems.line_element_sort_systems import LineElementSort

from ..solver.components.geometries import Line2D

__all__ = ['PostProcessor']


class PostProcessor(catecs.World):
    def __init__(self, structure):
        super().__init__()
        self.structure = structure
        self.canvas = Canvas()
        # Initialize the general entity for all the static components of the structure
        self.general_entity_id = self.add_entity()
        # Process the initialization systems
        self._process_initialization_systems()

    def draw_structure(self, color='black'):
        for _, line in self.structure.get_component(Line2D):
            self.canvas.draw_line(line.point_list[0], line.point_list[1], color)

    def show_structure(self, plot_window):
        self.draw_structure()
        self.canvas.show_matplotlib(plot_window=plot_window, show_plot=True)

    def _process_initialization_systems(self):
        # Add a line element sort system and run it
        les_id = self.add_system(LineElementSort())
        # Process the preprocessor system
        self.process_systems(les_id)
        # Remove the preprocessor system
        self.remove_system(les_id)
