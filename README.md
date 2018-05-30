# PyStructural
A structural finite element method implementation.

## Installing and running

### Installation

Currently PyStructural can only be installed by using the terminal. Open a terminal in the directory in which the setup.py file of PyStructural is and enter the following command:

    python setup.py install

### Using the program

Coming soon!

```python
import pystructural as ps


# Create a structure instane
structure = ps.core.Structure2D()

# Add two frame elements to the structure
structure.add_frame_element([0.0, 0.0], [5.0, 0.0], 1.0, 1.0, 1.0, 1.0)
structure.add_frame_element([5.0, 0.0], [10.0, 0.0], 1.0, 1.0, 1.0, 1.0)

# Add supports
structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
structure.add_support([10.0, 0.0], displacement_y=False)

# Add a point load
structure.add_point_load([5.0, 0.0], [0.0, -10.0, 0.0])

# Solve the linear system
structure.solve_linear_system()
```