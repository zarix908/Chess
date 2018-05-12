from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from model.game_manager import GameManager
from view.load_game_dialog import LoadGameDialog
from view.save_game_dialog import SaveGameDialog


class GameWidget(Widget):
    game_board_widget = ObjectProperty(None)

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.__popup = None
        self.__game = game

    def set_game_board(self, game_board_widget):
        self.remove_widget(self.game_board_widget)
        game_board_widget.size_hint_y = 0.9
        self.add_widget(game_board_widget)

    def on_save_game_press(self):
        content = SaveGameDialog(save=self.save_game)
        self.__popup = Popup(title="Save game", content=content,
                             size_hint=(0.9, 0.9))
        self.__popup.open()

    def save_game(self, file_name):
        GameManager.save_game(self.__game, file_name)
        self.__popup.dismiss()

    def on_load_game_press(self):
        content = LoadGameDialog(load=self.load_game)
        self.__popup = Popup(title="Load game", content=content,
                             size_hint=(0.9, 0.9))
        self.__popup.open()

    def load_game(self, file_name):
        game = GameManager.load_game(file_name)
        self.__game._Game__current_state = game._Game__current_state
        self.__game._Game__past_moves = game._Game__past_moves
        self.__game._Game__current_move_color = game._Game__current_move_color
        self.__popup.dismiss()
