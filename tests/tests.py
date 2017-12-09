import unittest

from model.cell import Cell
from model.game import Game
from model.vector import Vector


class GameTest(unittest.TestCase):
    def test_main(self):
        self.__number = 0

        game = Game()
        self.base_test(game, 4, 1, 4, 4, False)
        self.base_test(game, 4, 4, 4, 6, False)
        self.base_test(game, 4, 6, 4, 3, False)
        self.base_test(game, 4, 3, 4, 1, False)
        self.base_test(game, 4, 1, 4, 3, True)
        self.base_test(game, 4, 6, 4, 4, True)
        self.base_test(game, 3, 0, 7, 4, True)
        self.base_test(game, 1, 7, 2, 5, True)
        self.base_test(game, 7, 4, 4, 4, True)
        self.base_test(game, 5, 6, 5, 5, False)
        self.base_test(game, 5, 5, 6, 7, False)
        self.base_test(game, 6, 7, 4, 6, True)
        self.base_test(game, 4, 4, 4, 6, True)
        self.base_test(game, 5, 7, 4, 6, True)
        self.base_test(game, 4, 3, 4, 2, False)

        game = Game()
        self.base_test(game, 0, 1, 0, 3, True)
        self.base_test(game, 6, 7, 5, 5, True)
        self.base_test(game, 0, 3, 0, 4, True)
        self.base_test(game, 1, 6, 1, 4, True)
        self.base_test(game, 0, 4, 1, 5, True)
        self.base_test(game, 2, 6, 1, 5, True)

    def base_test(self, game, x1, y1, x2, y2, result):
        self.__number += 1

        start_cell = Cell(x1, y1)
        end_cell = Cell(x2, y2)

        self.assertEqual(game.try_make_move(Vector(start_cell, end_cell)),
                         result)


if __name__ == '__main__':
    unittest.main()
