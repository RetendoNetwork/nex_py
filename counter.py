from typing import TypeVar, Union

T = TypeVar('T', bound=Union[int, float, complex])

class Counter:
    def __init__(self, start: T) -> None:
        self.value: T = start

    def next(self) -> T:
        self.value += 1
        return self.value