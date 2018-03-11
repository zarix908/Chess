from post_filter import PostFilter
from predictive_filter import PredictiveFilter
from game_state import GameState
from moves_getter import MovesGetter


class Game:
    def __init__(self):
        self.__current_state = GameState()
        self.__moves = []

        self.__moves_getter = MovesGetter()
        self.__predict_filter = PredictiveFilter()
        self.__post_filter = PostFilter()
        self.__predict_filter.on_pass_capture = self.on_pass_capture

    def get_current_state(self):
        return self.__current_state

    def make_move(self, move):
        moves = self.get_possible_moves(move.start_cell)

        if move in moves:
            new_state = GameState(self.__current_state, move)
            new_state = self.__post_filter.filter(new_state, move)

            if new_state is not None:
                self.__current_state = new_state
                self.__moves.append(move)

    def get_possible_moves(self, cell):
        piece = self.__current_state.get(cell)
        moves = self.__moves_getter.get_moves(cell, piece.type, piece.color)
        moves = self.__predict_filter.filter(self.__current_state, moves,
                                             self.get_last_move(), piece.type)
        return moves

    def get_last_move(self):
        return self.__moves[-1] if len(self.__moves) > 0 else None

    def on_pass_capture(self, cell):
        pass
