import zlib


class ZlibCompression:
	def compress(self, data):
		compressed = zlib.compress(data)
		ratio = int(len(data) / len(compressed) + 1)
		return bytes([ratio]) + compressed
		
	def decompress(self, data):
		if data[0] == 0:
			return data[1:]
		
		decompressed = zlib.decompress(data[1:])
		ratio = int(len(decompressed) / (len(data) - 1) + 1)
		if ratio != data[0]:
			raise ValueError("Unexpected compression ratio (expected %i, got %i)" %ratio, data[0])
		return decompressed