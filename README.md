# NEX_PY
- NEX Python Library for Wii U/3DS/Switch Games written in Python.

## Installation
```
pip install nex-retendo
```

## Features
- [x] HPP
- [x] PRUDP
   - [x] Transport UDP
   - [x] PRUDPv0 (Friend Server & some 3DS Games)
   - [x] PRUDPv1 (Wii U & some 3DS Games)
   - [x] PRUDPLite (Switch)
- [x] Kerberos
- [x] RMC

## Example
```python
from nex.rmc import RMCError
from nex.result_codes import ResultCodes
from nex.kerberos import ClientTicket
import collections
import secrets

import aioconsole
import asyncio

import logging
logging.basicConfig(level=logging.INFO)


ACCESS_KEY = "ridfebb9" # ACCESS KEY
NEX_VERSION = 10100 # NEX VERSION
SECURE_SERVER = "Quazal Rendez-Vous" # SECURE SERVER

User = collections.namedtuple("User", "pid name password")

users = [
	User(2, "Quazal Rendez-Vous", "password"),
	User(100, "guest", "MMQea3n!fsik")
]

def get_user_by_name(name):
	for user in users:
		if user.name == name:
			return user

def get_user_by_pid(pid):
	for user in users:
		if user.pid == pid:
			return user
			
def derive_key(user):
	deriv = kerberos.KeyDerivationOld(65000, 1024)
	return deriv.derive_key(user.password.encode("ascii"), user.pid)


class AuthenticationServer:
	def __init__(self, settings):
		super().__init__()
		self.settings = settings
	
	async def login(self, client, username):
		print("User trying to log in:", username)
		
		user = get_user_by_name(username)
		if not user:
			raise RMCError("RendezVous::InvalidUsername")
			
		server = get_user_by_name(SECURE_SERVER)
		
		url = StationURL(
			scheme="prudps", address="127.0.0.1", port=6000,
			PID = server.pid, CID = 1, type = 2,
			sid = 1, stream = 10
		)
		
		conn_data = authentication.RVConnectionData()
		conn_data.main_station = url
		conn_data.special_protocols = []
		conn_data.special_station = StationURL()
		
		response = RMCResponse()
		response.result = ResultCodes.success()
		response.pid = user.pid
		response.ticket = self.generate_ticket(user, server)
		response.connection_data = conn_data
		response.server_name = "Example server"
		return response
	
	# Generate Kerberos Ticket function.
	def generate_ticket(self, source, target):
		settings = self.settings
		
		user_key = derive_key(source)
		server_key = derive_key(target)
		session_key = secrets.token_bytes(settings["kerberos.key_size"])
		
		internal = kerberos.ServerTicket()
		internal.timestamp = DateTime.now()
		internal.source = source.pid
		internal.session_key = session_key
		
		ticket = ClientTicket()
		ticket.session_key = session_key
		ticket.target = target.pid
		ticket.internal = internal.encrypt(server_key, settings)
		
		return ticket.encrypt(user_key, settings)
		

class SecureServer:
	# Secure code here.
	pass 


async def main():
	s = settings.default() # Load default config.
	s.configure(ACCESS_KEY, NEX_VERSION) # Configuring ACCESS_KEY and NEX_VERSION.
	
	auth_servers = [
		AuthenticationServer(s)
	]
	secure_servers = [
		# You can add other Secure class.
		SecureServer()
	]
	
	server_key = derive_key(get_user_by_name(SECURE_SERVER))
	async with rmc.serve(s, auth_servers, "127.0.0.1", 6000): # Starting Authentication Server on 127.0.0.1 on port 6000.
		async with rmc.serve(s, secure_servers, "127.0.0.1", 6001, key=server_key): # Starting Secure Server on 127.0.0.1 on port 6001.
			await aioconsole.ainput("Press ENTER to close..\n")

asyncio.run(main()) # Run the main function.
```

## Credits
- Kinnay for some codes from NintendoClients.
