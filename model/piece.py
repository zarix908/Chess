from enums import PieceType


class Piece:
    Castle_id_for_rooks = 13

    def __init__(self, type, color):
        self.__type = type
        self.__color = color
        self.__asset_path = "assets/" + str(self.__type) + "_" + str(
            self.__color) + ".png"
        if type is PieceType.ROOK:
            self.__castle_id = Piece.Castle_id_for_rooks
            Piece.Castle_id_for_rooks += 1

    @property
    def type(self):
        return self.__type

    @property
    def color(self):
        return self.__color

    @property
    def asset_path(self):
        return self.__asset_path

    """def castle_id_equal(self, other):
        if self.__type is PieceType.ROOK and other.__type is PieceType.ROOK:
            return self.__castle_id != other.__castle_id
        else:
            raise TypeError("pieces types must be rook")"""

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False

        return self.__type == other.__type and self.__color == other.__color

    def __copy__(self):
        return Piece(self.__type, self.__color)

    def __hash__(self):
        castle_id = 0 if self.type is not PieceType.ROOK else self.__castle_id
        return int(self.__type) + int(self.__color) + castle_id
