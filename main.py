from controller import Controller
from model.game import Game

from kivy import Config

Config.set('graphics', 'resizable', False)

from kivy.app import App
from view.root_window import RootWindow


class Chess(App):
    def build(self):
        game = Game()
        root_window = RootWindow(game, Controller(game))
        return root_window


if __name__ == '__main__':
    Chess().run()
