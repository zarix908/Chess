import numpy as np
from model.piece import Piece

from enums import PieceType, PieceColor
from model.ray import Ray
from model.validators.abstract_validators_container import *


class TrajectoryValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, current_map, move_vector):
        super().__init__(current_map, move_vector)

    @validator(ValidatorTypes.PROHIBIT)
    def king_limit_move_length(self):
        length_in_cells = self._move_vector.length_in_cells
        return self.move_validator([PieceType.KING],
                                   lambda: length_in_cells != 1)

    @validator(ValidatorTypes.PROHIBIT)
    def pawn_limit_move_length(self):
        piece = self._active_piece
        if piece.type is not PieceType.PAWN:
            return False

        critical_cell_y = 1 if piece.color is PieceColor.WHITE else 6

        return self._move_vector.length_in_cells > (
            2 if self._move_vector.start_cell.y == critical_cell_y else 1)

    @validator(ValidatorTypes.PROHIBIT)
    def pawn_direction_move(self):
        piece = self._active_piece

        if piece.type != PieceType.PAWN:
            return False

        right_direction_y_value = 1 if piece.color is PieceColor.WHITE else -1
        return np.sign(self._move_vector.y) != right_direction_y_value

    @validator(ValidatorTypes.PROHIBIT)
    def jump_across_pieces(self):
        if self._active_piece.type is PieceType.KNIGHT:
            return False

        ray = Ray(self._current_map, self._move_vector.ort_in_cells)
        near_piece_vector = ray.cast(lambda obj: isinstance(obj, Piece))

        if near_piece_vector is None:
            return False

        return not near_piece_vector.contain(self._move_vector)

    @validator(ValidatorTypes.PROHIBIT)
    def pawn_capture_piece_by_vertical(self):
        if self._active_piece.type is not PieceType.PAWN:
            return False

        target_cell = self._move_vector.end_cell
        target = self._current_map.get(target_cell)

        return self._move_vector.x == 0 and target is not None

    @validator(ValidatorTypes.PROHIBIT)
    def capture_self_color_piece(self):
        piece = self._active_piece
        target = self._current_map.get(self._move_vector.end_cell)

        if target is None:
            return False

        return piece.color == target.color

    @validator(ValidatorTypes.ALLOW)
    def vertical_horizontal_move(self):
        x = self._move_vector.x
        y = self._move_vector.y
        length_in_cells = self._move_vector.length_in_cells
        return self.move_validator(
            [PieceType.ROOK, PieceType.QUEEN, PieceType.KING, PieceType.PAWN],
            lambda: (x == 0 or y == 0) and length_in_cells != 0)

    @validator(ValidatorTypes.ALLOW)
    def diagonal_move(self):
        return self.move_validator(
            [PieceType.BISHOP, PieceType.QUEEN, PieceType.KING],
            lambda: abs(self._move_vector.x) == abs(self._move_vector.y))

    @validator(ValidatorTypes.ALLOW)
    def knight_move(self):
        length = self._move_vector.length
        return self.move_validator([PieceType.KNIGHT],
                                   lambda: length == np.math.sqrt(5))

    @validator(ValidatorTypes.ALLOW)
    def pawn_capture_piece(self):
        target = self._current_map.get(self._move_vector.end_cell)
        x = self._move_vector.x
        y = self._move_vector.y

        return abs(x) == abs(y) == 1 and target is not None

    def move_validator(self, apply_for_piece_types, condition):
        if self._active_piece.type not in apply_for_piece_types:
            return False

        return condition()
