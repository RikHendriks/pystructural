__all__ = ['LoadCombinationsComponent']


class LoadCombinationsComponent:
    def __init__(self):
        # Load cases
        self.load_cases = {}
        self.current_load_case_id = 0
        self.load_case_names = {}
        # Load combinations
        self.load_combinations = {}
        self.current_load_combination_id = 0
        self.load_combination_names = {}

    def _add_new_load_case(self, load_case_name):
        self.load_cases[self.current_load_case_id] = load_case_name
        self.load_case_names[load_case_name] = self.current_load_case_id
        self.current_load_case_id += 1
        return self.current_load_case_id - 1

    def add_generic_load_combination(self):
        self.add_load_combination('generic_load_combination', {load_case_id: 1.0 for load_case_id in self.load_cases})

    def add_load_case(self, load_case_name):
        if load_case_name in self.load_case_names:
            return self.load_case_names[load_case_name]
        else:
            return self._add_new_load_case(load_case_name)

    def add_load_combination(self, load_combination_name, load_cases):
        # Load cases is a dict of {load_case_name: factor}
        self.load_combinations[self.current_load_combination_id] = load_cases
        self.load_combination_names[load_combination_name] = self.current_load_combination_id
        self.current_load_combination_id += 1
        return self.current_load_combination_id - 1

    def load_case_generator(self, load_case_id):
        for load_combination_id in self.load_combinations:
            if load_case_id in self.load_combinations[load_combination_id]:
                yield load_combination_id, self.load_combinations[load_combination_id][load_case_id]
