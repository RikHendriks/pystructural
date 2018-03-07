__all__ = ['DOF']


class DOF:
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

    def update_dof(self, other_dof):
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

    def get_dof(self, i):
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

    def get_dof_id_list(self):
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
        return id_list