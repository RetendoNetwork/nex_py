class StationURL:
	str_params = ["address", "Uri", "Rsa", "Ra", "Ntrpa"]
	int_params = [
		"port", "stream", "sid", "PID", "CID", "type", "RVCID",
		"natm", "natf", "upnp", "pmp", "probeinit", "PRID",
		"fastproberesponse", "NodeID", "R", "Rsp", "Rp",
		"Tpt", "Pl", "Ntrpp"
	]

	def __init__(self, scheme="prudp", **kwargs):
		self.urlscheme = scheme
		self.params = kwargs

	def __repr__(self):
		params = ";".join(
			["%s=%s" %(key, value) for key, value in self.params.items()]
		)
		if self.urlscheme:
			return "%s:/%s" %(self.urlscheme, params)
		return params
		
	def __getitem__(self, field):
		if field in self.str_params:
			return str(self.params.get(field, ""))
		if field in self.int_params:
			return int(self.params.get(field, 0))
		raise KeyError(field)
		
	def __setitem__(self, field, value):
		self.params[field] = value
	
	def scheme(self):
		return self.urlscheme
		
	def address(self):
		return self["address"], self["port"]
		
	def is_public(self): 
		return bool(self["type"] & 2)
	
	def is_behind_nat(self): 
		return bool(self["type"] & 1)
	
	def is_global(self): 
		return self.is_public() and not self.is_behind_nat()
		
	def copy(self):
		return StationURL(self.urlscheme, **self.params)
		
	@classmethod
	def parse(cls, string):
		if string:
			scheme, fields = string.split(":/")
			params = {}
			if fields:
				params = dict(field.split("=") for field in fields.split(";"))
			return cls(scheme, **params)
		else:
			return cls()