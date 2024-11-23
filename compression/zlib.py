import zlib


class Zlib:
    def compress(self, payload: bytes) -> bytes:
        compressed = zlib.compress(payload)

        compression_ratio = len(payload) // len(compressed) + 1

        result = bytes([compression_ratio]) + compressed

        return result

    def decompress(self, payload: bytes) -> bytes:
        compression_ratio = payload[0]
        compressed = payload[1:]

        if compression_ratio == 0:
            return compressed

        decompressed = zlib.decompress(compressed)

        ratio_check = len(decompressed) // len(compressed) + 1

        if ratio_check != compression_ratio:
            raise ValueError(f"Failed to decompress payload. Got bad ratio. Expected {compression_ratio}, got {ratio_check}")

        return decompressed

    def copy(self):
        return Zlib()