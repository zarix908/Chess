from kivy import Config
from view.menu_widget import MenuWidget

Config.set('graphics', 'resizable', False)

import kivy.app


class Chess(kivy.app.App):
    def build(self):
        return MenuWidget()


if __name__ == '__main__':
    Chess().run()
