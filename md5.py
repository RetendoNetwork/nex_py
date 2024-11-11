import hashlib


def md5_hash(text: bytes) -> bytes:
    hasher = hashlib.md5()
    hasher.update(text)
    return hasher.digest()