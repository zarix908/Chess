from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from model.map import Map
from model.vector import Vector

from model.cell import Cell


class GameBoard(Widget):
    CELL_SIZE = 70
    PIECE_SIZE = 60

    game = ObjectProperty(None)
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__allotted_cell = None
        self.on_message_send_handler = None

        self.undo_map_available_handler = None
        self.redo_map_available_handler = None

    def update(self):
        self.send_to_root_window()

        with self.canvas:
            self.canvas.clear()
            Rectangle(pos=(0, 0), size=self.size,
                      source="assets/chessboard.png")
            self.draw_pieces_on_board()
            self.draw_rectangle_around_allotted_cell()

    def draw_rectangle_around_allotted_cell(self):
        if self.__allotted_cell is None:
            return

        x = self.__allotted_cell.x
        y = self.__allotted_cell.y

        if x > 7 or y > 7:
            return

        Color(1, 0, 0, 1)
        x *= GameBoard.CELL_SIZE
        y *= GameBoard.CELL_SIZE

        points = [x, y,
                  x + GameBoard.CELL_SIZE, y,
                  x + GameBoard.CELL_SIZE, y + GameBoard.CELL_SIZE,
                  x, y + GameBoard.CELL_SIZE,
                  x, y]

        Line(points=points, width=2)

    def draw_pieces_on_board(self):
        game_map = self.game.map

        for x in range(Map.SIZE):
            for y in range(Map.SIZE):
                piece = game_map.get(Cell(x, y))
                offset = (GameBoard.CELL_SIZE - GameBoard.PIECE_SIZE) / 2

                if piece is not None:
                    Rectangle(pos=(x * GameBoard.CELL_SIZE + offset,
                                   y * GameBoard.CELL_SIZE + offset),
                              size=(GameBoard.PIECE_SIZE,) * 2,
                              source=piece.asset_path)

    def on_touch_down(self, touch):
        if touch.device != 'mouse':
            return

        clicked_cell = Cell(int(touch.x // GameBoard.CELL_SIZE),
                            int(touch.y // GameBoard.CELL_SIZE))

        if self.__allotted_cell is None:
            self.__allotted_cell = clicked_cell
            return

        move_made = self.game.try_make_move(
            Vector(self.__allotted_cell, clicked_cell))
        self.__allotted_cell = None if move_made else clicked_cell

    def send_to_root_window(self):
        message = self.generate_message()

        self.on_message_send_handler(message)

        self.undo_map_available_handler(self.game.undo_map_available)
        self.redo_map_available_handler(self.game.redo_map_available)

    def generate_message(self):
        message = ""

        if self.game.king_is_checked:
            message = "Check!"
        elif self.game.is_finished:
            message = "Mate!"

        return message
