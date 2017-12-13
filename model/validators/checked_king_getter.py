from enums import PieceType, PieceColor
from model.map import Map
from model.piece import Piece
from model.validators.cell_bit_determinant import CellBitDeterminant


class CheckedKingGetter:
    def __init__(self, current_map):
        self.__current_map = current_map

    def get_checked_king(self):
        cell_bit_determinant = CellBitDeterminant(self.__current_map)
        return cell_bit_determinant.get_bit_piece_from(
            list(self.__get_kings_cells()))

    def __get_kings_cells(self):
        for color in PieceColor:
            sought_piece = Piece(PieceType.KING, color)
            yield Map.find(self.__current_map, sought_piece)
