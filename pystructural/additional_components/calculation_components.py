__all__ = ["GeneralComponent", "DOFCalculationComponent"]


class GeneralComponent:
    pass


class DOFCalculationComponent:
    def __init__(self):
        self.local_to_global_dof_dict = {}
        self.global_to_local_dof_dict = {}