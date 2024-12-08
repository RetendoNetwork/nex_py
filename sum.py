from typing import List, TypeVar


T = TypeVar('T', int, float)
O = TypeVar('O', int, float)

def sum(data: List[T]) -> O:
    result: O = 0 
    for b in data:
        result += O(b)
    return result