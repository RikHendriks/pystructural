import itertools


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

    def add_load_combination(self, load_combination_name, load_cases, is_name=False):
        if is_name:
            load_cases = {self.load_case_names[k]: v for k, v in load_cases.items()}
        # Load cases is a dict of {load_case_name: factor}
        self.load_combinations[self.current_load_combination_id] = load_cases
        self.load_combination_names[load_combination_name] = self.current_load_combination_id
        self.current_load_combination_id += 1
        return self.current_load_combination_id - 1

    def load_case_generator(self, load_case_id):
        for load_combination_id in self.load_combinations:
            if load_case_id in self.load_combinations[load_combination_id]:
                yield load_combination_id, self.load_combinations[load_combination_id][load_case_id]

    def load_combination_creator(self, load_combination_name,
                                 permanent_load_cases=None, switch_load_cases=None, switch_list_load_cases=None):
        # If there is are permanent load cases
        if permanent_load_cases is None:
            permanent_load_cases = {}
        # If there are a switch load cases
        if switch_load_cases:
            switch_load_cases = powerset([list(load_case.items())[0] for load_case in switch_load_cases])
            switch_load_cases = [{load_case[0]: load_case[1] for load_case in load_combination} for load_combination in
                                 switch_load_cases]
        # If there are switch list load cases
        if switch_list_load_cases:
            switch_list_load_cases = itertools.product(*[load_case.items() for load_case in switch_list_load_cases])
            switch_list_load_cases = [{load_case[0]: load_case[1] for load_case in load_combination} for
                                      load_combination in switch_list_load_cases]
        # Add the three load cases to each other to obtain all the load combinations
        load_combination_list = itertools.product(switch_load_cases, switch_list_load_cases)
        load_combination_list = [{k: v for load_case in load_combination for k, v in load_case.items()} for
                                 load_combination in load_combination_list]
        # Add the permanent load cases to each load combination
        for load_case in load_combination_list:
            load_case.update(permanent_load_cases)
        print(load_combination_list)
        # Add the load combinations
        for i in range(len(load_combination_list)):
            self.add_load_combination(load_combination_name + str(i), load_combination_list[i], True)


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
