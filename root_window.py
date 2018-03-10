from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.widget import Widget
from cell import Cell
from game_state import GameState
from move import Move
from moves_getter import MovesGetter


class RootWindow(Widget):
    CELL_SIZE = 70
    PIECE_SIZE = 60

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)

        side = GameState.SIZE * RootWindow.CELL_SIZE
        size = (side, side)
        Window.size = self.size = size

        self.__moves_getter = MovesGetter()
        self.__game = game
        self.__allotted_cell = None
        self.on_message_send_handler = None

        self.undo_map_available_handler = None
        self.redo_map_available_handler = None

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

        x = self.__allotted_cell.x
        y = self.__allotted_cell.y

        if x > 7 or y > 7:
            return

        Color(1, 0, 0, 1)
        x *= RootWindow.CELL_SIZE
        y *= RootWindow.CELL_SIZE

        points = [x, y,
                  x + RootWindow.CELL_SIZE, y,
                  x + RootWindow.CELL_SIZE, y + RootWindow.CELL_SIZE,
                  x, y + RootWindow.CELL_SIZE,
                  x, y]

        Line(points=points, width=2)

        active_piece = self.__game.get_current_state().get(
            self.__allotted_cell)

        if active_piece is None:
            return

        for move in self.__game.get_possible_moves(self.__allotted_cell):
            x = move.end_cell.x
            y = move.end_cell.y

            if x > 7 or y > 7:
                continue

            Color(0.4, 0.9, 0.4, 0.4)

            x *= RootWindow.CELL_SIZE
            y *= RootWindow.CELL_SIZE

            Rectangle(pos=(x, y), size=(RootWindow.CELL_SIZE,) * 2)

    def draw_pieces_on_board(self):
        game_map = self.__game.get_current_state()

        for x in range(8):
            for y in range(8):
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

        if self.__allotted_cell != clicked_cell:
            if self.__game.get_current_state().get(
                    Cell(self.__allotted_cell.x,
                         self.__allotted_cell.y)) is not None:
                self.__game.make_move(Move(self.__allotted_cell, clicked_cell))

            self.__allotted_cell = clicked_cell
        else:
            self.__allotted_cell = None
