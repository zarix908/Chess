from enum import Enum


class GameMode:
    HUMAN_VS_PERSON = 0,
    HUMAN_VS_AI = 1,
    AI_VS_HUMAN = 2

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

    @staticmethod
    def invert(color):
        return PieceColor((int(color) + 1) % 2)

    def __str__(self):
        return self._name_

    def __int__(self):
        return self._value_


class PlayerType(Enum):
    AI = 0
    HUMAN = 1


class Flag(Enum):
    SHORT_CASTLING = 0
    LONG_CASTLING = 1
