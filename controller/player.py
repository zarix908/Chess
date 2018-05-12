from enums import PlayerType


class Player:
    def __init__(self, color, controller, ai):
        self.__color = color
        self.__controller = controller
        self.__ai = ai
        controller.move_complete.append(self.move_complete_event)

    @property
    def type(self):
        return PlayerType.HUMAN if self.__ai is None else PlayerType.AI

    def move_complete_event(self, color):
        if self.__color != color and self.__ai is not None:
            self.__controller.make_move(self.__ai.get_move(self.__color))

    def move_receive_from_ui_handler(self, move):
        self.__controller.make_move(move)
