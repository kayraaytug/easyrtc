from easyrtc import WebRTCServer
from easyrtc import DataStream
import asyncio

async def main():
    server = WebRTCServer("127.0.0.1", 9999)
    server.add_data_stream(DataStream())
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())