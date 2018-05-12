from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class SaveGameDialog(FloatLayout):
    save = ObjectProperty(None)