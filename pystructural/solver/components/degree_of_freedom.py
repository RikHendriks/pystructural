"""
pystructural.solver.components.degree_of_freedom
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the degree of freedom class.
"""
__all__ = ['DOF']


class DOF:
    """The DOF (degree of freedom) class which holds the information of which kinds of DOFs are active or inactive on
    a given entity.

    :param displacement_x: DOF for the displacement in the x axis, dof id: 0.
    :param displacement_y: DOF for the displacement in the y axis, dof id: 1.
    :param displacement_z: DOF for the displacement in the z axis, dof id: 2.
    :param rotation_x: DOF for the rotation around the x axis, dof id: 3.
    :param rotation_y: DOF for the rotation around the y axis, dof id: 4.
    :param rotation_z: DOF for the rotation around the z axis, dof id: 5.
    """

    def __init__(self, displacement_x=False, displacement_y=False, displacement_z=False,
                 rotation_x=False, rotation_y=False, rotation_z=False):
        # Initialize the displacements
        self.displacement_x = displacement_x
        self.displacement_y = displacement_y
        self.displacement_z = displacement_z
        # Initialize the rotations
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        # Initialize the dof id list
        self.dof_id_list = None
        # Update the dof id list
        self.update_dof_id_list()

    def update_dof(self, other_dof):
        """Update self with another dof: set each bool to true in self if it is true in other_dof.

        :param other_dof: The other dof with which to update self.
        """
        # Displacement x
        if other_dof.displacement_x is True:
            self.displacement_x = True
        # Displacement y
        if other_dof.displacement_y is True:
            self.displacement_y = True
        # Displacement z
        if other_dof.displacement_z is True:
            self.displacement_z = True
        # Rotation x
        if other_dof.rotation_x is True:
            self.rotation_x = True
        # Rotation y
        if other_dof.rotation_y is True:
            self.rotation_y = True
        # Rotation z
        if other_dof.rotation_z is True:
            self.rotation_z = True
        # Update the dof id list
        self.update_dof_id_list()

    def check_dof_id(self, i):
        """Check if a DOF is on or off.

        :param i: The dof id number.
        :return: Return True if the DOF corresponding with the id number is active.
        """
        # Displacement x
        if i == 0:
            return self.displacement_x
        # Displacement y
        elif i == 1:
            return self.displacement_y
        # Displacement z
        elif i == 2:
            return self.displacement_z
        # Rotation x
        elif i == 3:
            return self.rotation_x
        # Rotation y
        elif i == 4:
            return self.rotation_y
        # Rotation z
        elif i == 5:
            return self.rotation_z
        else:
            raise IndexError("This function only accepts an integer number from 0 to 5")

    def update_dof_id_list(self):
        """Update the dof_id_list: put each DOF id in the dof_id_list if the DOF is active.
        """
        id_list = []
        # Displacement x
        if self.displacement_x is True:
            id_list.append(0)
        # Displacement y
        if self.displacement_y is True:
            id_list.append(1)
        # Displacement z
        if self.displacement_z is True:
            id_list.append(2)
        # Rotation x
        if self.rotation_x is True:
            id_list.append(3)
        # Rotation y
        if self.rotation_y is True:
            id_list.append(4)
        # Rotation z
        if self.rotation_z is True:
            id_list.append(5)
        # Return the id_list
        self.dof_id_list = id_list
