import time

from camera import Camera
from frame import Frame
from SliderWindow import SliderWindow
from video_reader import FrameGetter
from Frontend import Frontend
from settings import Settings


print_string = ""
cam = Camera()
slider_configs = [
    {"name": "Min Blau", "min": 0, "max": 255},
    {"name": "Max Blau", "min": 0, "max": 255},
    {"name": "Min Gruen", "min": 0, "max": 255},
    {"name": "Max Gruen", "min": 0, "max": 255},
    {"name": "Min Rot", "min": 0, "max": 255},
    {"name": "Max Rot", "min": 0, "max": 255},
    {"name": "Expected Lines", "min": 0, "max": 10},
    {"name": "Filter 1", "min": 0, "max": 20},
    {"name": "Filter 2", "min": 0, "max": 20},
    {"name": "Filter 3", "min": 0, "max": 1000},
    {"name": "Filter 4", "min": 0, "max": 1000}
]

settings = Settings()

slider_window = SliderWindow("Custom Sliders", slider_configs)

frame_getter = FrameGetter(r"D:\Videos Burger Wback\video 10.avi")
frontend = Frontend(settings)

numpy_image = frame_getter.get_frame()
while True:
    if frontend.enable_frame_update:
        numpy_image = frame_getter.get_frame()
    frame = Frame(numpy_image, slider_window.get_slider_values(), 800, 2300, settings.get_settings())
    frontend.update_frame(frame)
    #time.sleep(1)
