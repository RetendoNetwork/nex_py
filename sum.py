from typing import List, TypeVar

T = TypeVar('T', bound=int)
O = TypeVar('O', bound=int)


def sum(data: List[T]) -> O:
    result: O = 0 
    for b in data:
        result += O(b)
    return result