from Crypto.Cipher import ARC4

class RC4:
	def __init__(self, key):
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
	
	def set_key(self, key):
		self.rc4enc = ARC4.new(key)
		self.rc4dec = ARC4.new(key)
		
	def encrypt(self, data): 
		return self.rc4enc.encrypt(data)
	
	def decrypt(self, data): 
		return self.rc4dec.decrypt(data)