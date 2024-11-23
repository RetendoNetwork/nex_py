class Dummy:
    def __init__(self):
        self.key = []

    def get_key(self) -> list:
        return self.key

    def set_key(self, key: list) -> None:
        self.key = key

    def encrypt(self, payload: list) -> list:
        return payload

    def decrypt(self, payload: list) -> list:
        return payload

    def copy(self) -> 'Dummy':
        copied = Dummy()
        copied.set_key(self.key)
        return copied