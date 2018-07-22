from pystructural.core.math_ps import *


__all__ = ['Results', 'LineResults']


class Results:
    def __init__(self):
        pass


class LineResults(Results):
    def __init__(self, line_start, line_end):
        self.line_start = line_start
        self.line_end = line_end
        # Initialize the variables for the combined line value generator
        self.is_initialized = False
        self.combined_line_values = []
        # line_values_dict{line_id}[line][node_unit, value]
        self.line_values_dict = {}
        self.current_line_values_list_id = 0
        super().__init__()

    def add_line_values(self, line_values):
        self.is_initialized = False
        self.line_values_dict[self.current_line_values_list_id] = \
            [[line_to_unit_interval(line[0], self.line_start, self.line_end), line[1], line[2]] for line in line_values]
        self.current_line_values_list_id += 1
        return self.current_line_values_list_id - 1

    def initialize_combined_line_value_generator(self):
        # Delete the current combined line value list and initialize it as a new list
        del self.combined_line_values
        self.combined_line_values = []
        # Initialize the line generator list
        line_generator_list = {k: 0 for k in self.line_values_dict.keys()}

        # Define the advance line generator list
        def advance_line_generator_list(k):
            if line_generator_list[k] + 1 < len(self.line_values_dict[k]):
                line_generator_list[k] += 1
                return True
            else:
                return False

        # While the lines haven't all ended
        while True:
            # Get the minimum value in the unit interval
            min_unit = min(*[self.line_values_dict[k][v][0] for k, v in line_generator_list.items()])

            # Find all the line points that have this minimum unit interval
            k_min_dict = {k: v for k, v in line_generator_list.items() if self.line_values_dict[k][v][0] == min_unit}
            k_min_values = [self.line_values_dict[k][v][1] for k, v in k_min_dict.items()]
            k_load_combinations = [self.line_values_dict[k][v][2] for k, v in k_min_dict.items()]

            # Yield the unit interval and the values at the interval
            self.combined_line_values.append([line_embedding(min_unit, self.line_start, self.line_end), k_min_values,
                                              k_load_combinations])

            # Advance the lines in the k_min_list
            is_all_none = True
            for k in k_min_dict:
                if advance_line_generator_list(k) is True:
                    is_all_none = False

            # End the while loop if no k has advanced
            if is_all_none:
                break
        # Set the is initialized value to true
        self.is_initialized = True

    def combined_line_value_generator(self):
        # If the combined line value generator is not yet initialized
        if not self.is_initialized:
            self.initialize_combined_line_value_generator()
        # Yield every element in the combined line values list
        for combined_line_value in self.combined_line_values:
            yield combined_line_value
