from model.piece import Piece
from model.vector import Vector

from enums import PieceColor
from enums import PieceType
from model.cell import Cell


class Map:
    SIZE = 8

    def __init__(self, is_auto_init):
        self.__map = [[None for y in range(Map.SIZE)]
                      for x in range(Map.SIZE)]

        if is_auto_init:
            self.set_initial_state()

    def set_initial_state(self):
        self.__add_pieces(PieceColor.WHITE)
        self.__add_pieces(PieceColor.BLACK)

    def __add_pieces(self, color):
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
        if cell is None:
            return None

        if not (0 <= cell.x < Map.SIZE and 0 <= cell.y < Map.SIZE):
            return None

        piece = self.__map[cell.x][cell.y]
        return None if piece is None else Piece(piece.type, piece.color)

    def drag(self, move_vector):
        start_cell = move_vector.start_cell
        end_cell = move_vector.end_cell

        self.__map[end_cell.x][end_cell.y] = self.__map[start_cell.x][
            start_cell.y]
        self.__map[start_cell.x][start_cell.y] = None

    def remove(self, cell):
        self.__map[cell.x][cell.y] = None

    def __copy__(self):
        new_map = Map(is_auto_init=False)

        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                new_map.__map[x][y] = self.get(Cell(x, y))

        return new_map

    def __str__(self):
        result = ""
        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                piece = self.__map[x][y]

                if piece is None:
                    result += "##"
                else:
                    result += str(int(piece.color)) + str(int(piece.type))

            result += "\n"

        return result

    @staticmethod
    def get_last_move_vector(previous_map, current_map):
        if not (isinstance(previous_map, Map) and isinstance(
                current_map, Map)):
            raise TypeError("arguments should be Map")

        begin_cell = None
        end_cell = None

        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                if previous_map.get(Cell(x, y)) == current_map.get(Cell(x, y)):
                    continue

                if current_map.get(Cell(x, y)) is None:
                    begin_cell = Cell(x, y)
                else:
                    end_cell = Cell(x, y)

        if begin_cell is None or end_cell is None:
            return None

        return Vector(begin_cell, end_cell)
