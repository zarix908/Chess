from copy import copy

from enums import PieceColor
from model.map import Map
from model.map_cvs import MapCVS
from model.validators.checked_king_getter import CheckedKingGetter
from model.validators.move_validator import MoveValidator


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__color_current_move = PieceColor.WHITE
        self.__checked_king = CheckedKingGetter(self.map).get_checked_king()
        self.__game_is_finished = False
        self.__map_cvs = MapCVS()
        self.__map_cvs.add_map(self.map)

    def try_make_move(self, move_vector):
        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        self.__checked_king = None

        move_validator = MoveValidator(self.map,
                                       self.__map_cvs.previous_map(),
                                       move_vector,
                                       self.__color_current_move)

        move_validator.on_remove_piece_handler = self.on_remove_piece_handler

        if move_validator.is_valid():
            self.__checked_king = self.identify_checked_king(self.map,
                                                             move_vector)
            if not self.self_color_king_checked_after_move():
                self.invert_color_current_move()
                self.__map.drag(move_vector)
                self.__map_cvs.add_map(self.map)
                return True

        # self.detect_end_game()

        return False

    @property
    def map(self):
        return copy(self.__map)

    @property
    def king_is_checked(self):
        return self.__checked_king is not None

    @property
    def is_finished(self):
        return self.__game_is_finished

    @property
    def undo_map_available(self):
        return self.__map_cvs.undo_map_available

    @property
    def redo_map_available(self):
        return self.__map_cvs.redo_map_available

    def on_remove_piece_handler(self, piece_cell):
        self.__map.remove(piece_cell)

    def invert_color_current_move(self):
        self.__color_current_move = PieceColor.invert(
            self.__color_current_move)

    def identify_checked_king(self, map, move_vector):
        map.drag(move_vector)
        return CheckedKingGetter(map).get_checked_king()

    def self_color_king_checked_after_move(self):
        if self.__checked_king is None:
            return False

        return self.__checked_king.color == self.__color_current_move

    def undo_map(self):
        self.invert_color_current_move()
        self.__map = self.__map_cvs.undo_map()

    def redo_map(self):
        self.invert_color_current_move()
        self.__map = self.__map_cvs.redo_map()
