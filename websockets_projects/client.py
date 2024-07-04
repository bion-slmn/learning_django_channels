import asyncio
import websockets
from websockets_projects.server_with_ssl import Server
import ssl
import pathlib


class Client:
    def __init__(self, ip_address, port):
        self.url = f'wss://{ip_address}:{port}'

    async def connect_server(self):

        async with websockets.connect(self.url,
                                      ssl=self.load_sslcontext()
                                      ) as websocket:
            while True:
                name = input("What is your name ?")

                await websocket.send(name)
                print(f'>>> {name:>11}')

                greeting = await websocket.recv()
                print(f'<<<<<<< {name:<20}')

    def load_sslcontext(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
        ssl_context.load_verify_locations(localhost_pem)

        return ssl_context


client = Client('localhost', 8765)
asyncio.run(client.connect_server())
