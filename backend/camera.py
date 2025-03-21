import gxipy as gx
import cv2
from interface import Interface
from interface_definition import CamSettings
import time_debug
from dataclasses import replace


class Camera:
    latest_numpy_image = None
    camera_is_connected = False
    device_manager = None
    cam: gx.U3VDevice | None = None
    last_written_settings = None

    def __init__(self, settings: Interface):
        self.settings = settings
        self.connect_camera()
        if not self.camera_is_connected:
            print("unable to connect camera")

    def connect_camera(self):
        self.device_manager = gx.DeviceManager()
        try:
            dev_num, dev_info_list = self.device_manager.update_device_list()
        except gx.NeedMoreBuffer:
            print("Please remove other USB devices to connect to camera")
            return
        if dev_num == 0:
            return
        try:
            self.cam = self.device_manager.open_device_by_index(1)
            print(
                f"successfully connected to camera. Vendor: {dev_info_list[0]['vendor_name']}, Device: {dev_info_list[0]['model_name']}, Serial Number: {dev_info_list[0]['sn']}")
        except gx.InvalidAccess as e:
            print(f"Camera is already connected to a different application. InvalidAccess exception: {e}")
            return
        except gx.OffLine:
            print("Camera disconnected")
            return
        self.camera_is_connected = True
        self.settings.set_cam_connection_state(self.camera_is_connected)
        self.last_written_settings = None
        self.write_settings()

        # empty frame buffer just in case to prevent delays
        while self.cam.data_stream[0].get_image() is not None:
            print("frame was not none")

    def write_settings(self):
        if self.last_written_settings == self.settings.get_cam_settings():
            print("not updating cam interface as they did not change")
            self.settings.cam_update_request_flag = False
            return
        if not self.camera_is_connected:
            return
        settings: CamSettings = self.settings.get_cam_settings()
        settings = self.validate_settings(settings)

        # turn off the stream if active
        if not self.cam.Width.is_writable():
            self.cam.stream_off()

        # set all the interface
        self.cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        self.cam.Width.set(4096)
        self.cam.Height.set(settings.frame_cutout.max - settings.frame_cutout.min)
        self.cam.OffsetY.set(settings.frame_cutout.min)
        self.cam.ReverseX.set(settings.ReverseX)
        self.cam.ReverseY.set(settings.ReverseY)
        self.cam.ExposureTime.set(settings.ExposureTime)
        self.cam.ColorTransformationEnable.set(settings.ColorTransformationEnable)
        self.settings.cam_update_request_flag = False

        # replace -> deepcopy
        self.last_written_settings = replace(settings)

        # turn on the stream
        self.cam.stream_on()

    def update_exposure(self):
        settings: CamSettings = self.settings.get_cam_settings()
        settings = self.validate_settings(settings)
        self.cam.ExposureTime.set(settings.ExposureTime)
        self.settings.cam_exposure_update_flag = False
        self.last_written_settings.ExposureTime = settings.ExposureTime

    @staticmethod
    def validate_settings(settings: CamSettings):
        if settings.ExposureTime > 1000000.0:
            settings.ExposureTime = 1000000.0
        if settings.ExposureTime < 28.0:
            settings.ExposureTime = 28.0

        settings.frame_cutout.max += settings.frame_cutout.max % 2
        settings.frame_cutout.min += settings.frame_cutout.min % 2

        return settings

    def disconnect_camera(self):
        self.cam.close_device()
        self.camera_is_connected = False
        self.settings.set_cam_connection_state(self.camera_is_connected)

    def send_acquisition_command(self):
        # send command to camera to extract one frame
        try:
            self.cam.TriggerSoftware.send_command()
        except gx.OffLine:
            print("camera disconnected")
            self.disconnect_camera()
        except Exception as e:
            print(f"error at sending command {e}")
            self.disconnect_camera()

    def get_frame(self):
        time_debug.print_time("starting to get frame")
        if not self.camera_is_connected:
            self.connect_camera()
            return None

        if self.settings.cam_update_request_flag:
            self.write_settings()

        if self.settings.cam_exposure_update_flag:
            self.update_exposure()

        raw_image = self.cam.data_stream[0].get_image()
        self.send_acquisition_command()

        time_debug.print_time("got raw image")
        if raw_image is None:
            print("no frame received")
            # self.disconnect_camera()
            return None

        rgb_image = raw_image.convert("RGB")
        time_debug.print_time("got RGB image")
        rgb_array = rgb_image.get_numpy_array()
        time_debug.print_time("got RGB array")
        numpy_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        time_debug.print_time("got numpy image")



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
