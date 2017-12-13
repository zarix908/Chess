from enums import PieceType, PieceColor
from model.cell import Cell
from model.map import Map
from model.validators.abstract_validators_container import *
from model.validators.cell_bit_determinant import CellBitDeterminant
from model.vector import Vector


class AppendixRulesValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, current_map, previous_map, move_vector,
                 color_current_move):
        super().__init__(current_map, move_vector)
        self.__previous_map = previous_map
        self.__color_current_move = color_current_move

    @validator(ValidatorTypes.ALLOW)
    def pawn_capture_other_pawn_on_aisle(self):
        if self.__previous_map is None or self._move_vector.x == 0:
            return False

        last_move_vector = Map.get_last_move_vector(self.__previous_map,
                                                    self._current_map)
        enemy_piece = self._current_map.get(last_move_vector.end_cell)

        if enemy_piece.type is not \
                PieceType.PAWN or last_move_vector.length_in_cells != 2:
            return False

        if last_move_vector.end_cell == self._move_vector \
                .horizontal_ort.end_cell:
            self.notify_game_remove_piece(last_move_vector.end_cell)
            return True

        return False

    @validator(ValidatorTypes.ALLOW)
    def castling(self):
        piece = self._active_piece
        if piece.type is not PieceType.KING or self._current_map.king_is_moved(
                piece):
            return False

        y = 0 if piece.color == PieceColor.WHITE else 7
        start_x = 4
        end_x = 6
        start_cell = Cell(start_x, y)
        end_cell = Cell(end_x, y)
        vector = Vector(start_cell, end_cell)

        if vector != self._move_vector:
            return False

        rook = self._current_map.get(Cell(end_x + 1, y))
        if rook is None or rook.type is not PieceType.ROOK:
            return False
        if self._current_map.rook_is_moved(rook):
            return False

        y = 0 if piece.color == PieceColor.WHITE else 7
        for x in range(4, 8):
            cell_bit_determinant = CellBitDeterminant(self._current_map,
                                                      Cell(x, y))

            if cell_bit_determinant.is_bit(piece.color):
                return False

        return True

    @validator(ValidatorTypes.PROHIBIT)
    def current_color_move_satisfies(self):
        return self._active_piece.color != self.__color_current_move
