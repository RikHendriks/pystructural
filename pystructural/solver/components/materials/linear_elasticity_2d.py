from pystructural.solver.components.materials.material import *

__all__ = ['LinearElasticity2DMaterial']


class LinearElasticity2DMaterial(Material):
    def __init__(self, youngs_modulus, mass_density):
        self.youngs_modulus = youngs_modulus
        self.mass_density = mass_density
        super().__init__()
