__all__ = ['Material',
           'LinearElasticity2DMaterial']


class Material:
    def __init__(self):
        pass


class LinearElasticity2DMaterial(Material):
    def __init__(self, youngs_modulus, mass_density):
        self.youngs_modulus = youngs_modulus
        self.mass_density = mass_density
        super().__init__()
