from frame import Frame
from video_reader import FrameGetter
from frontend import Frontend
from plc import PLC
from interface import Settings
import asyncio

class Imaging:
    def __init__(self, settings: Settings, plc: PLC, frontend: Frontend):
        self.settings = settings
        self.plc = plc
        self.frame_getter = FrameGetter(r"D:\Videos Burger Wback\video 10.avi")
        self.numpy_image = self.frame_getter.get_frame()
        self.frontend = frontend

    async def run(self):
        if self.frontend.enable_frame_update:
            self.numpy_image = self.frame_getter.get_frame()
        frame = Frame(self.numpy_image, 6, 800, 2300, self.settings.get_settings())
        self.frontend.update_frame(frame)
        self.plc.send_line_values(frame.get_line_values())
        while self.plc.new_line_values_available:
            await asyncio.sleep(0)





