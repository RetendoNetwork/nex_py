import lzo
import struct


class LZO:
    """
    Implements packet payload compression using LZO.
    """

    def compress(self, payload: bytes) -> bytes:
        """
        Compresses the payload using LZO and returns the compressed data.
        """
        compressed = lzo.compress(payload)
        compression_ratio = len(payload) // len(compressed) + 1

        # Prepare the result by prepending the compression ratio
        result = bytearray()
        result.append(compression_ratio)  # First byte is the compression ratio
        result.extend(compressed)         # Append the compressed data

        return bytes(result)

    def decompress(self, payload: bytes) -> bytes:
        """
        Decompresses the payload using LZO and returns the decompressed data.
        """
        compression_ratio = payload[0]
        compressed = payload[1:]

        if compression_ratio == 0:
            # Compression ratio of 0 means no compression, return the original data
            return compressed

        try:
            decompressed = lzo.decompress(compressed)
        except Exception as e:
            raise Exception(f"Decompression failed: {e}")

        ratio_check = len(decompressed) // len(compressed) + 1

        if ratio_check != compression_ratio:
            raise ValueError(
                f"Failed to decompress payload. Got bad ratio. Expected {compression_ratio}, got {ratio_check}"
            )

        return decompressed

    def copy(self):
        """
        Returns a copy of the LZO compression algorithm.
        """
        return LZO()

def new_lzo_compression():
    """
    Returns a new instance of the LZO compression algorithm.
    """
    return LZO()