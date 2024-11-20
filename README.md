# NEX
- Retendo Network PRUDP/NEX server library.

# Installation
> [!WARNING]
> NOTE: We have not put this lib directly with pip yet.
- Install [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads/).
- After, open folder explorer and go to `C:\Users\YourUser\AppData\Local\Programs\Python\PythonXXX\Lib\site-packages`.
- Then, open the cmd on this folder and run `git clone https://github.com/RetendoNetwork/nex.git`.
- After, on the cmd run `cd nex` and run `pip install .`
- And now you have Retendo Network NEX with Python.
> [!TIP]  
> If it's doesn't work to import NEX Library, try to run on the cmd `pip show nex`.

# Supported features
- [ ] Quazal Support
- [ ] HPP Support
  - [x] HPP Client
  - [ ] HPP Packet
  - [ ] HPP Server
- [ ] PRUDP Support
  - [ ] PRUDP Connection
  - [ ] PRUDP Packet
  - [ ] PRUDP Servers
  - [ ] PRUDP EndPoint
  - [ ] UDP Transport
  - [x] PRUDPv0 Packet
  - [x] PRUDPv1 Packet
- [x] Kerberos Authentication
- [x] RMC
  - [x] RMC Message
  - [x] RMC Request
- [x] NAT Checker (Support Add)

# Example for use NEX
```py
from nex.type.pid import PID
from nex.account import Account
import nex.rmc_message
from nex.packet_interface import PacketInterface
from nex.prudp_server import PRUDPServer, PRUDPEndpoint

def main():
    # Initialize PRUDP server and endpoint
    auth_server = PRUDPServer()
    endpoint = PRUDPEndPoint(1)

    # Create a new account and set server account
    endpoint.server_account = Account(PID(1), "Quazal Authentication", "password")
    endpoint.account_details_by_pid = {}  # Example of account details by PID
    endpoint.account_details_by_username = {}  # Example of account details by username

    # Setup event handler for packet data
    def on_data_handler(packet):
        if isinstance(packet, PRUDPPacketInterface):
            request = packet.rmc_message()
            print(f"[AUTH] ProtocolID: {request.protocol_id}, MethodID: {request.method_id}")

            if request.protocol_id == 0xA:  # TicketGrantingProtocol
                if request.method_id == 0x1:  # TicketGrantingProtocol::Login
                    handle_login(packet)

                if request.method_id == 0x3:  # TicketGrantingProtocol::RequestTicket
                    handle_request_ticket(packet)

    endpoint.on_data(on_data_handler)

    # Bind endpoint to the server and configure settings
    auth_server.bind_prudp_endpoint(endpoint)
    auth_server.set_fragment_size(962)
    auth_server.library_versions = {"default": {"major": 1, "minor": 1, "patch": 0}}
    auth_server.listen(60000)
```