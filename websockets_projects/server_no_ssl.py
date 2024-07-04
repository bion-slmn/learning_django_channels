import asyncio
import websockets


class Server:
    def __init__(self):
        self.CONNECTED = set()


    async def broadcast(self, message):
        if self.CONNECTED:
            await asyncio.wait([ws.send(message) for ws in self.CONNECTED])

    async def handle_client(self, websocket: websockets):
        '''
        handle a client
        '''
        self.CONNECTED.add(websocket)
        await self.broadcast(f"A user has joined the chat. Total users: {len(self.CONNECTED)}")

        try:
            async for message in websocket:
                await self.broadcast(message)
        finally:
            self.CONNECTED.remove(websocket)
            await self.broadcast(f"A user has joined the chat. Total users: {len(self.CONNECTED)}") 

    async def main(self):
        async with websockets.serve(self.handle_client, "localhost", 6789):
            await asyncio.Future()


server = Server()
print('Seerver started............')
asyncio.run(server.main())
