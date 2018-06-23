import numpy as np

import matplotlib.pyplot as plt
import svgpathtools as svg


class Canvas:
    def __init__(self):
        self.lines = []
        self.texts = []

    def draw_line(self, start, end, color='black'):
        self.lines.append([np.array([start, end]), color])

    def draw_text(self, coordinate, text, font_size=12, color='black'):
        self.texts.append([coordinate, text, font_size, color])

    def show_matplotlib(self, filename=None, plot_window=None, show_plot=False):
        # Plot each line to matplotlib
        for line in self.lines:
            plt.plot([line[0][0][0], line[0][1][0]], [line[0][0][1], line[0][1][1]], line[1])
        # Plot each text to matplotlib
        for text in self.texts:
            plt.text(text[0][0], text[0][1], text[1], fontsize=text[2], color=text[3])
        # Redefine the axis of the plot
        plt.axis(plot_window)
        # Save the plotted file
        if filename is not None:
            plt.savefig(filename)
        # Show the plot
        if show_plot:
            plt.show()

    # TODO change this to matplotlib and remove the dependencies to svgpathtools
    def save_as_svg(self, filename):
        lines = [svg.Line(start[0] + start[1] * -1j, end[0] + end[1] * -1j) for [start, end], _ in self.lines]
        line_colors = [color for [_, _], color in self.lines]
        text_path = [svg.Line(coordinate[0] + coordinate[1] * -1j, coordinate[0] + 1.0 + coordinate[1] * -1j) for
                     coordinate, _, _, _ in self.texts]
        text = [text for _, text, _, _ in self.texts]
        svg.wsvg(lines, line_colors, stroke_widths=[0.01] * len(lines),
                 text=text, text_path=text_path, font_size=[0.1] * len(text),
                 filename=filename)
