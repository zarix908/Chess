import math

from enums import PieceType, ValidatorTypes
from model.map import Map
from model.validators.abstract_validators_container import *


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

    @validator(ValidatorTypes.PROHIBIT)
    def current_color_move_satisfies(self):
        return self._active_piece.color != self.__color_current_move
