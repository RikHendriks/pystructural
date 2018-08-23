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
        DOF.__init__(self, self.spring_x is not None, self.spring_y is not None, self.spring_z is not None,
                     self.rotation_spring_x is not None, self.rotation_spring_y is not None,
                     self.rotation_spring_z is not None)

    def spring_dof_generator(self):
        """A generator for the dof and the corresponding spring value.

        :return: A tuple (dof_id, spring_value)
        """
        dof_id_list = self.dof_id_list
        # For every dof that is used in the spring
        for dof_id in dof_id_list:
            if dof_id == 0:
                yield (dof_id, self.spring_x)
            elif dof_id == 1:
                yield (dof_id, self.spring_y)
            elif dof_id == 2:
                yield (dof_id, self.spring_z)
            elif dof_id == 3:
                yield (dof_id, self.rotation_spring_x)
            elif dof_id == 4:
                yield (dof_id, self.rotation_spring_y)
            elif dof_id == 5:
                yield (dof_id, self.rotation_spring_z)
