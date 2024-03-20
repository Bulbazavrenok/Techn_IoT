from async_websocket_client.apps import AsyncWebSocketApp
from async_websocket_client.dispatchers import BaseDispatcher


class SomeDispatcher(BaseDispatcher):
    def __init__(self, agent_id: int):
        super().__init__()
        self.agent_id = agent_id

    async def on_connect(self):
        print(f'Connected to websocket server (id = {self.agent_id})')

    async def on_message(self, message: str):
        print(f'received: {message} (id = {self.agent_id})')


if __name__ == "__main__":
    client = AsyncWebSocketApp('ws://localhost:8000/ws/0', SomeDispatcher(0))

    client.asyncio_run()
