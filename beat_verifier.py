from attacking_moves_getter import AttackingMovesGetter


class BeatVerifier:
    def __init__(self):
        self.__attacking_moves_getter = AttackingMovesGetter()

    def is_beaten_cell(self, game_state, evil_color, cell):
        moves = self.__attacking_moves_getter.get_moves(game_state, evil_color,
                                                        cell)
        for _ in moves:
            return True

        return False
