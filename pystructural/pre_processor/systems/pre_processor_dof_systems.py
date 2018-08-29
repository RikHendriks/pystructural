import catecs

from pystructural.solver.components.degree_of_freedom import DOFHolder, DOF
from pystructural.solver.components.element import FrameElement2D, LinearTriangleElement2D
from pystructural.solver.components.load import PointLoad2D, QLoad2D, ImposedLoad2D
from pystructural.solver.components.support import Support
from pystructural.solver.components.connection import Spring

__all__ = ['PreProcessorDofSystems']


# List of all Dof subclasses
dof_subclasses = [FrameElement2D, LinearTriangleElement2D,
                  PointLoad2D, QLoad2D, ImposedLoad2D,
                  Support,
                  Spring]


class PreProcessorDofSystems(catecs.System):
    def __init__(self):
        self.dof_holder = DOFHolder()
        super().__init__()

    def process(self):
        # Run system instance: dof dict update
        self.world.run_system(DOFDictUpdate(self.dof_holder))
        # Run system instance: subclasses dof dict update
        self.world.run_system(SubClassesDOFDictUpdate(self.dof_holder))


class DOFDictUpdate(catecs.System):
    def __init__(self, dof_holder):
        self.dof_holder = dof_holder
        super().__init__()

    def process(self):
        # For every dof instance in the system
        for _, dof_instance in self.world.get_component(DOF):
            # For every dof in the dof instance
            for dof in dof_instance.dof_set:
                # Get the dof id in the dof holder for the corresponding dof
                dof_id = self.dof_holder.add_dof(dof)
                # Set the dof dict where: {dof, dof_id in dof_holder}
                dof_instance.dof_id_dict[dof] = dof_id


class SubClassesDOFDictUpdate(catecs.System):
    def __init__(self, dof_holder):
        self.dof_holder = dof_holder
        super().__init__()

    def process(self):
        # For every dof_subclasses instance in the system
        for dof_subclasses_class in dof_subclasses:
            for entity, dof_subclasses_instance in self.world.get_component(dof_subclasses_class):
                for dof in dof_subclasses_instance.dof_set:
                    # Get the dof id in the dof holder for the corresponding dof
                    dof_id = self.dof_holder.add_dof(dof)
                    # Set the dof dict where: {dof, dof_id in dof_holder}
                    dof_subclasses_instance.dof_id_dict[dof] = dof_id
