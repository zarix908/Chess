from copy import copy

from enums import PieceColor
from model.cell import Cell
from model.map import Map
from model.map_cvs import MapCVS
from model.validators.checked_king_getter import CheckedKingGetter
from model.validators.move_validator import MoveValidator
from model.vector import Vector


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__color_current_move = PieceColor.WHITE
        self.__checked_king = CheckedKingGetter(self.map).get_checked_king()
        self.__is_finished = False
        self.__map_cvs = MapCVS()
        self.__map_cvs.add_map(self.map)
        self.__moved_pieces = []

    def try_make_move(self, move_vector):
        if self.__is_finished:
            return

        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        self.__checked_king = None

        move_validator = MoveValidator(self.map,
                                       self.__map_cvs.previous_map(),
                                       move_vector,
                                       self.__color_current_move,
                                       self.__moved_pieces)

        move_validator.on_remove_piece_handler = self.on_remove_piece_handler
        move_validator.on_castling_handler = self.on_castling_handler

        if move_validator.is_valid():
            self.__checked_king = Game.identify_checked_king(self.map,
                                                             move_vector)
            if not self.self_color_king_checked_after_move():
                self.__moved_pieces.append(piece)
                self.invert_color_current_move()
                self.__map.drag(move_vector)
                self.__map_cvs.add_map(self.map)
                # self.detect_end_game()
                return True

        return False

    @property
    def map(self):
        return copy(self.__map)

    @property
    def king_is_checked(self):
        return self.__checked_king is not None

    @property
    def is_finished(self):
        return self.__is_finished

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

    @staticmethod
    def identify_checked_king(map, move_vector):
        map.drag(move_vector)
        return CheckedKingGetter(map).get_checked_king()

    def self_color_king_checked_after_move(self):
        if self.__checked_king is None:
            return False

        return self.__checked_king.color == self.__color_current_move

    def undo(self):
        self.__moved_pieces.pop()
        self.invert_color_current_move()
        self.__map = self.__map_cvs.undo_map()

    def redo(self):
        self.__map = self.__map_cvs.redo_map()
        self.__moved_pieces.append(
            Map.get_last_move_vector(self.__map_cvs.previous_map(), self.map))
        self.invert_color_current_move()

    def detect_end_game(self):
        pass

    def on_castling_handler(self, color, is_short):
        y = 0 if color is PieceColor.WHITE else 7
        start_x = 7 if is_short else 0
        end_x = 5 if is_short else 3
        vector = Vector(Cell(start_x, y), Cell(end_x, y))
        self.__map.drag(vector)
