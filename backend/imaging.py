from frame import Frame
from video_reader import FrameGetter
from frontend import Frontend
from plc import PLC
from interface import Settings
import asyncio
from constants import path_video
from line_finder import LineFinder


class Imaging:
    def __init__(self, settings: Settings, plc: PLC, frontend: Frontend):
        self.settings = settings
        self.plc = plc
        self.frame_getter = FrameGetter(path_video)
        self.numpy_image = self.frame_getter.get_frame()
        self.frontend = frontend
        self.line_finder = LineFinder()

    async def run(self):
        if self.frontend.enable_frame_update:
            self.numpy_image = self.frame_getter.get_frame()
        frame = Frame(self.numpy_image, self.settings.get_settings(), self.line_finder.get_lines())
        self.line_finder.update(frame.get_frame_collapsed())
        self.frontend.update_frame(frame)
        self.plc.send_line_values(self.line_finder.get_line_values())
        await self.plc.ready_for_new_frame()
