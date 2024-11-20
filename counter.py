from typing import Union, TypeVar

T = TypeVar('T', int, float, complex)


class Counter:
    def __init__(self, start: T):
        self.value = start

    def next(self) -> T:
        self.value += 1
        return self.value