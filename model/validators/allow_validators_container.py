import math

from enums import PieceType
from model.map import Map
from model.validators.abstract_validators_container import *


class AllowValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        for allow_validator in self.get_validators():
            if allow_validator():
                return True

    @validator
    def vertical_horizontal_moving(self):
        x = self._move_vector.x
        y = self._move_vector.y
        length_in_cells = self._move_vector.length_in_cells
        return self.moving_validator(
            [PieceType.ROOK, PieceType.QUEEN, PieceType.KING, PieceType.PAWN],
            lambda: (x == 0 or y == 0) and length_in_cells != 0)

    @validator
    def diagonal_moving(self):
        return self.moving_validator(
            [PieceType.BISHOP, PieceType.QUEEN, PieceType.KING],
            lambda: abs(self._move_vector.x) == abs(self._move_vector.y))

    @validator
    def knight_moving(self):
        length = self._move_vector.length
        return self.moving_validator([PieceType.KNIGHT],
                                     lambda: length == math.sqrt(5))

    @validator
    def pawn_capture_piece(self):
        target = self._current_map.get(self._move_vector.end_cell)
        x = self._move_vector.x
        y = self._move_vector.y

        return abs(x) == abs(y) == 1 and target is not None

    @validator
    def pawn_capture_other_pawn_on_aisle(self):
        if self._previous_map is None or self._move_vector.x == 0:
            return False

        last_move_vector = Map.get_last_move_vector(self._previous_map,
                                                    self._current_map)
        enemy_piece = self._current_map.get(last_move_vector.end_cell)

        if enemy_piece.type is not \
                PieceType.PAWN or last_move_vector.length_in_cells != 2:
            return False

        if last_move_vector.end_cell == self._move_vector\
                .horizontal_ort.end_cell:
            self.notify_game_remove_piece(last_move_vector.end_cell)
            return True

        return False
