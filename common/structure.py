from nex.streams import StreamOut

import logging
logger = logging.getLogger(__name__)


class Structure:
	def max_version(self, settings): 
		return 0
			
	def get_hierarchy(self):
		hierarchy = []
		cls = self.__class__
		while cls != Structure:
			hierarchy.append(cls)
			cls = cls.__bases__[0]
		return hierarchy[::-1]
	
	def encode(self, stream):
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			if stream.settings["nex.struct_header"]:
				version = cls.max_version(self, stream.settings)
				
				substream = StreamOut(stream.settings)
				cls.save(self, substream, version)
				
				stream.u8(version)
				stream.buffer(substream.get())
			else:
				cls.save(self, stream, 0)

	def decode(self, stream):
		hierarchy = self.get_hierarchy()
		for cls in hierarchy:
			if stream.settings["nex.struct_header"]:
				max_version = cls.max_version(self, stream.settings)
				
				version = stream.u8()
				if version > max_version:
					logger.warning(
						"Struct %s version is higher than expected (%i > %i)",
						cls.__name__, version, max_version
					)
					
				substream = stream.substream()
				cls.load(self, substream, version)
				
				if not substream.eof():
					logger.warning(
						"Struct %s has unexpected size (got %i bytes, but only %i were read)",
						cls.__name__, substream.size(), substream.tell()
					)
			else:
				cls.load(self, stream, 0)
				
	def load(self, stream, version): 
		raise NotImplementedError("%s.load()" %self.__class__.__name__)
	
	def save(self, stream, version): 
		raise NotImplementedError("%s.save()" %self.__class__.__name__)