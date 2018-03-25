__all__ = ['Load']


class Load:
    compatible_geometry = None

    def __init__(self, point_load_list):
        self.point_load_list = point_load_list
        # Geometry
        self.geometry = None

    def get_dof(self):
        pass

    def get_load_value_to_node_and_dof_variable(self, i):
        pass

    def load_dof_generator(self):
        dim = len(self.point_load_list)
        for i in range(0, dim):
            yield self.get_load_value_to_node_and_dof_variable(i), self.point_load_list[i]
