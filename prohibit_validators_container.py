import numpy as np

from abstract_validators_container import *
from enums import PieceType, PieceColor
from piece import Piece
from ray import Ray


class ProhibitValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        for prohibit_validator in self.get_validators():
            if prohibit_validator():
                return False

        return True

    @validator
    def king_limit_moving_length(self):
        length_in_cells = self._move_vector.length_in_cells
        return self.moving_validator([PieceType.KING],
                                     lambda: length_in_cells != 1)

    @validator
    def pawn_limit_moving_length(self):
        piece = self._active_piece
        if piece.type is not PieceType.PAWN:
            return False

        critical_cell_y = 1 if piece.color is PieceColor.WHITE else 6

        return self._move_vector.length_in_cells > (
            2 if self._move_vector.start_cell.y == critical_cell_y else 1)

    @validator
    def pawn_direction_moving(self):
        piece = self._active_piece

        if piece.type != PieceType.PAWN:
            return False

        right_direction_y_value = 1 if piece.color is PieceColor.WHITE else -1
        return np.sign(self._move_vector.y) != right_direction_y_value

    @validator
    def jump_across_pieces(self):
        if self._active_piece.type is PieceType.KNIGHT:
            return False

        ray = Ray(self._current_map, self._move_vector.ort_in_cells)
        near_piece_vector = ray.cast(lambda obj: isinstance(obj, Piece))

        if near_piece_vector is None:
            return False

        return not near_piece_vector.contain(self._move_vector)

    @validator
    def pawn_capture_piece_by_vertical(self):
        if self._active_piece.type is not PieceType.PAWN:
            return False

        target_cell = self._move_vector.end_cell
        target = self._current_map.get(target_cell)

        return self._move_vector.x == 0 and target is not None
