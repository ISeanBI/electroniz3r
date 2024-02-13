import asyncio
import websockets

class WebSocketConnection:
    async def send_text(self, text):
        pass

    async def send_data(self, data):
        pass

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def listen(self):
        pass


class WebSocketConnectionDelegate:
    async def on_connected(self, connection):
        pass

    async def on_disconnected(self, connection, error):
        pass

    async def on_error(self, connection, error):
        pass

    async def on_message_text(self, connection, text):
        pass

    async def on_message_data(self, connection, data):
        pass


class WebSocketTaskConnectionSingleton(WebSocketConnection):
    def __init__(self):
        super().__init__()
        self.delegate = None
        self.web_socket_task = None
        self.did_debugger_respond = False

    @staticmethod
    def shared():
        return WebSocketTaskConnectionSingleton()

    async def send_text(self, text):
        await self.web_socket_task.send(text)

    async def send_data(self, data):
        await self.web_socket_task.send(data)

    async def connect(self):
        uri = "your_websocket_uri_here"
        async with websockets.connect(uri) as ws:
            self.web_socket_task = ws
            await self.delegate.on_connected(self)
            await self.listen()

    async def disconnect(self):
        await self.web_socket_task.close()
        await self.delegate.on_disconnected(self, None)

    async def listen(self):
        while True:
            result = await self.web_socket_task.recv()
            self.did_debugger_respond = True

            try:
                text = result.decode('utf-8')
                await self.delegate.on_message_text(self, text)
            except UnicodeDecodeError:
                await self.delegate.on_message_data(self, result)

    def execute_code_in_electron_app(self, code):
        wrapped_code = f"eval(Buffer.from('{code.encode().decode('base64')}', 'base64').toString())"
        cmd = f"{{\"id\":1337,\"method\":\"Runtime.evaluate\",\"params\":{{\"expression\":\"{wrapped_code}\",\"objectGroup\":\"console\",\"includeCommandLineAPI\":true,\"silent\":false,\"returnByValue\":false,\"generatePreview\":true,\"userGesture\":true,\"awaitPromise\":false,\"replMode\":true,\"allowUnsafeEvalBlockedByCSP\":false,\"executionContextId\":1}}}}"
        asyncio.run(self.send_text(cmd))