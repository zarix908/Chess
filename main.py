from kivy import Config
from kivy.clock import Clock

from game import Game
from root_window import RootWindow

Config.set('graphics', 'resizable', False)

from kivy.app import App


class Chess(App):
    def build(self):
        game = Game()
        root_window = RootWindow(game)
        Clock.schedule_interval(lambda delta_time: root_window.update(),
                                0.03)
        return root_window


if __name__ == '__main__':
    Chess().run()


