import copy

import matplotlib.pyplot as plt
import numpy as np
import svgpathtools as svg

__all__ = ['Canvas',
           'scale_line', 'scale_lines',
           'translate_line', 'translate_lines',]


class Canvas:
    def __init__(self):
        self.lines = []
        self.texts = []
        self.plot_window = [0.0, 0.0, 0.0, 0.0]

    def expand_plot_window(self, p):
        # If x of the point is smaller than min x in plot window
        if p[0] < self.plot_window[0]:
            self.plot_window[0] = p[0]
        # If x of the point is greater than max x in plot window
        if p[0] > self.plot_window[1]:
            self.plot_window[1] = p[0]
        # If y of the point is smaller than min y in plot window
        if p[1] < self.plot_window[2]:
            self.plot_window[2] = p[1]
        # If y of the point is greater than max y in plot window
        if p[1] > self.plot_window[3]:
            self.plot_window[3] = p[1]

    def draw_line(self, start, end, color='black'):
        # If the line is (partially) outside the border then increase the borders
        self.expand_plot_window(start)
        self.expand_plot_window(end)
        # Append the line to the line list
        self.lines.append([np.array([start, end]), color])

    def draw_lines(self, lines, color='black'):
        for line in lines:
            self.draw_line(line[0], line[1], color)

    def draw_text(self, coordinate, text, font_size=12, color='black'):
        self.texts.append([coordinate, text, font_size, color])

    def draw_symbol(self, symbol, scale, translation, color='black'):
        symbol = scale_lines(symbol, scale)
        symbol = translate_lines(symbol, translation)
        self.draw_lines(symbol, color)

    def show_matplotlib(self, filename=None, plot_window=None, show_plot=False):
        # Plot each line to matplotlib
        for line in self.lines:
            plt.plot([line[0][0][0], line[0][1][0]], [line[0][0][1], line[0][1][1]], line[1])
        # Plot each text to matplotlib
        for text in self.texts:
            plt.text(text[0][0], text[0][1], text[1], fontsize=text[2], color=text[3])
        # Redefine the axis of the plot
        if plot_window is None:
            # Make a copy of the plot window
            plot_window = copy.deepcopy(self.plot_window)
            # Add margins to the plot window
            x_margin = max(1.0, 0.05 * (plot_window[1] - plot_window[0]))
            y_margin = max(1.0, 0.05 * (plot_window[3] - plot_window[2]))
            plot_window[0] -= x_margin
            plot_window[1] += x_margin
            plot_window[2] -= y_margin
            plot_window[3] += y_margin
            # Set the axis
            plt.axis(plot_window)
        else:
            # Set the axis
            plt.axis(plot_window)
        # Save the plotted file
        if filename is not None:
            plt.savefig(filename)
        # Show the plot
        if show_plot:
            plt.show()

    def save_as_svg(self, filename):
        lines = [svg.Line(start[0] + start[1] * -1j, end[0] + end[1] * -1j) for [start, end], _ in self.lines]
        line_colors = [color for [_, _], color in self.lines]
        text_path = [svg.Line(coordinate[0] + coordinate[1] * -1j, coordinate[0] + 1.0 + coordinate[1] * -1j) for
                     coordinate, _, _, _ in self.texts]
        text = [text for _, text, _, _ in self.texts]
        svg.wsvg(lines, line_colors, stroke_widths=[0.01] * len(lines),
                 text=text, text_path=text_path, font_size=[0.1] * len(text),
                 filename=filename)


def scale_line(line, scale):
    line[0] *= scale
    line[1] *= scale
    return line


def scale_lines(lines, scale):
    for i in range(len(lines)):
        lines[i] = scale_line(lines[i], scale)
    return lines


def translate_line(line, translation):
    line[0] += translation
    line[1] += translation
    return line


def translate_lines(lines, translation):
    for i in range(len(lines)):
        lines[i] = translate_line(lines[i], translation)
    return lines
