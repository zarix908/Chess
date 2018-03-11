from predictive_filter import PredictiveFilter
from moves_getter import MovesGetter


class BeatVerifier:
    def __init__(self):
        self.__moves_getter = MovesGetter()
        self.__filter = PredictiveFilter()

    def is_beaten_cell(self, game_state, evil_color, cell):
        pieces = game_state.get_pieces(evil_color)
        pieces_moves = {}

        for piece, it_cell in pieces.items():
            moves = self.__moves_getter.get_moves(it_cell, piece.type,
                                                  piece.color)
            pieces_moves[piece] = filter(lambda move: move.end_cell == cell,
                                         moves)

        for piece, moves in pieces_moves.items():
            moves = self.__filter.filter(game_state, moves, None, piece.type)
            for _ in moves:
                return True

        return False

    def get_moves(self, pieces):
        for piece, cell in pieces.items():
            yield self.__moves_getter.get_moves(cell, piece.type, piece.color)
