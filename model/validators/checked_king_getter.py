from enums import PieceType, PieceColor
from model.cell import Cell
from model.map import Map
from model.piece import Piece

from model.validators.trajectory_validators_container import \
    TrajectoryValidatorsContainer
from model.vector import Vector


class CheckedKingGetter:
    def __init__(self, current_map):
        self.__current_map = current_map

    def get_checked_king(self):
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                cell = Cell(x, y)
                piece = self.__current_map.get(cell)

                if piece is None:
                    continue

                for king_cell in self.__get_kings_cells():
                    if self.__valid_trajectory(Vector(cell, king_cell)):
                        return self.__current_map.get(king_cell)

        return None

    def __valid_trajectory(self, next_move_vector):
        return TrajectoryValidatorsContainer(self.__current_map,
                                             next_move_vector).is_valid()

    def __get_kings_cells(self):
        for color in PieceColor:
            sought_piece = Piece(PieceType.KING, color)
            yield Map.find(self.__current_map, sought_piece)
        """for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                cell = Cell(x, y)
                piece = self.__current_map.get(cell)

                if piece is not None and piece.type is PieceType.KING:
                    yield cell"""
