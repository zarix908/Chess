import inspect

from enums import ValidatorTypes


def validator(validator_type):
    def decorator(func):
        def validator_decorator(*args, **kwargs):
            return func(*args, **kwargs)

        validator_decorator.__doc__ = validator_type
        return validator_decorator

    return decorator


class AbstractValidatorsContainer:
    def __init__(self, current_map, move_vector):
        self._current_map = current_map
        self._move_vector = move_vector
        self._active_piece = self._current_map.get(
            self._move_vector.start_cell)

        self.on_remove_piece_handler = None

    def is_valid(self):
        return self.allow_valid() and self.prohibit_valid()

    def allow_valid(self):
        for allow_validator in self.get_validators_by_type(
                ValidatorTypes.ALLOW):
            if allow_validator():
                return True

        return False

    def prohibit_valid(self):
        for prohibit_validator in self.get_validators_by_type(
                ValidatorTypes.PROHIBIT):
            if prohibit_validator():
                return False

        return True

    def get_validators_by_type(self, validators_type):
        class_members = map(lambda el: el[1], inspect.getmembers(self))

        for member in class_members:
            if member.__doc__ == validators_type:
                yield member

    def notify_game_remove_piece(self, piece_cell):
        self.on_remove_piece_handler(piece_cell)
