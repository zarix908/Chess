from copy import copy

from enums import PieceColor
from model.map import Map
from model.validators.checked_king_getter import CheckedKingGetter
from model.validators.move_validator import MoveValidator


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__maps_stack = []
        self.__color_current_move = PieceColor.WHITE
        self.__checked_king = CheckedKingGetter(self.map).get_checked_king()

    def try_make_move(self, move_vector):
        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        move_validator = MoveValidator(self.map,
                                       self.pop_maps_stack(),
                                       move_vector,
                                       self.__color_current_move)

        move_validator.on_remove_piece_handler = self.on_remove_piece_handler

        if move_validator.is_valid():
            if not self.self_color_king_checked_after_move(move_vector):
                self.invert_color_current_move()
                self.__maps_stack.append(self.map)
                self.__map.drag(move_vector)

                return True

        return False

    @property
    def map(self):
        return copy(self.__map)

    @property
    def king_is_checked(self):
        return copy(self.__checked_king)

    def pop_maps_stack(self):
        return None if len(self.__maps_stack) < 1 else copy(
            self.__maps_stack[-1])

    def on_remove_piece_handler(self, piece_cell):
        self.__map.remove(piece_cell)

    def invert_color_current_move(self):
        self.__color_current_move = PieceColor.invert(
            self.__color_current_move)

    def self_color_king_checked_after_move(self, move_vector):
        new_map = self.map
        new_map.drag(move_vector)
        checked_king = CheckedKingGetter(new_map).get_checked_king()

        if checked_king is None:
            return False

        return checked_king.color == self.__color_current_move
