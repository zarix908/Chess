from cell import Cell
from enums import PieceType
from vector import Vector
import numpy as np


class Filter:
    def __init__(self):
        pass

    def filter(self, game_state, moves, last_move, piece_type):
        moves = filter(lambda move: not self.has_let(game_state, move), moves)
        moves = filter(lambda move: not self.capture_self(game_state, move),
                       moves)

        if piece_type is PieceType.PAWN:
            moves = filter(
                lambda move: not self.pawn_capture_empty(game_state, move,
                                                         last_move), moves)
        return moves

    def has_let(self, game_state, move):
        if game_state.get(move.start_cell).type is PieceType.KNIGHT:
            return False

        vector = Vector(np.sign(move.x), np.sign(move.y))
        cell = Cell(move.start_cell.x + vector.x, move.start_cell.y + vector.y)

        while cell != move.end_cell and self.on_board(cell):
            if game_state.get(cell) is not None:
                return True
            cell = Cell(cell.x + vector.x, cell.y + vector.y)

        return False

    def capture_self(self, game_state, move):
        piece = game_state.get(move.start_cell)
        target = game_state.get(move.end_cell)

        if target is None:
            return False

        return piece.color == target.color

    def pawn_capture_empty(self, game_state, move, last_move):
        target = game_state.get(move.end_cell)

        if move.x == 0 or target is not None:
            return False

        


    def on_board(self, cell):
        return 0 <= cell.x < 8 and 0 <= cell.y < 8
