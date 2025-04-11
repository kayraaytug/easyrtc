from easyrtc import WebRTCServer, CameraStream
import asyncio

async def main():
    server = WebRTCServer("127.0.0.1", 9999)
    server.add_camera_stream(CameraStream())
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())