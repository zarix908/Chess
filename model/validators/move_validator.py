from model.validators.appendix_validators_container import \
    AppendixRulesValidatorsContainer

from model.validators.trajectory_validators_container import \
    TrajectoryValidatorsContainer


class MoveValidator:
    def __init__(self, current_map, previous_map, move_vector,
                 color_current_move):
        self.__current_map = current_map
        self.__move_vector = move_vector
        self.__previous_map = previous_map
        self.__color_current_move = color_current_move

        self.on_remove_piece_handler = None

    def is_valid(self):
        appendix_rules_container = AppendixRulesValidatorsContainer(
            self.__current_map,
            self.__previous_map,
            self.__move_vector,
            self.__color_current_move)

        trajectory_container = TrajectoryValidatorsContainer(
            self.__current_map,
            self.__move_vector)

        appendix_rules_container.on_remove_piece_handler = \
            self.on_remove_piece_handler

        allow_validators_result = trajectory_container.allow_valid() \
                                  or appendix_rules_container.allow_valid()

        prohibit_validators_result = trajectory_container.prohibit_valid() \
                            and appendix_rules_container.prohibit_valid()

        return allow_validators_result and prohibit_validators_result
