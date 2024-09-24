import gxipy as gx
import cv2
import numpy as np


class Camera:
    latest_numpy_image = None
    camera_is_connected = False
    device_manager = None
    cam = None

    def __init__(self):
        self.connect_camera()

    def connect_camera(self):
        self.device_manager = gx.DeviceManager()
        dev_num, dev_info_list = self.device_manager.update_device_list()
        if dev_num == 0:
            print("no camera connected")
            return
        print(f"successfully connected to camera. Vendor: {dev_info_list[0]['vendor_name']}, Device: {dev_info_list[0]['model_name']}, Serial Number: {dev_info_list[0]['sn']}")
        try:
            self.cam = self.device_manager.open_device_by_index(1)
        except gx.InvalidAccess as e:
            print(f"Camera is already connected to a different application. InvalidAccess exception: {e}")
            return

        self.cam.TriggerMode.set(gx.GxSwitchEntry.OFF)
        self.cam.data_stream[0].set_acquisition_buffer_number(1)
        self.cam.stream_on()
        self.camera_is_connected = True

    def get_frame(self):
        if not self.camera_is_connected:
            self.connect_camera()
            return None
        raw_image = self.cam.data_stream[0].get_image()
        if raw_image is None:
            print("no frame received. Reconnecting camera")
            self.camera_is_connected = False
            self.cam.close_device()
            return None
        rgb_image = raw_image.convert("RGB")
        rgb_array = rgb_image.get_numpy_array()
        numpy_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        return numpy_image

if __name__ == '__main__':
    print("running")
    cam = Camera()
    while True:
        image = cam.get_frame()
        if image is not None:
            image = cv2.resize(image, (800, 400))
            cv2.imshow('NumPy Image', image)
            cv2.waitKey(1)
