from random import randint


class AI:
    def __init__(self, game):
        self.__game = game

    def get_move(self, for_color):
        game_state = self.__game.get_current_state()

        for piece, cell in game_state.get_pieces(for_color).items():
            moves = self.__game.get_possible_moves(cell)
            if len(moves) > 0:
                return moves[randint(0, len(moves) - 1)]

        raise NotImplementedError
