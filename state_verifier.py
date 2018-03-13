from beat_verifier import BeatVerifier
from cell import Cell
from enums import PieceType, PieceColor


class StateVerifier:
    def __init__(self):
        self.__beat_verifier = BeatVerifier()

    def verify(self, game_state, move):
        return not (self.king_checked_after_move(game_state, move) or
                    self.is_beaten_castling(game_state, move))

    def king_checked_after_move(self, game_state, move):
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
        return king_checked

    def is_beaten_castling(self, game_state, move):
        moved_piece = game_state.get(move.end_cell)
        if moved_piece.type is not PieceType.KING:
            return False

        if move.length != 2:
            return False

        piece = game_state.get(move.end_cell)
        evil_color = PieceColor.invert(piece.color)

        y = move.start_cell.y
        cells = [Cell(i, y) for i in range(4, 7)] if move.length == 2 else [
            Cell(j, y) for j in reversed(range(2, 5))]

        for cell in cells:
            if self.__beat_verifier.is_beaten_cell(game_state, evil_color,
                                                   cell):
                return True

        return False
