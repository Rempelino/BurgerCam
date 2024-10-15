from frame import Frame
from frame_getter import FrameGetter
from frontend import Frontend
from plc import PLC
from interface import Interface
from line_finder import LineFinder
from log import Log
import time_debug


class Imaging:
    def __init__(self, settings: Interface, plc: PLC, frontend: Frontend, log: Log):
        self.settings = settings
        self.plc = plc
        self.frame_getter = FrameGetter(settings, log)
        self.numpy_image = self.frame_getter.get_frame()
        self.frontend = frontend
        self.line_finder = LineFinder()
        self.log = log

    def run(self):
        self.numpy_image = self.frame_getter.get_frame()
        self.log.update_frame(self.numpy_image)#[self.settings.settings.cam_settings.frame_cutout.min:self.settings.settings.cam_settings.frame_cutout.max, :])
        if self.numpy_image is None:
            frame = None
            self.settings.plc_state_update_request_flag = True
        else:
            time_debug.print_time("starting frame process")
            frame = Frame(self.numpy_image, self.settings.get_settings(), self.line_finder.get_lines())
            self.line_finder.update(frame.get_frame_collapsed(), self.settings.settings.lines)
            time_debug.print_time("lines updated")
            self.plc.send_line_values(self.line_finder.get_line_values())
        self.frontend.update_frame(frame)
        time_debug.print_time("imaging done")


