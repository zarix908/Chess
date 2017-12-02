import inspect



def validator(func):
    def validator_decorator(*args, **kwargs):
        return func(*args, **kwargs)

    validator_decorator.__doc__ = "validator"
    return validator_decorator


class AbstractValidatorsContainer:
    def __init__(self, current_map, previous_map, move_vector):
        self._current_map = current_map
        self._previous_map = previous_map
        self._move_vector = move_vector
        self._active_piece = self._current_map.get(
            self._move_vector.start_cell)

    def is_valid(self):
        raise NotImplementedError("method is_valid() not declared in subclass")

    def moving_validator(self, apply_for_piece_types, condition):
        if self._active_piece.type not in apply_for_piece_types:
            return False

        return condition()

    def get_validators(self):
        class_members = map(lambda el: el[1], inspect.getmembers(self))

        for member in class_members:
            if member.__doc__ == "validator":
                yield member
