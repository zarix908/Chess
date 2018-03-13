import pickle


class MovesGetter:
    def __init__(self):
        with open('moves.pickle', 'rb') as file:
            self.__moves = pickle.load(file)

    def get_moves(self, cell, piece_type, color):
        return self.__moves[cell][piece_type][color]
