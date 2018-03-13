from itertools import chain

from moves_getter import MovesGetter
from predictive_filter import PredictiveFilter


class AttackingMovesGetter:
    def __init__(self):
        self.__moves_getter = MovesGetter()
        self.__filter = PredictiveFilter()

    def get_moves(self, game_state, evil_color, cell):
        pieces = game_state.get_pieces(evil_color)
        pieces_moves = {}

        for piece, it_cell in pieces.items():
            moves = self.__moves_getter.get_moves(it_cell, piece.type,
                                                  piece.color)
            pieces_moves[piece] = filter(lambda move: move.end_cell == cell,
                                         moves)

        all_moves = None
        for piece, moves in pieces_moves.items():
            moves = self.__filter.filter(game_state, moves, None, piece.type)
            all_moves = moves if all_moves is None else chain(all_moves, moves)

        return all_moves
