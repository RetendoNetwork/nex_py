from lz4.frame import LZ4FrameCompressor, LZ4FrameDecompressor
import struct


class LZ4Compression:
    def __init__(self):
        pass

    def compress(self, payload):
        compressed = LZ4FrameCompressor.compress(payload)
        compression_ratio = len(payload) // len(compressed) + 1
        result = struct.pack('B', compression_ratio) + compressed
        return result

    def decompress(self, payload):
        compression_ratio = struct.unpack('B', payload[0:1])[0]
        compressed = payload[1:]

        if compression_ratio == 0:
            return compressed

        try:
            decompressed = LZ4FrameDecompressor.decompress(compressed)
        except Exception as e:
            return []

        ratio_check = len(decompressed) // len(compressed) + 1
        if ratio_check != compression_ratio:
            raise ValueError(f"Failed to decompress payload. Got bad ratio. Expected {compression_ratio}, got {ratio_check}")

        return decompressed