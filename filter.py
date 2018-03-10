from cell import Cell
from enums import PieceType
from vector import Vector
import numpy as np


class Filter:
    def __init__(self):
        self.on_pass_capture = None

    def filter(self, game_state, moves, last_move, piece_type):
        moves = filter(lambda move: not self.has_let(game_state, move), moves)
        moves = filter(lambda move: not self.is_capture_self(game_state, move),
                       moves)

        if piece_type is PieceType.PAWN:
            moves = filter(
                lambda move: not self.is_pawn_capture_empty(game_state, move,
                                                            last_move), moves)

        return moves

    def has_let(self, game_state, move):
        piece_type = game_state.get(move.start_cell).type
        if piece_type is PieceType.KNIGHT:
            return False

        vector = Vector(np.sign(move.x), np.sign(move.y))
        cell = Cell(move.start_cell.x + vector.x, move.start_cell.y + vector.y)

        while cell != move.end_cell and self.on_board(cell):
            if game_state.get(cell) is not None:
                return True
            cell = Cell(cell.x + vector.x, cell.y + vector.y)

        if piece_type is PieceType.PAWN and cell == move.end_cell:
            if game_state.get(move.end_cell) is not None:
                return True

        return False

    def is_capture_self(self, game_state, move):
        piece = game_state.get(move.start_cell)
        target = game_state.get(move.end_cell)

        if target is None:
            return False

        return piece.color == target.color

    def is_pawn_capture_empty(self, game_state, move, last_move):
        target = game_state.get(move.end_cell)

        if move.x == 0 or target is not None:
            return False

        return not self.is_pass_capture(game_state, move, last_move)

    def is_pass_capture(self, game_state, move, last_move):
        if last_move is None:
            return False

        if game_state.get(last_move.end_cell).type is not PieceType.PAWN:
            return False

        if last_move.length != 2:
            return False

        dx = last_move.end_cell.x - move.start_cell.x
        dy = last_move.end_cell.y - move.start_cell.y

        if dx != move.x or dy != 0:
            return False

        self.on_pass_capture(last_move.end_cell)
        return True

    def on_board(self, cell):
        return 0 <= cell.x < 8 and 0 <= cell.y < 8
