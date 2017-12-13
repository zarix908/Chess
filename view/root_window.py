from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.widget import Widget

from model.map import Map
from view.board import Board


class RootWindow(Widget):
    def __init__(self, game, controller):
        super().__init__()
        side = Map.SIZE * Board.CELL_SIZE
        size = (side + 240, side)
        Window.size = self.size = size

        layout = BoxLayout(size=self.size)

        board = Board(game, controller, size=size, size_hint_x=0.7)
        board.on_message_send_handler = self.on_message_send_handler
        Clock.schedule_interval(lambda delta_time: board.update(), 0.03)

        self.__message_label = Label(text="Hello, World", color=(1, 0, 0, 1),
                                     size_hint_x=0.3)

        layout.add_widget(board)
        layout.add_widget(self.__message_label)

        self.add_widget(layout)

    def on_message_send_handler(self, message):
        self.__message_label.text = message
