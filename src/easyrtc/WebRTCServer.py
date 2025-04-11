from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling

class WebRTCServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.camera_stream = None
        self.data_streams = []

    def add_camera_stream(self, stream):
        """Add a media track to the server."""
        self.camera_stream = stream

    def add_data_stream(self, data_stream):
        """Add a data stream to the server."""
        self.data_streams.append(data_stream)

    async def _setup_peer_connection(self):
        pc = RTCPeerConnection()

        # Add camera stream
        pc.addTrack(self.camera_stream)

        # Create a single data channel and link to data streams
        if self.data_streams:
            channel = pc.createDataChannel("chat")
            for ds in self.data_streams:
                ds.set_channel(channel)

        return pc

    async def _handle_signaling(self, pc, signaling):
        """Handle signaling messages for one session."""
        await signaling.connect()

        @pc.on("connectionstatechange")
        async def on_connection_state_change():
            print(f"Connection state changed: {pc.connectionState}")
            if pc.connectionState in ["failed", "disconnected", "closed"]:
                print("Cleaning up connection...")
                await pc.close()

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)

        try:
            await signaling.send(pc.localDescription)
        except Exception as e:
            print(f"Failed to send offer: {e}")
            return

        while True:
            obj = await signaling.receive()
            if isinstance(obj, RTCSessionDescription):
                await pc.setRemoteDescription(obj)
                print("Remote description set")
            elif obj is None:
                print("Signaling ended")
                break

    async def handle_connection(self):
        """Continuously listen for and handle WebRTC connections."""
        while True:
            print(f"WebRTC listening on {self.ip_address}:{self.port}")
            signaling = TcpSocketSignaling(self.ip_address, self.port)
            pc = await self._setup_peer_connection()

            try:
                await self._handle_signaling(pc, signaling)
            except Exception as e:
                print(f"Error during signaling: {e}")
            finally:
                await pc.close()
                try:
                    await signaling.close()
                except Exception:
                    pass
                print("Connection closed, waiting for new client...")
                
    async def run(self):
        if not self.camera_stream:
            raise RuntimeError("WebRTCServer requires at least one media track.")
        await self.handle_connection()
