from nex.streams import StreamOut


class AnyDataHolder:
	object_map = {}

	def __init__(self):
		self.data = None
		
	def encode(self, stream):	
		stream.string(self.data.__class__.__name__)
		
		substream = StreamOut(stream.settings)
		substream.add(self.data)
		
		stream.u32(len(substream.get()) + 4)
		stream.buffer(substream.get())
		
	def decode(self, stream):
		name = stream.string()
		substream = stream.substream().substream()
		self.data = substream.extract(self.object_map[name])
		
	@classmethod
	def register(cls, object, name):
		cls.object_map[name] = object