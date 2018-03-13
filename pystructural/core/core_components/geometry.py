__all__ = ['Geometry']


class Geometry:

    def __init__(self, point_id_list, point_list):
        self.point_id_list = point_id_list
        self.point_list = point_list
        # Variables
        self.area = None

    def compute_area(self):
        pass