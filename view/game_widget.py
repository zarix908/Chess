from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget


class GameWidget(Widget):
    game_board_widget = ObjectProperty(None)

    def set_game_board(self, game_board_widget):
        self.remove_widget(self.game_board_widget)
        game_board_widget.size_hint_y = 0.1
        self.add_widget(game_board_widget)
