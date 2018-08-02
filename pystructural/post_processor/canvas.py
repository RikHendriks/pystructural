import copy

import matplotlib.pyplot as plt
import bokeh.plotting as bk_plt
import bokeh.models as bk_mod
import bokeh.io as bk_io
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

    def draw_line(self, x, y, color='black'):
        # If the line is (partially) outside the border then increase the borders
        self.expand_plot_window([min(x), min(y)])
        self.expand_plot_window([max(x), max(y)])
        # Append the line to the line list
        self.lines.append([x, y, color])

    def draw_lines(self, lines, color='black'):
        for x, y in lines:
            self.draw_line(x, y, color)

    def draw_text(self, x, y, text, font_size=12, color='black'):
        self.texts.append([x, y, text, font_size, color])

    def draw_symbol(self, symbol, scale, translation, color='black'):
        symbol = scale_lines(symbol, scale)
        symbol = translate_lines(symbol, translation)
        self.draw_lines(symbol, color)

    def clear(self):
        # Delete the data in the canvas
        del self.lines
        del self.texts
        # Reinitialize the data in the canvas
        self.lines = []
        self.texts = []
        self.plot_window = [0.0, 0.0, 0.0, 0.0]

    def show(self, plot_window=None, visualization_package='matplotlib'):
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
        # Show the canvas with the given visualization package
        if visualization_package == 'matplotlib':
            self.show_matplotlib(plot_window)
        elif visualization_package == 'bokeh':
            self.show_bokeh()

    def save(self, filename, plot_window, visualization_package='matplotlib'):
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
        # Save the canvas with the given visualization package
        if visualization_package == 'matplotlib':
            self.save_matplotlib(filename, plot_window)
        elif visualization_package == 'bokeh':
            self.save_bokeh(filename)
        elif visualization_package == 'svgpathtools':
            self.save_svgpathtools(filename + '.svg')

    def show_matplotlib(self, plot_window):
        # Plot each line to matplotlib
        for line in self.lines:
            plt.plot(line[0], line[1], line[2])
        # Plot each text to matplotlib
        for text in self.texts:
            plt.text(text[0], text[1], text[2], fontsize=text[3], color=text[4])
        # Set the axis
        plt.axis(plot_window)
        # Show the plot
        plt.show()
        # Clear the plot
        plt.gcf().clear()

    def show_bokeh(self):
        # Instantiate the figure
        f = bk_plt.figure()
        # Plot each line to bokeh
        for line in self.lines:
            f.line(line[0], line[1], line_color=line[2])
        # Plot the text to bokeh
        for text in self.texts:
            f.add_layout(bk_mod.Label(x=text[0], y=text[1], text=text[2]))
        # Show the results
        bk_plt.show(f)

    def save_matplotlib(self, filename, plot_window):
        # Plot each line to matplotlib
        for line in self.lines:
            plt.plot(line[0], line[1], line[2])
        # Plot each text to matplotlib
        for text in self.texts:
            plt.text(text[0], text[1], text[2], fontsize=text[3], color=text[4])
        # Set the axis
        plt.axis(plot_window)
        # Save the plotted file
        plt.savefig(filename)
        # Clear the plot
        plt.gcf().clear()

    def save_bokeh(self, filename):
        # Instantiate the figure
        f = bk_plt.figure()
        # Plot each line to bokeh
        for line in self.lines:
            f.line(line[0], line[1], line_color=line[2])
        # Plot the text to bokeh
        for text in self.texts:
            f.add_layout(bk_mod.Label(x=text[0], y=text[1], text=text[2]))
        # Save the results
        bk_io.export_png(f, filename)

    def save_svgpathtools(self, filename):
        lines = []
        for x, y, _ in self.lines:
            for i in range(len(x)-1):
                lines.append(svg.Line(x[i] + y[i] * -1j, x[i+1] + y[i+1] * -1j))
        line_colors = [color for x, _, color in self.lines for _ in range(len(x))]
        text_path = []
        for x, y, _, _, _ in self.texts:
            for i in range(len(x)):
                text_path.append(svg.Line(x[i] + y[i] * -1j, x[i] + 1.0 + y[i] * -1j))
        text = [text for x, _, text, _, _ in self.texts for _ in range(len(x))]
        svg.wsvg(lines, line_colors, stroke_widths=[0.01] * len(lines),
                 text=text, text_path=text_path, font_size=[0.1] * len(text),
                 filename=filename)


def scale_line(line, scale):
    line[0] = [scale * x for x in line[0]]
    line[1] = [scale * y for y in line[1]]
    return line


def scale_lines(lines, scale):
    for i in range(len(lines)):
        lines[i] = scale_line(lines[i], scale)
    return lines


def translate_line(line, translation):
    line[0] = [x + translation[0] for x in line[0]]
    line[1] = [y + translation[1] for y in line[1]]
    return line


def translate_lines(lines, translation):
    for i in range(len(lines)):
        lines[i] = translate_line(lines[i], translation)
    return lines
