from filter import Filter
from moves_getter import MovesGetter


class BeatVerifier:
    def __init__(self):
        self.__moves_getter = MovesGetter()
        self.__filter = Filter()

    def is_beaten_cell(self, game_state, evil_color, cell):
        pieces = game_state.get_pieces(evil_color)
        pieces_moves = {}

        for piece, cell in pieces:
            moves = self.__moves_getter.get_moves(cell, piece.type,
                                                  piece.color)
            pieces_moves[piece] = map(lambda move: move.end_cell == cell,
                                      moves)

        for piece, moves in pieces_moves:
            moves = self.__filter.filter(game_state, moves, None, piece.type)
            for _ in moves:
                return True

        return False

    def get_moves(self, pieces):
        for piece, cell in pieces.items():
            yield self.__moves_getter.get_moves(cell, piece.type, piece.color)
