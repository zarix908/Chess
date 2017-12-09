from copy import copy

from enums import PieceColor
from model.map import Map
from model.validators.validators_container import ValidatorsContainer


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__map_stack = []
        self.__color_current_move = PieceColor.WHITE
        self.__king_is_checked = False

    def try_make_move(self, move_vector):
        with open("log.txt", "a") as file:

            file.write("------------------------\n")  # DEBUG #TODO
            file.write(str(move_vector.start_cell.x) + " " +
                            str(move_vector.start_cell.y) + "\n")
            file.write(str(move_vector.end_cell.x) + " " +
                            str(move_vector.end_cell.y) + "\n")

            piece = self.__map.get(move_vector.start_cell)
            if piece is None:
                file.write(str(False) + "\n")
                file.write("------------------------\n")  # DEBUG #TODO
                return False

            validator_container = ValidatorsContainer(self.map,
                                                      self.get_map_stack(),
                                                      move_vector,
                                                      self.__color_current_move)

            validator_container \
                .on_remove_piece_handler = self.on_remove_piece_handler

            validator_container \
                .on_check_enemy_king_handler = self.on_check_enemy_king

            if validator_container.is_valid():
                self.__color_current_move = PieceColor.invert(
                    self.__color_current_move)
                self.__map_stack.append(copy(self.__map))
                self.__map.drag(move_vector)
                file.write(str(True) + "\n")
                file.write("------------------------\n")  # DEBUG #TODO
                return True

            file.write(str(False) + "\n")
            file.write("------------------------\n")  # DEBUG #TODO
            return False

    def stash_king_is_check(self):
        self.__king_is_checked = False

    @property
    def map(self):
        return self.__map

    @property
    def king_is_checked(self):
        return self.__king_is_checked

    def get_map_stack(self):
        return None if len(self.__map_stack) < 1 else self.__map_stack[-1]

    def on_remove_piece_handler(self, piece_cell):
        self.__map.remove(piece_cell)

    def on_check_enemy_king(self):
        self.__king_is_checked = True
