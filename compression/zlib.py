import zlib


class Zlib:
    def compress(self, payload: bytes) -> bytes:
        """
        Compresses the payload using zlib and returns the compressed data
        with the compression ratio as the first byte.
        """
        compressed = zlib.compress(payload)

        compression_ratio = len(payload) // len(compressed) + 1

        # Adding the compression ratio as the first byte
        result = bytes([compression_ratio]) + compressed

        return result

    def decompress(self, payload: bytes) -> bytes:
        """
        Decompresses the payload using zlib, checking the compression ratio.
        """
        compression_ratio = payload[0]
        compressed = payload[1:]

        if compression_ratio == 0:
            # Compression ratio of 0 means no compression
            return compressed

        decompressed = zlib.decompress(compressed)

        # Check if the decompression ratio is correct
        ratio_check = len(decompressed) // len(compressed) + 1

        if ratio_check != compression_ratio:
            raise ValueError(f"Failed to decompress payload. Got bad ratio. Expected {compression_ratio}, got {ratio_check}")

        return decompressed

    def copy(self):
        """
        Returns a new instance of the Zlib compression algorithm.
        """
        return Zlib()