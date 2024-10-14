import cv2
from camera import Camera
from interface import Interface
from log import Log




class FrameGetter:
    last_frame = None
    frame_counter = 0
    video_active = False

    def __init__(self, video_path, settings: Interface, log: Log):
        self.cam = Camera(settings)
        self.log = log



    def get_frame(self):
        if not self.log.replay_active:
            frame = self.cam.get_frame()
            return frame

        if not self.video_active:
            self.init_video()

        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
            return self.last_frame
        else:
            self.cap.release()
            self.video_active = True
            self.init_video()
            return self.last_frame

    def init_video(self):
        self.cap = cv2.VideoCapture(self.log.replay_path)
        if self.cap.isOpened():
            self.video_active = True

