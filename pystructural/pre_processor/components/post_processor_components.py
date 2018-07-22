__all__ = ['LineElementSortComponent']


class LineElementSortComponent:
    def __init__(self):
        # Every group consists of a list of tuples: (line id, node id,
        # 0 or 1 depending on if the node is the first or second node in the line element point id list)
        self.groups = {}
        self.groups_phase_id_list = {}

    def group_id_generator(self, phase_id_filter):
        for group_id in self.groups:
            if phase_id_filter is not None:
                if phase_id_filter in self.groups_phase_id_list[group_id]:
                    yield group_id
            else:
                yield group_id

    def line_element_id_generator(self, group_id):
        if group_id in self.groups:
            for line_id in self.groups[group_id]:
                yield line_id
        else:
            return None
