from beat_verifier import BeatVerifier
from enums import PieceType, PieceColor
from piece import Piece


class PostFilter:
    def __init__(self):
        self.__beat_verifier = BeatVerifier()

    def filter(self, game_state, move):
        piece = game_state.get(move.end_cell)
        pieces = game_state.get_pieces(piece.color)

        self_king_cell = None
        for piece, cell in pieces.items():
            if piece.type is PieceType.KING:
                self_king_cell = cell

        evil_color = PieceColor.invert(piece.color)

        king_checked = self.__beat_verifier.is_beaten_cell(game_state,
                                                           evil_color,
                                                           self_king_cell)
        return game_state if not king_checked else None
