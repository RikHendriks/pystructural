.. _getting_started:

Getting Started
===============

Installation
^^^^^^^^^^^^

Currently PyStructural can only be installed by using the terminal. Open a terminal in the directory in which the
setup.py file of PyStructural is and enter the following command::

    python setup.py install


Basic Example
^^^^^^^^^^^^^

The following shows an example of a simple structure that consists of a horizontal frame with a point load in the
middle, for more information see :ref:`examples/basic_structure`.

.. code-block:: python

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
