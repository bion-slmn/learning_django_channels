import asyncio
import websockets
import signal
import pathlib
import ssl


class Server:
    def __init__(self):
        self.server = None

    async def handle_client(self, websocket):
        '''
        recieve information from the client and send the name
        '''
        try:
            while True:
                try:
                    name = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    print(f'<<<< {name :#>11}')

                    greeting = f'Hello {name}'

                    # Send data to the client
                    await websocket.send(greeting)
                    print(f">>> {greeting:>20}")
                except asyncio.TimeoutError:
                    print("Timeout: No message received from client")
                    break
        except websockets.ConnectionClosedOK:
            print("Connection closed by the client")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def main(self):
        '''
        main process to run the server

        '''
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.sig_handler)

        print("Startin server...................")
        async with websockets.serve(self.handle_client,
                                    "localhost", 8765,
                                    ssl=self.load_sslcontext()) as server:
            self.server = server
            await asyncio.Future()
        print('Server closed..........')

    def load_sslcontext(self) -> ssl.SSLContext:
        '''
        load ssl context
        '''
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        local_pem = pathlib.Path(__file__).with_name('localhost.pem')
        ssl_context.load_cert_chain(local_pem)

        return ssl_context

    def sig_handler(self):
        for task in asyncio.all_tasks():
            task.cancel()
        self.server.close


if __name__ == "__main__":
    server = Server()
    try:
        asyncio.run(server.main())
    except asyncio.exceptions.CancelledError:
        print('Main task closed...............')
