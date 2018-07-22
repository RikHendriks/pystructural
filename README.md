# PyStructural
[![Build Status](https://travis-ci.org/pystructural/pystructural.svg?branch=master)](https://travis-ci.org/pystructural/pystructural)
[![Documentation Status](https://readthedocs.org/projects/pystructural/badge/?version=latest)](https://pystructural.readthedocs.io/en/latest/?badge=latest)

PyStructural is a structural finite element method implementation in Python.

The design philosophy of PyStructural is that PyStructal:
* is completely written in Python
* is highly customizable
* uses an Entity Component System (ECS) as its core architecture ([CATECS](https://github.com/RikHendriks/catecs))

## Basic usage

The following shows an example of a simple structure that consists of a horizontal frame with a pointload in the middle.

```python
import pystructural as ps


# Create a structure instance
structure = ps.core.Structure2D()

# Add a frame element
structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0e4, 1.0, 1.0, 1.0)

# Add supports
structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
structure.add_support([10.0, 0.0], displacement_y=False)

# Add a point load
structure.add_point_load([5.0, 0.0], [0.0, -10.0, 0.0])

# Solve the linear system
structure.solve_linear_system()

# Show the structure
structure.show_structure()
```

<coming soon, a nice picture of this structure>

## Installation

Currently PyStructural can only be installed by using the terminal. Open a terminal in the directory in which the setup.py file of PyStructural is and enter the following command:

    python setup.py install

## Roadmap

Coming soon!