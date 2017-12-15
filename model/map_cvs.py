from copy import copy


class MapCVS:
    def __init__(self):
        self.__stack = []
        self.__canceled_stack = []

    @property
    def undo_map_available(self):
        return len(self.__stack) > 1

    @property
    def redo_map_available(self):
        return len(self.__canceled_stack) > 0

    def undo_map(self):
        self.__canceled_stack.append(self.__stack.pop())
        return self.peek(self.__stack)

    def redo_map(self):
        res = self.__canceled_stack.pop()
        self.__stack.append(res)
        return res

    def previous_map(self):
        return None if len(self.__stack) < 2 else copy(self.__stack[-2])

    def peek(self, stack):
        return None if len(stack) < 1 else stack[-1]

    def add_map(self, map):
        self.__canceled_stack.clear()
        self.__stack.append(map)
