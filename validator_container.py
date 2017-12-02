from abstract_validators_container import *
from allow_validators_container import AllowValidatorsContainer
from prohibit_validators_container import ProhibitValidatorsContainer


class ValidatorsContainer(AbstractValidatorsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self):
        arguments = [self._current_map, self._previous_map, self._move_vector]

        allow_result = AllowValidatorsContainer(*arguments).is_valid()
        prohibit_result = ProhibitValidatorsContainer(*arguments).is_valid()

        return allow_result and prohibit_result
