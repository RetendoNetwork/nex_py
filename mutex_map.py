import threading
from typing import Callable, Dict, TypeVar, Optional

K = TypeVar('K')
V = TypeVar('V')


class MutexMap:
    def __init__(self):
        self._lock = threading.RLock()  # Using RLock for read-write locking
        self.real: Dict[K, V] = {}

    def set(self, key: K, value: V):
        with self._lock:
            self.real[key] = value

    def get(self, key: K) -> Optional[V]:
        with self._lock:
            return self.real.get(key)

    def get_or_set_default(self, key: K, create_default: Callable[[], V]) -> V:
        with self._lock:
            if key not in self.real:
                self.real[key] = create_default()
            return self.real[key]

    def has(self, key: K) -> bool:
        with self._lock:
            return key in self.real

    def delete(self, key: K):
        with self._lock:
            if key in self.real:
                del self.real[key]

    def delete_if(self, predicate: Callable[[K, V], bool]) -> int:
        with self._lock:
            amount = 0
            for key, value in list(self.real.items()):  # Create a copy of the keys for safe iteration
                if predicate(key, value):
                    del self.real[key]
                    amount += 1
            return amount

    def run_and_delete(self, key: K, callback: Callable[[K, V], None]):
        with self._lock:
            if key in self.real:
                value = self.real[key]
                callback(key, value)
                del self.real[key]

    def size(self) -> int:
        with self._lock:
            return len(self.real)

    def each(self, callback: Callable[[K, V], bool]) -> bool:
        with self._lock:
            for key, value in self.real.items():
                if callback(key, value):
                    return True
            return False

    def clear(self, callback: Optional[Callable[[K, V], None]] = None):
        with self._lock:
            for key, value in list(self.real.items()):  # Iterate over a copy of the items
                if callback:
                    callback(key, value)
                del self.real[key]