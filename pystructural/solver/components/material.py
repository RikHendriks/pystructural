"""
pystructural.solver.components.material
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the various materials.
"""
__all__ = ['Material',
           'LinearElasticity2DMaterial']


class Material:
    """The basic material class which each material needs to inherit.
    """

    def __init__(self):
        pass


class LinearElasticity2DMaterial(Material):
    """The linear elasticity 2d material which inherits from the material class.

    :param youngs_modulus: The youngs modulus of the material.
    :param mass_density: The mass density of the material.
    """

    def __init__(self, youngs_modulus, mass_density):
        self.youngs_modulus = youngs_modulus
        self.mass_density = mass_density
        super().__init__()
