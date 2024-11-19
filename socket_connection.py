import socket
import websockets

from prudp_server import PRUDPServer
from mutex_map import MutexMap
from prudp_connection import PRUDPConnection


class SocketConnection:
    def __init__(self, server: PRUDPServer, address, websocket_connection: websockets):
        self.server = server
        self.address = address
        self.websocket_connection = websocket_connection
        self.connections = MutexMap(PRUDPConnection)