class Move:
    def __init__(self, start_cell, end_cell):
        self.__start_cell = start_cell
        self.__end_cell = end_cell

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

    def __eq__(self, other):
        return self.start_cell == other.start_cell \
               and self.end_cell == other.end_cell
