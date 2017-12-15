from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from model.map import Map
from view.game_board import GameBoard


class RootWindow(Widget):
    game = ObjectProperty(None)
    controller = ObjectProperty(None)
    game_board = ObjectProperty(None)
    undo_map_button = ObjectProperty(None)
    redo_map_button = ObjectProperty(None)
    message_label = ObjectProperty(None)

    def __init__(self, game, controller):
        super().__init__()

        side = Map.SIZE * GameBoard.CELL_SIZE
        size = (side + 240, side)
        Window.size = self.size = size

        self.game = game
        self.controller = controller

        self.undo_map_button.bind(on_press=self.undo_map)
        self.redo_map_button.bind(on_press=self.redo_map)

        self.game_board.undo_map_available_handler = self.on_undo_map_available
        self.game_board.redo_map_available_handler = self.on_redo_map_available
        self.game_board.on_message_send_handler = self.on_message_send

        Clock.schedule_interval(lambda delta_time: self.game_board.update(),
                                0.03)

    def undo_map(self, arg):
        if arg.last_touch.device == "mouse":
            self.game.undo_map()

    def redo_map(self, arg):
        if arg.last_touch.device == "mouse":
            self.game.redo_map()

    def on_undo_map_available(self, is_available):
        self.undo_map_button.disabled = not is_available

    def on_redo_map_available(self, is_available):
        self.redo_map_button.disabled = not is_available

    def on_message_send(self, message):
        self.message_label.text = message
