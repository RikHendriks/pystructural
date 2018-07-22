__all__ = ['PhasedAnalysis']


class PhasedAnalysis:
    def __init__(self):
        # Initialize phases
        self.phases = {}
        self.phase_names = {}
        self.previous_phases = {}
        self.current_phase_id = 0

    def add_phase(self, phase_name):
        self.phases[self.current_phase_id] = phase_name
        self.phase_names[phase_name] = self.current_phase_id
        self.previous_phases[self.current_phase_id] = []
        self.current_phase_id += 1
        return self.current_phase_id - 1

    def phase_generator(self):
        # A generator for every phase
        for phase_id in self.phases:
            yield phase_id

    def add_previous_phase(self, phase_id, *previous_phases):
        for previous_phase in previous_phases:
            self.previous_phases[phase_id].append(previous_phase)