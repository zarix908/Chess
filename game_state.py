from cell import Cell
from enums import PieceType, PieceColor
from piece import Piece


class GameState:
    """Immutable class"""
    SIZE = 8

    def __init__(self, old_state=None, move=None):
        self.long_castling_available = True
        self.short_castling_available = True

        self.__pieces = {}
        self.__map = [[None for y in range(GameState.SIZE)]
                      for x in range(GameState.SIZE)]

        if old_state is None or move is None:
            self.set_initial_state()
        else:
            self.generate_new_state(old_state, move)

    def get_pieces(self, color):
        return dict((piece, cell) for piece, cell in self.__pieces.items() if
                    piece.color == color)

    def set_initial_state(self):
        self.add_pieces(PieceColor.WHITE)
        self.add_pieces(PieceColor.BLACK)

    def add_pieces(self, color):
        y = 0 if color is PieceColor.WHITE else GameState.SIZE - 1
        x = 0

        base_pieces = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                       PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                       PieceType.KNIGHT, PieceType.ROOK]

        for i in base_pieces:
            self.add_piece(Piece(i, color), x, y)
            x += 1

        y = 1 if color is PieceColor.WHITE else GameState.SIZE - 2
        for x in range(GameState.SIZE):
            self.add_piece(Piece(PieceType.PAWN, color), x, y)

    def get(self, cell):
        if cell is None:
            return None

        if not (0 <= cell.x < GameState.SIZE and 0 <= cell.y < GameState.SIZE):
            return None

        piece = self.__map[cell.x][cell.y]
        return None if piece is None else Piece(piece.type, piece.color)

    def generate_new_state(self, old_state, move):
        self.short_castling_available = old_state.short_castling_available
        self.long_castling_available = old_state.long_castling_available

        for x in range(GameState.SIZE):
            for y in range(GameState.SIZE):
                cell = Cell(x, y)

                if cell == move.start_cell:
                    self.add_piece(None, x, y)
                elif cell == move.end_cell:
                    self.add_piece(old_state.get(move.start_cell), cell.x,
                                   cell.y)
                else:
                    piece = old_state.get(cell)
                    self.add_piece(piece, cell.x, cell.y)

        self.complete_castling(old_state, move)

    def add_piece(self, piece, x, y):
        self.__map[x][y] = piece
        if piece is not None:
            self.__pieces[piece] = Cell(x, y)

    def complete_castling(self, old_state, move):
        piece = old_state.get(move.start_cell)
        if piece.type is PieceType.KING and move.length == 2:
            x = 7 if move.x == 2 else 0
            new_x = 5 if move.x == 2 else 3
            y = 0 if piece.color is PieceColor.WHITE else 7
            self.add_piece(None, x, y)
            self.add_piece(Piece(PieceType.ROOK, piece.color), new_x, y)

    # TODO
    def __str__(self):
        result = ""
        for y in range(GameState.SIZE):
            for x in range(GameState.SIZE):
                piece = self.__map[x][y]

                if piece is None:
                    result += "##"
                else:
                    result += str(int(piece.color)) + str(int(piece.type))

            result += "\n"

        return result
