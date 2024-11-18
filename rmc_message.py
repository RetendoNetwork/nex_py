import struct

import streams
from endpoint_interface import EndpointInterface


class RMCRequest:
	def __init__(self):
		self.endpoint = EndpointInterface
		self.is_request = True

class RMCResponse:
	pass

class RMCMessage:
	REQUEST = 0
	RESPONSE = 1
	
	def __init__(self, settings):
		self.settings = settings
		
		self.mode = RMCMessage.REQUEST
		self.protocol = None
		self.method = None
		self.call_id = 0
		self.error = -1
		self.body = b""
		
	@staticmethod
	def prepare(settings, mode, protocol, method, call_id, body):
		inst = RMCMessage(settings)
		inst.mode = mode
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.body = body
		return inst
		
	@staticmethod
	def request(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.REQUEST, protocol, method, call_id, body
		)
		
	@staticmethod
	def response(settings, protocol, method, call_id, body):
		return RMCMessage.prepare(
			settings, RMCMessage.RESPONSE, protocol, method, call_id, body
		)
		
	@staticmethod
	def error(settings, protocol, method, call_id, error):
		inst = RMCMessage(settings)
		inst.mode = RMCMessage.RESPONSE
		inst.protocol = protocol
		inst.method = method
		inst.call_id = call_id
		inst.error = error
		return inst
	
	@staticmethod
	def parse(settings, data):
		inst = RMCMessage(settings)
		inst.decode(data)
		return inst
		
	def encode(self):
		stream = streams.StreamOut(self.settings)
		
		flag = 0x80 if self.mode == self.REQUEST else 0
		if self.protocol < 0x80:
			stream.u8(self.protocol | flag)
		else:
			stream.u8(0x7F | flag)
			stream.u16(self.protocol)
		
		if self.mode == self.REQUEST:
			stream.u32(self.call_id)
			stream.u32(self.method)
			stream.write(self.body)
		else:
			if self.error != -1 and self.error & 0x80000000:
				stream.bool(False)
				stream.u32(self.error)
				stream.u32(self.call_id)
			else:
				stream.bool(True)
				stream.u32(self.call_id)
				stream.u32(self.method | 0x8000)
				stream.write(self.body)
		return struct.pack("I", stream.size()) + stream.get()
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		length = stream.u32()
		if length != stream.size() - 4:
			raise ValueError("RMC message has unexpected size")
		
		protocol = stream.u8()
		self.protocol = protocol & ~0x80
		if self.protocol == 0x7F:
			self.protocol = stream.u16()
		
		if protocol & 0x80:
			self.mode = self.REQUEST
			self.call_id = stream.u32()
			self.method = stream.u32()
			self.body = stream.readall()
		else:
			self.mode = self.RESPONSE
			if stream.bool():
				self.call_id = stream.u32()
				self.method = stream.u32() & ~0x8000
				self.body = stream.readall()
			else:
				self.error = stream.u32()
				self.call_id = stream.u32()
				if not stream.eof():
					raise ValueError("RMC error message is bigger than expected")