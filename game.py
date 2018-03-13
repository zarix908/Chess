from enums import PieceType
from post_filter import PostFilter
from predictive_filter import PredictiveFilter
from game_state import GameState
from moves_getter import MovesGetter


class Game:
    def __init__(self):
        self.__current_state = GameState()
        self.__past_moves = []
        self.__all_possible_moves = {}

        self.__moves_getter = MovesGetter()
        self.__post_filter = PostFilter()

        self.__predict_filter = PredictiveFilter()
        self.__predict_filter.on_pass_capture = self.on_pass_capture
        self.__predict_filter.on_castling = self.on_castling

    def get_current_state(self):
        return self.__current_state

    def make_move(self, move):
        moves = self.get_possible_moves(move.start_cell)

        if move in moves:
            self.castling_unavailable(move)

            new_state = GameState(self.__current_state, move)
            self.change_game_state(new_state, move)

    def change_game_state(self, new_state, last_move):
        self.__current_state = new_state
        self.__past_moves.append(last_move)
        del self.__all_possible_moves
        self.__all_possible_moves = {}

    def get_possible_moves(self, cell):
        if cell not in self.__all_possible_moves:
            self.generate_possible_moves(cell)

        return self.__all_possible_moves[cell]

    def generate_possible_moves(self, cell):
        piece = self.__current_state.get(cell)
        moves = self.__moves_getter.get_moves(cell, piece.type, piece.color)
        moves = self.__predict_filter.filter(self.__current_state, moves,
                                             self.get_last_move(), piece.type)

        moves = filter(lambda move: self.will_correct_state_after_move(move),
                       moves)

        self.__all_possible_moves[cell] = list(moves)

    def will_correct_state_after_move(self, move):
        game_state = GameState(self.__current_state, move)
        return self.__post_filter.filter(game_state, move) is not None

    def get_last_move(self):
        return self.__past_moves[-1] if len(self.__past_moves) > 0 else None

    def on_pass_capture(self, cell):
        pass

    def on_castling(self):
        pass

    def castling_unavailable(self, move):
        piece = self.__current_state.get(move.start_cell)
        if piece.type is PieceType.ROOK:
            if move.start_cell.x == 0:
                self.__current_state.long_castling_available = False
            elif move.start_cell.x == 7:
                self.__current_state.short_castling_available = False

        if piece.type is PieceType.KING:
            self.__current_state.short_castling_available = False
            self.__current_state.long_castling_available = False
