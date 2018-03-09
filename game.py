from game_state import GameState
from moves_getter import MovesGetter


class Game:
    def __init__(self):
        self.__moves_getter = MovesGetter()
        self.__current_state = GameState()

    def get_current_state(self):
        return self.__current_state

    def make_move(self, move):
        piece = self.__current_state.get(move.start_cell)
        moves = self.__moves_getter.get_moves(move.start_cell, piece.type)
        if move in moves:
            self.__current_state = GameState(self.__current_state, move)


