from model.validators.abstract_validators_container import *
from model.validators.allow_validators_container import \
    AllowValidatorsContainer

from model.validators.prohibit_validators_container import \
    ProhibitValidatorsContainer


class ValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        arguments = [self._current_map, self._previous_map, self._move_vector,
                     self._current_move_color]

        allow_container = AllowValidatorsContainer(*arguments)
        prohibit_container = ProhibitValidatorsContainer(*arguments)

        allow_container.on_remove_piece_handler = self.on_remove_piece_handler
        prohibit_container\
            .on_check_enemy_king_handler = self.on_check_enemy_king_handler

        return allow_container.is_valid() and prohibit_container.is_valid()
