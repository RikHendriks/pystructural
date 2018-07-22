.. _examples/basic_structure:

Example - Basic Structure
=========================

Import PyStructural.

.. code-block:: python

    import pystructural as ps

Create a structure instance.

.. code-block:: python

    # Create a structure instance
    structure = ps.core.Structure2D()

Add a frame element to the structure instance.

.. code-block:: python

    # Add a frame element
    structure.add_frame_element([0.0, 0.0], [10.0, 0.0], 1.0e4, 1.0, 1.0, 1.0)

Add the supports at both ends of the frame element.

.. code-block:: python

    # Add supports
    structure.add_support([0.0, 0.0], displacement_x=False, displacement_y=False)
    structure.add_support([10.0, 0.0], displacement_y=False)

Add a point load in the middle of the structure.

.. code-block:: python

    # Add a point load
    structure.add_point_load([5.0, 0.0], [0.0, -10.0, 0.0])

We are going to solve the linear system of the structure instance.

.. code-block:: python

    # Solve the linear system
    structure.solve_linear_system()

We are going to show the results of the linear calculation.

.. code-block:: python

    # Show the structure
    structure.show_structure()


Full Code
^^^^^^^^^

The full code of the example:

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
