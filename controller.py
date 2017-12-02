class Controller:
    def __init__(self, game):
        self.__game = game

    def send_data(self, *data):
        return self.__game.try_make_move(data[0])
