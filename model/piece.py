class Piece:
    def __init__(self, type, color):
        self.__type = type
        self.__color = color
        self.__asset_path = "assets/" + str(self.__type) + "_" + str(
            self.__color) + ".png"

    @property
    def type(self):
        return self.__type

    @property
    def color(self):
        return self.__color

    @property
    def asset_path(self):
        return self.__asset_path

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False

        return self.__type == other.__type and self.__color == other.__color

    def __copy__(self):
        return Piece(self.__type, self.__color)
