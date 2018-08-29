"""
pystructural.solver.components.connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the various connections.
"""
from pystructural.solver.components.degree_of_freedom import DOF

__all__ = ['Connection',
           'Spring']


class Connection:
    """The basic connection class which each geometry needs to inherit.
    """

    def __init__(self):
        pass


# TODO change this class
class Spring(Connection, DOF):
    """The Spring geometry class which inherits from the connection and dof classes.

    :param spring_x: Spring value for the x axis, dof id: 0.
    :param spring_y: Spring value for the y axis, dof id: 1.
    :param spring_z: Spring value for the z axis, dof id: 2.
    :param rotation_spring_x: Rotational spring value for the x axis, dof id: 3.
    :param rotation_spring_y: Rotational spring value for the y axis, dof id: 4.
    :param rotation_spring_z: Rotational spring value for the z axis, dof id: 5.
    """

    def __init__(self, spring_x=None, spring_y=None, spring_z=None,
                 rotation_spring_x=None, rotation_spring_y=None, rotation_spring_z=None):
        self.spring_x = spring_x
        self.spring_y = spring_y
        self.spring_z = spring_z
        self.rotation_spring_x = rotation_spring_x
        self.rotation_spring_y = rotation_spring_y
        self.rotation_spring_z = rotation_spring_z
        Connection.__init__(self)
        # Get the list of the dof's corresponding to the
        dof_id_list = []
        if spring_x:
            dof_id_list.append("displacement_x")
        if spring_y:
            dof_id_list.append("displacement_y")
        if spring_z:
            dof_id_list.append("displacement_z")
        if rotation_spring_x:
            dof_id_list.append("rotation_x")
        if rotation_spring_y:
            dof_id_list.append("rotation_y")
        if rotation_spring_z:
            dof_id_list.append("rotation_z")
        # Initialize the DOF
        DOF.__init__(self, *dof_id_list)

    def spring_dof_generator(self):
        """A generator for the dof and the corresponding spring value.

        :return: A tuple (dof_id, spring_value)
        """
        # For every dof that is used in the spring
        for dof in self.dof_id_dict:
            if dof == "displacement_x":
                yield (self.dof_id_dict[dof], self.spring_x)
            elif dof == "displacement_y":
                yield (self.dof_id_dict[dof], self.spring_y)
            elif dof == "displacement_z":
                yield (self.dof_id_dict[dof], self.spring_z)
            elif dof == "rotation_x":
                yield (self.dof_id_dict[dof], self.rotation_spring_x)
            elif dof == "rotation_y":
                yield (self.dof_id_dict[dof], self.rotation_spring_y)
            elif dof == "rotation_z":
                yield (self.dof_id_dict[dof], self.rotation_spring_z)
