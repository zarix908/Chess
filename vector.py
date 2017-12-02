import math
import numpy as np
from cell import Cell
from copy import copy


class Vector:
    def __init__(self, *args):
        self.__start_cell = None
        self.__end_cell = None

        if len(args) == 2:
            self.init(args[0], args[1])

        elif len(args) == 3:
            start_cell = args[0]
            x = args[1]
            y = args[2]

            self.init(start_cell, Cell(start_cell.x + x, start_cell.y + y))

    def init(self, start_cell, end_cell):
        self.__start_cell = start_cell
        self.__end_cell = end_cell

    @property
    def start_cell(self):
        return self.__start_cell

    @property
    def end_cell(self):
        return self.__end_cell

    @property
    def x(self):
        return self.__end_cell.x - self.start_cell.x

    @property
    def y(self):
        return self.__end_cell.y - self.__start_cell.y

    @property
    def length_in_cells(self):
        return max(abs(self.x), abs(self.y))

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def ort_in_cells(self):
        return Vector(copy(self.__start_cell), np.sign(self.x),
                      np.sign(self.y))

    def contain(self, other):
        return self.co_directed(other) and self.length >= other.length

    def co_directed(self, other):
        return self.x * other.y == self.y * other.x and np.sign(
            self.x * self.y) == np.sign(other.x * other.y)

    def __add__(self, other):
        return Vector(copy(self.__start_cell), self.x + other.x,
                      self.y + other.y)

    def __copy__(self):
        return Vector(copy(self.__start_cell), copy(self.__end_cell))
