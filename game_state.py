from cell import Cell
from enums import PieceType, PieceColor
from piece import Piece


class GameState:
    SIZE = 8

    def __init__(self, old_state=None, move=None):
        self.__map = [[None for y in range(GameState.SIZE)]
                      for x in range(GameState.SIZE)]

        if old_state is None or move is None:
            self.set_initial_state()
        else:
            self.generate_new_state(old_state, move)

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
            self.__map[x][y] = Piece(i, color)
            x += 1

        y = 1 if color is PieceColor.WHITE else GameState.SIZE - 2
        for x in range(GameState.SIZE):
            self.__map[x][y] = Piece(PieceType.PAWN, color)

    def get(self, cell):
        if cell is None:
            return None

        if not (0 <= cell.x < GameState.SIZE and 0 <= cell.y < GameState.SIZE):
            return None

        piece = self.__map[cell.x][cell.y]
        return None if piece is None else Piece(piece.type, piece.color)

    def generate_new_state(self, old_state, move):
        for x in range(GameState.SIZE):
            for y in range(GameState.SIZE):
                cell = Cell(x, y)

                if cell == move.start_cell:
                    self.__map[cell.x][cell.y] = None
                elif cell == move.end_cell:
                    self.__map[cell.x][cell.y] = old_state.get(move.start_cell)
                else:
                    self.__map[cell.x][cell.y] = old_state.get(cell)

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
