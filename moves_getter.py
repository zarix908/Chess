import pickle


class MovesGetter:
    def __init__(self):
        with open('data.pickle', 'rb') as file:
            self.__moves = pickle.load(file)

    def get_moves(self, cell, piece_type):
        return self.__moves[cell][int(piece_type)]
