import math

from enums import PieceType
from model.map import Map
from model.validators.abstract_validators_container import *


class AllowValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        return self.is_valid_trajectory() or self.is_valid_appendix_rules()

    def is_valid_trajectory(self):
        return self.is_valid_by_validators_type(ValidatorTypes.TRAJECTORY)

    def is_valid_appendix_rules(self):
        return self.is_valid_by_validators_type(ValidatorTypes.APPENDIX_RULES)

    def is_valid_by_validators_type(self, validators_type):
        for allow_validator in self.get_validators_by_type(validators_type):
            if allow_validator():
                return True

        return False

    @validator(ValidatorTypes.TRAJECTORY)
    def vertical_horizontal_move(self):
        x = self._move_vector.x
        y = self._move_vector.y
        length_in_cells = self._move_vector.length_in_cells
        return self.move_validator(
            [PieceType.ROOK, PieceType.QUEEN, PieceType.KING, PieceType.PAWN],
            lambda: (x == 0 or y == 0) and length_in_cells != 0)

    @validator(ValidatorTypes.TRAJECTORY)
    def diagonal_move(self):
        return self.move_validator(
            [PieceType.BISHOP, PieceType.QUEEN, PieceType.KING],
            lambda: abs(self._move_vector.x) == abs(self._move_vector.y))

    @validator(ValidatorTypes.TRAJECTORY)
    def knight_move(self):
        length = self._move_vector.length
        return self.move_validator([PieceType.KNIGHT],
                                   lambda: length == math.sqrt(5))

    @validator(ValidatorTypes.TRAJECTORY)
    def pawn_capture_piece(self):
        target = self._current_map.get(self._move_vector.end_cell)
        x = self._move_vector.x
        y = self._move_vector.y

        return abs(x) == abs(y) == 1 and target is not None

    @validator(ValidatorTypes.APPENDIX_RULES)
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
