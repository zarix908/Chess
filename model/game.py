from copy import copy

from enums import PieceColor
from model.cell import Cell
from model.map import Map
from model.validators.checked_king_getter import CheckedKingGetter
from model.validators.move_validator import MoveValidator
from model.validators.trajectory_validators_container import \
    TrajectoryValidatorsContainer
from model.vector import Vector


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__maps_stack = []
        self.__color_current_move = PieceColor.WHITE
        self.__checked_king = CheckedKingGetter(self.map).get_checked_king()
        self.__game_is_finished = False

    def try_make_move(self, move_vector):
        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        self.__checked_king = None

        move_validator = MoveValidator(self.map,
                                       self.pop_maps_stack(),
                                       move_vector,
                                       self.__color_current_move)

        move_validator.on_remove_piece_handler = self.on_remove_piece_handler

        if move_validator.is_valid():
            self.__checked_king = self.identify_checked_king(self.map,
                                                             move_vector)

            if not self.self_color_king_checked_after_move():
                self.invert_color_current_move()
                self.__maps_stack.append(self.map)
                self.__map.drag(move_vector)
                return True

        #self.detect_end_game()

        return False

    @property
    def map(self):
        return copy(self.__map)

    @property
    def king_is_checked(self):
        return self.__checked_king is not None

    @property
    def game_is_finished(self):
        return self.__game_is_finished

    def pop_maps_stack(self):
        return None if len(self.__maps_stack) < 1 else copy(
            self.__maps_stack[-1])

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

    """def detect_end_game(self):
        if self.__checked_king is None:
            return

        local_map = self.map
        enemy_king_cell = Map.find(local_map, self.__checked_king)

        for x in range(-1, 2):
            for y in range(-1, 2):
                x_point = enemy_king_cell.x + x
                y_point = enemy_king_cell.y + y

                if not (0 < x_point < Map.SIZE and 0 < y_point < Map.SIZE):
                    continue

                target_cell = Cell(x_point, y_point)

                vector = Vector(enemy_king_cell, target_cell)

                trajectory_validator = TrajectoryValidatorsContainer(local_map,
                                                                     vector)

                if trajectory_validator.is_valid():
                    new_map = copy(local_map)
                    checked_king = self.identify_checked_king(new_map, vector)

                    if checked_king != self.__checked_king:
                        return

        self.__game_is_finished = True"""
