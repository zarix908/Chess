from model.cell_attack_moves_getter import CellAttackMovesGetter


class CellBeatVerifier:
    def __init__(self):
        self.__cell_attack_moves_getter = CellAttackMovesGetter()

    def is_beaten_cell(self, game_state, evil_color, cell):
        moves = self.__cell_attack_moves_getter.get_moves(game_state, evil_color,
                                                          cell)
        for _ in moves:
            return True

        return False
