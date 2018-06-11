__all__ = ['LineElementSortComponent']


class LineElementSortComponent:
    def __init__(self):
        # Every group consists of a list of tuples: (line id, node id,
        # 0 or 1 depending on if the node is the first or second node in the line element point id list)
        self.groups = {}

    def group_id_generator(self):
        for group_id in self.groups:
            yield group_id

    def line_element_id_generator(self, group_id=None):
        if group_id:
            for line_id in self.groups[group_id]:
                yield line_id
        else:
            return None
