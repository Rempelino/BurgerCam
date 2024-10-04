import gxipy as gx
import cv2
from interface import Settings
from interface_definition import CamSettings


class Camera:
    latest_numpy_image = None
    camera_is_connected = False
    device_manager = None
    cam: gx.U3VDevice | None = None

    def __init__(self, settings: Settings):
        self.settings = settings
        self.connect_camera()

    def write_settings(self):
        if not self.camera_is_connected:
            return
        settings: CamSettings = self.settings.get_cam_settings()
        settings = self.validate_settings(settings)
        print(f'writing cam setting: {settings}')
        self.cam.ReverseX.set(settings.ReverseX)
        self.cam.ReverseY.set(settings.ReverseY)
        self.cam.ExposureTime.set(settings.ExposureTime)
        self.cam.ColorTransformationEnable.set(settings.ColorTransformationEnable)
        self.settings.cam_update_request_flag = False

    @staticmethod
    def validate_settings(settings: CamSettings):
        if settings.ExposureTime > 1000000.0:
            settings.ExposureTime = 1000000.0
        if settings.ExposureTime < 28.0:
            settings.ExposureTime = 28.0
        return settings

    def connect_camera(self):
        self.device_manager = gx.DeviceManager()
        try:
            dev_num, dev_info_list = self.device_manager.update_device_list()
        except gx.NeedMoreBuffer:
            print("Please remove other USB devices to connect to camera")
            return
        if dev_num == 0:
            print("no camera connected")
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
        self.cam.TriggerMode.set(gx.GxSwitchEntry.ON)
        self.cam.TriggerSource.set(gx.GxTriggerSourceEntry.SOFTWARE)
        # self.cam.data_stream[0].set_acquisition_buffer_number(1)
        self.cam.stream_on()
        self.write_settings()
        self.camera_is_connected = True
        print("Connected Cam")
        self.settings.set_cam_connection_state(self.camera_is_connected)

    def disconnect_camera(self):
        self.cam.close_device()
        self.camera_is_connected = False
        print("Disconnected Cam")
        self.settings.set_cam_connection_state(self.camera_is_connected)


    def get_frame(self):
        if not self.camera_is_connected:
            self.connect_camera()
            return None

        if self.settings.cam_update_request_flag:
            self.write_settings()

        # send command to camera to extract one frame
        try:
            self.cam.TriggerSoftware.send_command()
        except gx.OffLine:
            print("camera disconnected")
            self.disconnect_camera()
            return None
        except Exception as e:
            print(f"error at sending command {e}")


        # retrieve the frame
        raw_image = self.cam.data_stream[0].get_image()
        if raw_image is None:
            print("no frame received. Reconnecting camera")
            self.disconnect_camera()
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
