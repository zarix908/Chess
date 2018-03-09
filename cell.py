class Cell:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def __hash__(self):
        return self.__x * 100 + self.__y
