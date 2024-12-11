from nex.errors import error_codes, error_names, ERROR_MASK
from nex.rmc import RMCError


class ResultCodes:
	def __init__(self, code=0x10001):
		self.error_code = code
	
	def __str__(self):
		return "%s (0x%08X)" %(self.name(), self.code())
		
	@staticmethod
	def success(code="Core::Unknown"):
		if type(code) == str:
			code = error_codes[code]
		return ResultCodes(code & ~ERROR_MASK)
		
	@staticmethod
	def error(code="Core::Unknown"):
		if type(code) == str:
			code = error_codes[code]
		return ResultCodes(code | ERROR_MASK)
	
	def is_success(self):
		return not self.error_code & ERROR_MASK
		
	def is_error(self):
		return bool(self.error_code & ERROR_MASK)
	
	def code(self):
		return self.error_code
		
	def name(self):
		if self.is_success():
			return "success"
		return error_names.get(self.error_code & ~ERROR_MASK, "unknown error")
		
	def raise_if_error(self):
		if self.is_error():
			raise RMCError(self.error_code)