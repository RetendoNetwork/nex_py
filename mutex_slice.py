import threading
from typing import List, TypeVar, Callable, Optional

V = TypeVar('V')


class MutexSlice:
    def __init__(self):
        self._lock = threading.RLock()
        self.real: List[V] = []

    def add(self, value: V):
        with self._lock:
            self.real.append(value)

    def delete(self, value: V) -> bool:
        with self._lock:
            for i, v in enumerate(self.real):
                if v == value:
                    self.real.pop(i)
                    return True
        return False

    def delete_all(self, value: V) -> bool:
        with self._lock:
            new_list = [v for v in self.real if v != value]
            if len(new_list) < len(self.real):
                self.real = new_list
                return True
        return False

    def has(self, value: V) -> bool:
        with self._lock:
            return value in self.real

    def get_index(self, value: V) -> int:
        with self._lock:
            try:
                return self.real.index(value)
            except ValueError:
                return -1

    def at(self, index: int) -> Optional[V]:
        with self._lock:
            if 0 <= index < len(self.real):
                return self.real[index]
            return None

    def values(self) -> List[V]:
        with self._lock:
            return self.real.copy()

    def size(self) -> int:
        with self._lock:
            return len(self.real)

    def each(self, callback: Callable[[int, V], bool]) -> bool:
        with self._lock:
            for index, value in enumerate(self.real):
                if callback(index, value):
                    return True
        return False

    def clear(self):
        with self._lock:
            self.real.clear()