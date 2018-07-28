"""
pystructural.solver.components.phased_analysis_components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implements the phased analysis class.
"""
__all__ = ['PhasedAnalysis']


class PhasedAnalysis:
    """The phased analysis class. This class is used to define the phases of an analysis and to set relations to the
    phases, for example a phase that precedes another.
    """

    def __init__(self):
        # Initialize phases
        self.phases = {}
        self.phase_names = {}
        self.previous_phases = {}
        self.current_phase_id = 0

    def create_phase(self, phase_name):
        """Creates a phase and adds it to the phased analysis.

        :param phase_name: The name of the phase that needs to be created.
        :return: Returns the phase id of the created phase.
        """
        self.phases[self.current_phase_id] = phase_name
        self.phase_names[phase_name] = self.current_phase_id
        self.previous_phases[self.current_phase_id] = []
        self.current_phase_id += 1
        return self.current_phase_id - 1

    def phase_generator(self):
        """A generator for the phases that are defined in the phased analysis.

        :return: Yields the phase id for every phase defined in the phased analysis.
        """
        # A generator for every phase
        for phase_id in self.phases:
            yield phase_id

    def add_previous_phase(self, phase_id, *previous_phase_id_list):
        """Defines the previous phases of a phase.

        :param phase_id: The phase id of the phase for which the previous phases needs to be defined.
        :param *previous_phase_id_list: The previous phase id's.
        """
        for previous_phase in previous_phase_id_list:
            self.previous_phases[phase_id].append(previous_phase)
