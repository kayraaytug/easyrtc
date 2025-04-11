from aiortc import RTCPeerConnection
from aiortc.contrib.signaling import TcpSocketSignaling

class WebRTCClient:
    def __init__(self, ip, port):
        self.pc = RTCPeerConnection()
        self.signaling = TcpSocketSignaling(ip, port)
        self.video_track = None
        self.data_channel = None

        @self.pc.on("track")
        def on_track(track):
            print(f"Received track: {track.kind}")
            if track.kind == "video":
                self.video_track = track

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            print(f"Data channel received: {channel.label}")
            self.data_channel = channel

            @channel.on("message")
            def on_message(message):
                print(f"Received data: {message}")

        @self.pc.on("connectionstatechange")
        async def on_connection_state_change():
            print(f"Connection state changed: {self.pc.connectionState}")
            if self.pc.connectionState in ["failed", "disconnected", "closed"]:
                print("Cleaning up connection...")
                await self.close()
                await self.connect()

    async def answer(self):
        offer = await self.signaling.receive()
        await self.pc.setRemoteDescription(offer)
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        await self.signaling.send(self.pc.localDescription)

    async def get_frame(self):
        """Returns a single frame as ndarray (BGR) from incoming video track."""
        if self.video_track is None:
            return None

        frame = await self.video_track.recv()
        return frame.to_ndarray(format="bgr24")

    async def connect(self):
        await self.signaling.connect()
        await self.answer()

    async def close(self):
        await self.signaling.close()
        await self.pc.close()
