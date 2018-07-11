__all__ = ['Load', 'ImposedLoad']


class Load:
    compatible_geometry = None

    def __init__(self, load_case_id):
        # Geometry
        self.geometry = None
        # Load combination id
        self.load_case_id = load_case_id

    def get_dof(self):
        pass

    def load_dof_generator(self):
        pass


class ImposedLoad(Load):
    def __init__(self, load_case_id):
        super().__init__(load_case_id)
