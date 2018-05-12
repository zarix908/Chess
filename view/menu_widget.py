from kivy.core.window import Window
from kivy.properties import ObjectProperty, Clock
from kivy.uix.widget import Widget

from controller.ai import AI
from controller.controller import Controller
from controller.player import Player
from enums import PieceColor, GameMode, PlayerType
from model.game import Game
from view.game_widget import GameWidget


class MenuWidget(Widget):
    start_button = ObjectProperty(None)
    human_vs_human_check_box = ObjectProperty(None)
    human_vs_ai_check_box = ObjectProperty(None)
    ai_vs_human_check_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (200, 200)

    def on_start_button_press(self):
        if self.start_button.last_touch.device != "mouse":
            return

        if self.human_vs_human_check_box.active:
            self.init_game(GameMode.HUMAN_VS_PERSON)
        elif self.ai_vs_human_check_box.active:
            self.init_game(GameMode.AI_VS_HUMAN)
        elif self.human_vs_ai_check_box.active:
            self.init_game(GameMode.HUMAN_VS_AI)
        else:
            raise NotImplementedError

    def init_game(self, mode):
        game = Game()
        controller = Controller(game)

        ai = AI(game)
        first_player = Player(PieceColor.WHITE, controller, ai if mode == GameMode.AI_VS_HUMAN else None)
        second_player = Player(PieceColor.BLACK, controller, ai if mode == GameMode.HUMAN_VS_AI else None)

        players = [first_player, second_player]

        root_window = GameWidget(game)
        for player in players:
            if player.type == PlayerType.HUMAN:
                root_window.move_receive_from_ui.append(player.move_receive_from_ui_handler)

        if first_player.type == PlayerType.AI:
            first_player.move_complete_event(PieceColor.BLACK)

        Clock.schedule_interval(lambda delta_time: root_window.update(),
                                0.03)

        self.clear_widgets()
        self.add_widget(root_window)
