from copy import copy
import numpy as np

from model.cell import Cell
from model.map import Map
from model.piece import Piece

from enums import PieceType, PieceColor
from model.ray import Ray
from model.validators.abstract_validators_container import *
from model.validators.allow_validators_container import \
    AllowValidatorsContainer
from model.vector import Vector


class ProhibitValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        return self.is_valid_trajectory() and self.is_valid_appendix_rules()

    def is_valid_trajectory(self):
        return self.is_valid_by_validators_type(ValidatorTypes.TRAJECTORY)

    def is_valid_appendix_rules(self):
        return self.is_valid_by_validators_type(ValidatorTypes.APPENDIX_RULES)

    def is_valid_by_validators_type(self, validator_types):
        for prohibit_validator in self.get_validators_by_type(validator_types):
            if prohibit_validator():
                return False

        return True

    @validator(ValidatorTypes.TRAJECTORY)
    def king_limit_move_length(self):
        length_in_cells = self._move_vector.length_in_cells
        return self.move_validator([PieceType.KING],
                                   lambda: length_in_cells != 1)

    @validator(ValidatorTypes.TRAJECTORY)
    def pawn_limit_move_length(self):
        piece = self._active_piece
        if piece.type is not PieceType.PAWN:
            return False

        critical_cell_y = 1 if piece.color is PieceColor.WHITE else 6

        return self._move_vector.length_in_cells > (
            2 if self._move_vector.start_cell.y == critical_cell_y else 1)

    @validator(ValidatorTypes.TRAJECTORY)
    def pawn_direction_move(self):
        piece = self._active_piece

        if piece.type != PieceType.PAWN:
            return False

        right_direction_y_value = 1 if piece.color is PieceColor.WHITE else -1
        return np.sign(self._move_vector.y) != right_direction_y_value

    @validator(ValidatorTypes.TRAJECTORY)
    def jump_across_pieces(self):
        if self._active_piece.type is PieceType.KNIGHT:
            return False

        ray = Ray(self._current_map, self._move_vector.ort_in_cells)
        near_piece_vector = ray.cast(lambda obj: isinstance(obj, Piece))

        if near_piece_vector is None:
            return False

        return not near_piece_vector.contain(self._move_vector)

    @validator(ValidatorTypes.TRAJECTORY)
    def pawn_capture_piece_by_vertical(self):
        if self._active_piece.type is not PieceType.PAWN:
            return False

        target_cell = self._move_vector.end_cell
        target = self._current_map.get(target_cell)

        return self._move_vector.x == 0 and target is not None

    @validator(ValidatorTypes.TRAJECTORY)
    def capture_self_color_piece(self):
        piece = self._active_piece
        target = self._current_map.get(self._move_vector.end_cell)

        if target is None:
            return False

        return piece.color == target.color

    @validator(ValidatorTypes.APPENDIX_RULES)
    def self_king_will_check_after_move(self):
        new_map = copy(self._current_map)
        new_map.drag(self._move_vector)

        return self.king_is_attacked_in_position(new_map,
                                                 self._active_piece.color)

    @validator(ValidatorTypes.APPENDIX_RULES)
    def current_color_move_satisfies(self):
        return self._active_piece.color != self._current_move_color

    def king_is_attacked_in_position(self, position, king_color):
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                cell = Cell(x, y)
                piece = position.get(cell)

                if piece is None or king_color == piece.color:
                    continue

                king_cell = self.find_king_by_color(self._active_piece.color)

                if self._active_piece.type is PieceType.KING:
                    king_cell = self._move_vector.end_cell

                if self._valid_trajectory(position, Vector(cell, king_cell)):
                    return True

        return False

    def _valid_trajectory(self, new_map, next_move_vector):
        arguments = [new_map, self._current_map, next_move_vector,
                     self._current_move_color]

        allow_container = AllowValidatorsContainer(*arguments)
        prohibit_container = ProhibitValidatorsContainer(*arguments)

        return allow_container.is_valid_trajectory() and prohibit_container \
            .is_valid_trajectory()

    def find_king_by_color(self, color):
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                cell = Cell(x, y)
                piece = self._current_map.get(cell)

                if piece is None:
                    continue

                if piece.type is PieceType.KING and piece.color == color:
                    return cell
