from enums import PieceType
from enums import PieceColor
from piece import Piece


class Map:
    SIZE = 8

    def __init__(self):
        self.__map = None
        self.set_initial_state()

    def set_initial_state(self):
        self.__map = [[None for y in range(Map.SIZE)]
                      for x in range(Map.SIZE)]

        self.add_pieces(PieceColor.WHITE)
        self.add_pieces(PieceColor.BLACK)

    def add_pieces(self, color):
        y = 0 if color is PieceColor.WHITE else Map.SIZE - 1
        x = 0

        base_pieces = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                       PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                       PieceType.KNIGHT, PieceType.ROOK]

        for i in base_pieces:
            self.__map[x][y] = Piece(i, color)
            x += 1

        y = 1 if color is PieceColor.WHITE else Map.SIZE - 2
        for x in range(Map.SIZE):
            self.__map[x][y] = Piece(PieceType.PAWN, color)

    def get(self, cell):
        if cell is not None and max(abs(cell.x), abs(cell.y)) < Map.SIZE:
            return self.__map[cell.x][cell.y]
        else:
            return None

    def drag(self, move_vector):
        start_cell = move_vector.start_cell
        end_cell = move_vector.end_cell

        self.__map[end_cell.x][end_cell.y] = self.__map[start_cell.x][
            start_cell.y]
        self.__map[start_cell.x][start_cell.y] = None

    def clone(self):
        pass

    def __str__(self):
        result = ""
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                piece = self.__map[x][y]

                if piece is None:
                    result += "##"
                else:
                    result += str(int(piece.color)) + str(int(piece.type))
