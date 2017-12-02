from validator_container import ValidatorsContainer
from map import Map


class Game:
    def __init__(self):
        self.__map = Map()
        self.__map_stack = []

    def try_make_move(self, move_vector):
        piece = self.__map.get(move_vector.start_cell)
        if piece is None:
            return False

        validators = ValidatorsContainer(self.map, self.get_map_stack(),
                                         move_vector)
        if validators.is_valid():
            self.__map.drag(move_vector)
            self.__map_stack.append(self.__map.clone())
            return True

        return False

    @property
    def map(self):
        return self.__map

    def get_map_stack(self):
        return None if len(self.__map_stack) < 1 else self.__map_stack[-1]
