import cv2
from aiortc import VideoStreamTrack
from av import VideoFrame
import fractions

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    async def recv(self):
        self.frame_count += 1
        ret, frame = self.cap.read()
        
        if not ret:
            print("Failed to read frame from camera")
            return None
        
        # Create and return an AIORTC VideoFrame
        video_frame = VideoFrame.from_ndarray(frame)
        video_frame.pts = self.frame_count
        video_frame.time_base = fractions.Fraction(1, 30)
        return video_frame

    def __del__(self):
        """Release camera and video writer when the object is destroyed."""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()