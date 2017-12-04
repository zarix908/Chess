from copy import copy

from model.map import Map
from model.validators.validators_container import ValidatorsContainer


class Game:
    def __init__(self):
        self.__map = Map(is_auto_init=True)
        self.__map_stack = []

    def try_make_move(self, move_vector):
        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        validator_container = ValidatorsContainer(self.map,
                                                  self.get_map_stack(),
                                                  move_vector)

        validator_container\
            .on_remove_piece_handler = self.on_remove_piece_handler

        if validator_container.is_valid():
            self.__map_stack.append(copy(self.__map))
            self.__map.drag(move_vector)
            return True

        return False

    @property
    def map(self):
        return self.__map

    def get_map_stack(self):
        return None if len(self.__map_stack) < 1 else self.__map_stack[-1]

    def on_remove_piece_handler(self, piece_cell):
        self.__map.remove(piece_cell)
