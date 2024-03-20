import json
from threading import Thread
from typing import Callable

import websocket


class WebSocketHandler(Thread):
    def __init__(self, agent_id: int,
                 on_open: Callable[[], None] = lambda: print('connected to a websocket'),
                 on_message: Callable[[str], None] = lambda msg: print(f'received message: {msg}'),
                 on_error: Callable[[str], None] = lambda err: print(f'error: {err}'),
                 on_close: Callable[[int, str], None] = lambda code, msg: print(f'closed: {code} {msg}')):
        super().__init__()

        self.agent_id = agent_id
        self.url = f"ws://localhost:8000/ws/{agent_id}"
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close


    def set_on_message(self, on_message: Callable[[str], None]):
        self.on_message = on_message

    def _on_open(self, ws):
        self.on_open()

    def _on_message(self, ws, message):
        data_dict = json.loads(message)
        self.on_message(data_dict)

    def _on_error(self, ws, error):
        self.on_error(error)

    def _on_close(self, ws, close_status_code, close_msg):
        self.on_close(close_status_code, close_msg)

    def run(self):
        ws = websocket.WebSocketApp(self.url,
                                    on_open=self._on_open,
                                    on_message=self._on_message,
                                    on_error=self._on_error,
                                    on_close=self._on_close)

        ws.run_forever(reconnect=5)


if __name__ == "__main__":
    ws = WebSocketHandler(0)
    ws.start()

    ws2 = WebSocketHandler(1)
    ws2.start()
