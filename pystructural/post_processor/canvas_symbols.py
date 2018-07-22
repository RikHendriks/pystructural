import numpy as np


__all__= ['get_right_arrow_symbol', 'get_up_arrow_symbol',
          'get_rotation_block_symbol', 'get_rotation_spring_symbol', 'get_displacement_block',
          'get_displacement_free_x', 'get_displacement_free_y']

# -------------------
# -- arrow symbols --
# -------------------


def get_right_arrow_symbol():
    lines = []
    lines.append([np.array([0.0, 0.0]), np.array([-0.25, 0.25])])
    lines.append([np.array([0.0, 0.0]), np.array([-0.25, -0.25])])
    lines.append([np.array([0.0, 0.0]), np.array([-1.0, 0.0])])
    return lines


def get_up_arrow_symbol():
    lines = []
    lines.append([np.array([0.0, 0.0]), np.array([-0.25, -0.25])])
    lines.append([np.array([0.0, 0.0]), np.array([0.25, -0.25])])
    lines.append([np.array([0.0, 0.0]), np.array([0.0, -1.0])])
    return lines


# ---------------------
# -- support symbols --
# ---------------------


def get_rotation_block_symbol():
    lines = []
    lines.append([np.array([-0.5, 0.5]), np.array([0.5, 0.5])])
    lines.append([np.array([0.5, 0.5]), np.array([0.5, -0.5])])
    lines.append([np.array([0.5, -0.5]), np.array([-0.5, -0.5])])
    lines.append([np.array([-0.5, -0.5]), np.array([-0.5, 0.5])])
    return lines


def get_rotation_spring_symbol():
    lines = []
    for i in range(0, 50):
        f = (float(i) / 50.0) * 1.05
        s = (float(i + 1) / 50.0) * 1.05
        f_n = 0.5 * np.array([f * np.cos(((4 * f) - 0.5) * np.pi), f * np.sin(((4 * f) - 0.5) * np.pi)])
        s_n = 0.5 * np.array([s * np.cos(((4 * s) - 0.5) * np.pi), s * np.sin(((4 * s) - 0.5) * np.pi)])
        lines.append([f_n, s_n])
    return lines


def get_displacement_block():
    lines = []
    lines.append([np.array([0.0, 0.0]), np.array([-0.5, -0.5])])
    lines.append([np.array([0.0, 0.0]), np.array([0.5, -0.5])])
    lines.append([np.array([-0.7, -0.5]), np.array([0.7, -0.5])])
    return lines


def get_displacement_free_x():
    lines = []
    lines.append([np.array([0.0, 0.0]), np.array([-0.5, -0.5])])
    lines.append([np.array([0.0, 0.0]), np.array([0.5, -0.5])])
    lines.append([np.array([-0.7, -0.5]), np.array([0.7, -0.5])])
    lines.append([np.array([-0.7, -0.7]), np.array([0.7, -0.7])])
    return lines


def get_displacement_free_y():
    lines = []
    lines.append([np.array([0.0, 0.0]), np.array([-0.5, 0.5])])
    lines.append([np.array([0.0, 0.0]), np.array([-0.5, -0.5])])
    lines.append([np.array([-0.5, 0.7]), np.array([-0.5, -0.7])])
    lines.append([np.array([-0.7, 0.7]), np.array([-0.7, -0.7])])
    return lines
