import threading
from typing import List, TypeVar, Callable, Optional

# Define a generic type V
V = TypeVar('V')


class MutexSlice:
    def __init__(self):
        self._lock = threading.RLock()  # Using RLock for managing synchronization
        self.real: List[V] = []

    def add(self, value: V):
        """Adds a value to the list"""
        with self._lock:
            self.real.append(value)

    def delete(self, value: V) -> bool:
        """Removes the first occurrence of a value from the list"""
        with self._lock:
            for i, v in enumerate(self.real):
                if v == value:
                    self.real.pop(i)
                    return True
        return False

    def delete_all(self, value: V) -> bool:
        """Removes all occurrences of a value from the list"""
        with self._lock:
            new_list = [v for v in self.real if v != value]
            if len(new_list) < len(self.real):
                self.real = new_list
                return True
        return False

    def has(self, value: V) -> bool:
        """Checks if the value exists in the list"""
        with self._lock:
            return value in self.real

    def get_index(self, value: V) -> int:
        """Returns the index of the value in the list, or -1 if not found"""
        with self._lock:
            try:
                return self.real.index(value)
            except ValueError:
                return -1

    def at(self, index: int) -> Optional[V]:
        """Returns the value at the given index"""
        with self._lock:
            if 0 <= index < len(self.real):
                return self.real[index]
            return None

    def values(self) -> List[V]:
        """Returns the list of values"""
        with self._lock:
            return self.real.copy()

    def size(self) -> int:
        """Returns the size of the list"""
        with self._lock:
            return len(self.real)

    def each(self, callback: Callable[[int, V], bool]) -> bool:
        """Executes a callback function on each element of the list"""
        with self._lock:
            for index, value in enumerate(self.real):
                if callback(index, value):
                    return True
        return False

    def clear(self):
        """Removes all items from the list"""
        with self._lock:
            self.real.clear()