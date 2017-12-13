from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from model.map import Map
from model.vector import Vector

from model.cell import Cell


class Board(Widget):
    CELL_SIZE = 70
    PIECE_SIZE = 60

    def __init__(self, game, controller, size, **kwargs):
        super().__init__(**kwargs)

        self.__game = game
        self.__controller = controller

        self.__allotted_cell = None

        self.on_message_send_handler = None

    def update(self):
        self.send_messages_to_root_window()

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
        x = self.__allotted_cell.x * Board.CELL_SIZE
        y = self.__allotted_cell.y * Board.CELL_SIZE

        points = [x, y,
                  x + Board.CELL_SIZE, y,
                  x + Board.CELL_SIZE, y + Board.CELL_SIZE,
                  x, y + Board.CELL_SIZE,
                  x, y]

        Line(points=points, width=2)

    def draw_pieces_on_board(self):
        game_map = self.__game.map

        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                piece = game_map.get(Cell(x, y))
                offset = (Board.CELL_SIZE - Board.PIECE_SIZE) / 2

                if piece is not None:
                    Rectangle(pos=(x * Board.CELL_SIZE + offset,
                                   y * Board.CELL_SIZE + offset),
                              size=(Board.PIECE_SIZE,) * 2,
                              source=piece.asset_path)

    def on_touch_down(self, touch):
        if touch.device != 'mouse':
            return

        clicked_cell = Cell(int(touch.x // Board.CELL_SIZE),
                            int(touch.y // Board.CELL_SIZE))

        if self.__allotted_cell is None:
            self.__allotted_cell = clicked_cell
            return

        move_made = self.__controller.send_data(
            Vector(self.__allotted_cell, clicked_cell))
        self.__allotted_cell = None if move_made else clicked_cell

    def send_messages_to_root_window(self):
        if self.__game.king_is_checked:
            self.on_message_send_handler("Check!")

        if self.__game.game_is_finished:
            self.on_message_send_handler("Mate!")
