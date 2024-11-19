from typing import TypeVar, List, Union

T = TypeVar('T', int, int)

def sum(data: List[T]) -> T:
    result = 0
    for b in data:
        result += b
    return result