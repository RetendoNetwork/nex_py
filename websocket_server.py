import asyncio
import websockets
import time
from typing import List

from prudp_connection import PRUDPConnection

PING_INTERVAL = 5
PING_WAIT = 10

class WebSocketServer:
    def __init__(self, prudp_server: PRUDPServer):
        self.prudp_server = prudp_server
        self.event_handler = WSHandler(self.prudp_server)
    
    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        await self.event_handler.on_open(websocket)

        try:
            async for message in websocket:
                await self.event_handler.on_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.event_handler.on_close(websocket)

    def listen(self, port: int):
        start_server = websockets.serve(self.handler, "localhost", port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Server started on ws://localhost:{port}")
        asyncio.get_event_loop().run_forever()

    def listen_secure(self, port: int, cert_file: str, key_file: str):
        start_server = websockets.serve(self.handler, "localhost", port, ssl={"certfile": cert_file, "keyfile": key_file})
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Server started on wss://localhost:{port}")
        asyncio.get_event_loop().run_forever()

class WSHandler:
    def __init__(self, prudp_server: PRUDPServer):
        self.prudp_server = prudp_server

    async def on_open(self, websocket: websockets.WebSocketServerProtocol):
        # Set ping interval and wait time
        websocket.pong_time = time.time() + PING_INTERVAL + PING_WAIT

    async def on_close(self, websocket: websockets.WebSocketServerProtocol):
        connections: List[PRUDPConnection] = []
        socket = self.prudp_server.get_connection(websocket.remote_address[0])
        
        if not socket:
            # Handle error if socket is not found
            return

        for connection in socket.connections.values():
            connections.append(connection)

        # Cleanup connections
        for connection in connections:
            connection.cleanup()

    async def on_ping(self, websocket: websockets.WebSocketServerProtocol, payload: bytes):
        websocket.pong_time = time.time() + PING_INTERVAL + PING_WAIT
        await websocket.pong()

    async def on_pong(self, websocket: websockets.WebSocketServerProtocol, payload: bytes):
        pass

    async def on_message(self, websocket: websockets.WebSocketServerProtocol, message: str):
        packet_data = message.encode()  # Convert message to bytes
        try:
            await self.prudp_server.handle_socket_message(packet_data, websocket.remote_address[0], websocket)
        except Exception as err:
            print(f"Error: {err}")
