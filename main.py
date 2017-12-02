from kivy import Config
from kivy.app import App
from kivy.clock import Clock

from controller import Controller

Config.set('graphics', 'resizable', False)

from game import Game
from root_window import RootWindow


class Chess(App):
    def build(self):
        game = Game()
        root_window = RootWindow(game, Controller(game))
        Clock.schedule_interval(lambda delta_time: root_window.update(), 0.3)
        return root_window


if __name__ == '__main__':
    Chess().run()
