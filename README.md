# PyStructural
PyStructural is a structural finite element method implementation in Python.

The design philosophy of PyStructural is:
* Completely written in Python
* Highly customizable

## Basic usage

The following shows an example of a simple structure that consists of a horizontal frame with a pointload in the middle.

```python
import pystructural as ps


# Create an structure instane
structure = ps.core.Structure2D()

# Add two frame elements to the structure
structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)

# Add supports
structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
structure.add_support([10.0, 0.0], displacement_y=False)

# Add a point load
structure.add_point_load([5.0, 0.0], [0.0, -10.0, 0.0])

# Solve the linear system
structure.solve_linear_system()

# Show structure
pp = ps.post_processor.PostProcessor(structure)
pp.show_structure([-5.0, 15.0, -5.0, 5.0])
```

<coming soon, a nice picture of this structure>

## Installation

Currently PyStructural can only be installed by using the terminal. Open a terminal in the directory in which the setup.py file of PyStructural is and enter the following command:

    python setup.py install

## Roadmap

Coming soon!