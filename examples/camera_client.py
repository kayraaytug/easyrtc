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
