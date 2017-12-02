from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.widget import Widget

from cell import Cell
from map import Map
from vector import Vector


class RootWindow(Widget):
    CELL_SIZE = 70
    PIECE_SIZE = 60

    def __init__(self, game, controller):
        super().__init__()

        self.__game = game
        self.__controller = controller
        Window.size = self.size = (Map.SIZE * RootWindow.CELL_SIZE,) * 2

        self.__allotted_cell = None

    def update(self):
        with self.canvas:
            self.canvas.clear()
            Rectangle(pos=(0, 0), size=self.size,
                      source="assets/chessboard.png")
            self.draw_pieces_on_board()
            self.draw_rectangle_around_allotted_cell()

    def draw_rectangle_around_allotted_cell(self):
        if self.__allotted_cell is None:
            return

        Color(1, 0, 0, 1)
        x = self.__allotted_cell.x * RootWindow.CELL_SIZE
        y = self.__allotted_cell.y * RootWindow.CELL_SIZE

        points = [x, y,
                  x + RootWindow.CELL_SIZE, y,
                  x + RootWindow.CELL_SIZE, y + RootWindow.CELL_SIZE,
                  x, y + RootWindow.CELL_SIZE,
                  x, y]

        Line(points=points, width=2)

    def draw_pieces_on_board(self):
        game_map = self.__game.map

        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                piece = game_map.get(Cell(x, y))
                offset = (RootWindow.CELL_SIZE - RootWindow.PIECE_SIZE) / 2

                if piece is not None:
                    Rectangle(pos=(x * RootWindow.CELL_SIZE + offset,
                                   y * RootWindow.CELL_SIZE + offset),
                              size=(RootWindow.PIECE_SIZE,) * 2,
                              source=piece.asset_path)

    def on_touch_down(self, touch):
        if touch.device != 'mouse':
            return

        clicked_cell = Cell(int(touch.x // RootWindow.CELL_SIZE),
                            int(touch.y // RootWindow.CELL_SIZE))

        if self.__allotted_cell is None:
            self.__allotted_cell = clicked_cell
            return

        move_made = self.__controller.send_data(
            Vector(self.__allotted_cell, clicked_cell))
        self.__allotted_cell = None if move_made else clicked_cell
