__all__ = ['Load']


class Load:
    compatible_geometry = None

    def __init__(self):
        # Geometry
        self.geometry = None

    def get_dof(self):
        pass

    def load_dof_generator(self):
        pass
