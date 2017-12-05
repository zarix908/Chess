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
    def __init__(self, current_map, previous_map, move_vector):
        self._current_map = current_map
        self._previous_map = previous_map
        self._move_vector = move_vector
        self._active_piece = self._current_map.get(
            self._move_vector.start_cell)

        self.on_remove_piece_handler = None

    def is_valid(self):
        raise NotImplementedError("method is_valid() not declared in subclass")

    def move_validator(self, apply_for_piece_types, condition):
        if self._active_piece.type not in apply_for_piece_types:
            return False

        return condition()

    def get_validators(self):
        for validator_type in ValidatorTypes.get_iterable_types():
            for i in self.get_validators_by_type(validator_type):
                yield i

    def get_validators_by_type(self, validators_type):
        class_members = map(lambda el: el[1], inspect.getmembers(self))

        for member in class_members:
            if member.__doc__ == validators_type:
                yield member

    def notify_game_remove_piece(self, piece_cell):
        self.on_remove_piece_handler(piece_cell)
