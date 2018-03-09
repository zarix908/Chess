from enum import Enum


class PieceType(Enum):
    ROOK = 0
    KNIGHT = 1
    BISHOP = 2
    KING = 3
    QUEEN = 4
    PAWN = 5

    def __str__(self):
        return self._name_

    def __int__(self):
        return self._value_


class PieceColor(Enum):
    BLACK = 0
    WHITE = 1

    def __str__(self):
        return self._name_

    def __int__(self):
        return self._value_
