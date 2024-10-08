import cv2
import time
from camera import Camera
from interface import Settings



use_camera = False
class FrameGetter:
    last_frame = None
    frame_counter = 0
    def __init__(self, video_path, settings: Settings):
        """
        Initialize the FrameGetter.
        :param video_path: String path to the video file
        """
        if use_camera:
            self.cam = Camera(settings)
        else:
            for index, path in enumerate(video_path):
                self.cap = cv2.VideoCapture(path)
                if self.cap.isOpened():
                    print(f"able to open path {path}")
                    self.video_path = path
                    break
                if index == len(video_path) - 1:
                    print("video could not be opened")

    def get_frame(self):
        if use_camera:
            return self.cam.get_frame()

        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
            return self.last_frame
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            return self.last_frame

