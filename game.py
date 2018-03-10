from filter import Filter
from game_state import GameState
from moves_getter import MovesGetter


class Game:
    def __init__(self):
        self.__moves = []
        self.__moves_getter = MovesGetter()
        self.__current_state = GameState()

    def get_current_state(self):
        return self.__current_state

    def make_move(self, move):
        moves = self.get_possible_moves(move.start_cell)

        if move in moves:
            self.__current_state = GameState(self.__current_state, move)
            self.__moves.append(move)

    def get_possible_moves(self, cell):
        piece = self.__current_state.get(cell)
        moves = self.__moves_getter.get_moves(cell, piece.type, piece.color)
        moves = Filter().filter(self.__current_state, moves,
                                self.get_last_move(), piece.type)
        return moves

    def get_last_move(self):
        return self.__moves[-1] if len(self.__moves) > 0 else None
