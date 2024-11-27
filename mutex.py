import threading
from typing import Dict, List, TypeVar, Callable, Optional, Any

V = TypeVar('V')


class MutexMap:
    def __init__(self):
        self._lock = threading.RLock()
        self._real: Dict[Any, Any] = {}

    def set(self, key: Any, value: Any):
        with self._lock:
            self._real[key] = value

    def get(self, key: Any) -> Optional[Any]:
        with self._lock:
            return self._real.get(key)

    def get_or_set_default(self, key: Any, create_default: Callable[[], Any]) -> Any:
        with self._lock:
            if key not in self._real:
                self._real[key] = create_default()
            return self._real[key]

    def has(self, key: Any) -> bool:
        with self._lock:
            return key in self._real

    def delete(self, key: Any):
        with self._lock:
            if key in self._real:
                del self._real[key]

    def delete_if(self, predicate: Callable[[Any, Any], bool]) -> int:
        with self._lock:
            amount = 0
            keys_to_delete = [key for key, value in self._real.items() if predicate(key, value)]
            for key in keys_to_delete:
                del self._real[key]
                amount += 1
            return amount

    def run_and_delete(self, key: Any, callback: Callable[[Any, Any], None]):
        with self._lock:
            if key in self._real:
                callback(key, self._real[key])
                del self._real[key]

    def size(self) -> int:
        with self._lock:
            return len(self._real)

    def each(self, callback: Callable[[Any, Any], bool]) -> bool:
        with self._lock:
            for key, value in self._real.items():
                if callback(key, value):
                    return True
            return False

    def clear(self, callback: Optional[Callable[[Any, Any], None]] = None):
        with self._lock:
            for key, value in list(self._real.items()):
                if callback:
                    callback(key, value)
                del self._real[key]


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