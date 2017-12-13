from model.cell import Cell
from model.map import Map
from model.validators.trajectory_validators_container import \
    TrajectoryValidatorsContainer
from model.vector import Vector


class CellBitDeterminant:
    def __init__(self, current_map, cell=None):
        self.__current_map = current_map
        self.__cell = cell

    def is_bit(self, self_color):
        res = self.get_bit_cell_from([self.__cell])
        if res is None:
            return False

        attacking_piece = self.__current_map.get(res[1])
        return attacking_piece.color != self_color

    def get_bit_piece_from(self, cells_list):
        res = self.get_bit_cell_from(cells_list)
        return self.__current_map.get(res if res is None else res[0])

    def get_bit_cell_from(self, cells_list):
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                cell = Cell(x, y)
                piece = self.__current_map.get(cell)

                if piece is None:
                    continue

                for sought_cell in cells_list:
                    if self.__valid_trajectory(Vector(cell, sought_cell)):
                        return sought_cell, cell

        return None

    def __valid_trajectory(self, next_move_vector):
        return TrajectoryValidatorsContainer(self.__current_map,
                                             next_move_vector).is_valid()
