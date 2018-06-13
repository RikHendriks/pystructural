from pystructural.solver.components.connection import Connection
from pystructural.solver.components.degree_of_freedom import DOF

__all__ = ['Spring']


class Spring(Connection, DOF):
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
        dof_id_list = self.get_dof_id_list()
        # For every dof that is used in the spring
        for dof in dof_id_list:
            if dof == 0:
                yield (dof, self.spring_x)
            elif dof == 1:
                yield (dof, self.spring_y)
            elif dof == 2:
                yield (dof, self.spring_z)
            elif dof == 3:
                yield (dof, self.rotation_spring_x)
            elif dof == 4:
                yield (dof, self.rotation_spring_y)
            elif dof == 5:
                yield (dof, self.rotation_spring_z)
