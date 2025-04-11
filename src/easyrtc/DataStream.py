import asyncio
import json
from aiortc import RTCDataChannel

class DataStream:
    def __init__(self, message=None, interval: float = 1.0):
        self.channel = None
        self._running = False
        self.message = message or {"type": "message", "message": "Hello!"}
        self.interval = interval

    def set_channel(self, channel: RTCDataChannel):
        self.channel = channel

        @channel.on("open")
        def on_open():
            print("Data channel is open!")
            self._running = True
            asyncio.create_task(self._send_data())

        @channel.on("close")
        def on_close():
            print("Data channel is closed")
            self._running = False

        @channel.on("message")
        def on_message(msg):
            try:
                data = json.loads(msg)
                print("Received JSON:", data)
            except json.JSONDecodeError:
                print("Received non-JSON message:", msg)

    async def _send_data(self):
        while self._running and self.channel and self.channel.readyState == "open":
            # Inject timestamp into message
            message_data = self.message.copy() if isinstance(self.message, dict) else {"message": self.message}

            self.channel.send(json.dumps(message_data))
            await asyncio.sleep(self.interval)

    def set_message(self, message):
        """
        Set the message to be sent.
        Accepts either a string or a dict (for JSON support).
        """
        if isinstance(message, (str, dict)):
            self.message = message
        else:
            raise ValueError("Message must be a string or dictionary.")

    def set_interval(self, interval: float):
        self.interval = interval
