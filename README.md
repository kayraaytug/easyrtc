# EasyRTC

**EasyRTC** is a lightweight Python-based WebRTC framework built with `aiortc` that allows easy peer-to-peer video and data streaming between a server and client using OpenCV and asyncio. This example demonstrates how to capture video on the server side and display it in real-time on the client side with grayscale processing.

---

## Features

- 🎥 Simple server-side webcam streaming
- 📡 WebRTC-based peer-to-peer video connection
- 🎞️ Real-time OpenCV processing

---

## Requirements

- Python 3.7+
- `aiortc`
- `opencv-python`
- `numpy`
- `av`

You can install the required packages with:

```bash
pip install easyrtc
```

## Examples

### `camera_server.py`

```python
from easyrtc import WebRTCServer, CameraStream
import asyncio

async def main():
    server = WebRTCServer("127.0.0.1", 9999)
    server.add_camera_stream(CameraStream())
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### `camera_client.py`

```python
from easyrtc import WebRTCClient
import asyncio
import cv2

async def main():
    client = WebRTCClient("127.0.0.1", 9999)
    await client.connect()
  
    while True:
        frame = await client.get_frame()
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("WebRTC Client", gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    await client.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())

```

#### `data_server.py`

```python
from easyrtc import WebRTCServer, DataStream
import asyncio

async def main():
    server = WebRTCServer("127.0.0.1", 9999)
    server.add_data_stream(DataStream(
        message={"type": "status", "value": "running"},
        interval=1.0
    ))
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```
