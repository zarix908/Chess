from copy import copy

from model.map import Map


class Ray:
    def __init__(self, map, ort):
        self.__map = map
        self.__ort = ort

    def cast(self, cast_stop_condition):
        ray = copy(self.__ort)

        obj = self.get_object_by_vector(ray)
        while not cast_stop_condition(obj) and self.map_contain_vector(ray):
            ray += self.__ort
            obj = self.get_object_by_vector(ray)

        return ray if self.map_contain_vector(ray) else None

    def get_object_by_vector(self, vector):
        target_cell = vector.end_cell
        return self.__map.get(target_cell)

    @staticmethod
    def map_contain_vector(vector):
        return max(abs(vector.x), abs(vector.y)) < Map.SIZE
