from .point import *
from .line import *
from .triangle import *

# TODO change the following lines
from pystructural.solver.components.elements.frame_element_2d import FrameElement2D
from pystructural.solver.components.elements.linear_triangle_element_2d import LinearTriangleElement2D

line_elements = [FrameElement2D]
triangle_elements = [LinearTriangleElement2D]
