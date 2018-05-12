import pickle


class GameManager:
    @staticmethod
    def save_game(game, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(game, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_game(file_name):
        with open(file_name, "rb") as file:
            return pickle.load(file)
