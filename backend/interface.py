import struct
from dataclasses import asdict, fields, is_dataclass
from enum import Enum
from typing import Union

from interface_definition import SettingsStructure, MaxMin, State
from save_settings import write_dataclass_to_file, read_dataclass_from_file


class Interface:
    plc_settings_update_request_flag = False
    plc_state_update_request_flag = False
    cam_update_request_flag = False
    plc_settings_download_request_flag = False
    cam_exposure_update_flag = False

    def __init__(self):
        try:
            self.settings = read_dataclass_from_file(SettingsStructure, 'settings_save.pkl')
        except AttributeError:
            self.settings = None
            print("unable to read dataclass from file")
        if not check_dataclass_structure(self.settings, SettingsStructure):
            print("dataclass structure of file was incorrect. Applying defaults.")
            self.settings = SettingsStructure()
        self.validate_settings(self.settings)
        self.state = State()

    def set_settings(self, settings: Union[SettingsStructure, bytearray]):
        # interface changed by frontend
        if isinstance(settings, SettingsStructure):
            print(f"setting settings to {settings}")
            self.validate_settings(settings)
            self.plc_settings_update_request_flag = True

        # interface changed by plc
        else:
            print(f"setting settings to {' '.join([hex(b)[2:].zfill(2) for b in settings])}")
            new_settings, _ = self.bytes_to_dict(settings, self.settings)
            self.validate_settings(new_settings)
            self.plc_settings_download_request_flag = False
            self.state.frontend_update_required = True

        print(f"new settings: {self.settings}")
        write_dataclass_to_file(self.settings, 'settings_save.pkl')
        self.cam_update_request_flag = True

    def get_settings(self, as_byte_stream=False):
        if not as_byte_stream:
            return self.settings
        return self.dict_to_bytes(asdict(self.settings))

    def get_state(self, as_byte_stream=False):
        if not as_byte_stream:
            return self.state
        return self.dict_to_bytes(asdict(self.state))

    def get_settings_from_PLC(self):
        self.plc_settings_download_request_flag = True

    def validate_settings(self, new_settings: SettingsStructure):
        self.settings = new_settings
        self.settings.colourFilter.hue = clamp_max_min(new_settings.colourFilter.hue, 0, 255)
        self.settings.colourFilter.saturation = clamp_max_min(new_settings.colourFilter.saturation, 0, 255)
        self.settings.colourFilter.value = clamp_max_min(new_settings.colourFilter.value, 0, 255)
        self.settings.filter_1 = clamp(new_settings.filter_1, 0, 30)
        self.settings.filter_2 = clamp(new_settings.filter_2, 0, 30)
        self.settings.cam_settings.frame_cutout = clamp_max_min(new_settings.cam_settings.frame_cutout, 0, 3000,
                                                                min_distance=50)

    def get_cam_settings(self):
        return self.settings.cam_settings

    def dict_to_bytes(self, dictionary):
        bytestream = b''
        previous_data_type_was_bool = False
        for key, value in dictionary.items():

            if isinstance(value, bool):
                previous_data_type_was_bool = True
            if not isinstance(value, bool) and not isinstance(value, dict):
                previous_data_type_was_bool = False

            if isinstance(value, int):
                new_bytes = struct.pack('<h', value)
                bytestream += new_bytes
            elif isinstance(value, bool):
                new_bytes = struct.pack('<?', value)
                bytestream += new_bytes + b'0'

            elif isinstance(value, float):
                while len(bytestream) % 4 != 0:
                    bytestream += b'0'
                new_bytes = struct.pack('<f', value)
                bytestream += new_bytes
            elif isinstance(value, dict):
                # every structure starts at a byte dividable by 4
                div = 4
                if previous_data_type_was_bool:
                    div = 2
                while len(bytestream) % div != 0:
                    bytestream += b'0'
                bytestream += self.dict_to_bytes(value)
            else:
                print(f"key: {key}, value: {value} is of unsupported type {type(value)} detected")
        return bytestream

    def bytes_to_dict(self, data, current_settings, index=0):
        new_settings = current_settings
        try:
            previous_data_type_was_bool = False
            for field in fields(new_settings):

                if field.type == bool:
                    previous_data_type_was_bool = True
                if field.type != bool and not is_dataclass(getattr(new_settings, field.name)):
                    previous_data_type_was_bool = False

                if field.type == int:
                    sub_data = data[index:index + 2]
                    index += 2
                    (new_value,) = struct.unpack('<h', sub_data)
                    # print(f'setting {field.name} at byte: {index-2} to {new_value}')
                    setattr(new_settings, field.name, new_value)
                elif field.type == bool:
                    sub_data = data[index:index + 1]
                    index += 2
                    (new_value,) = struct.unpack('<?', sub_data)
                    # print(f'setting {field.name} at byte: {index - 2} to {new_value}')
                    setattr(new_settings, field.name, new_value)
                elif field.type == float:
                    index = index + index % 4
                    sub_data = data[index:index + 4]
                    index += 4
                    (new_value,) = struct.unpack('<f', sub_data)
                    # print(f'setting {field.name} at byte: {index - 4} to {new_value}')
                    setattr(new_settings, field.name, new_value)
                elif is_dataclass(getattr(new_settings, field.name)):
                    # make sure that index is dividable by 4 or 2
                    # because data structs in the plc are always a multiple of 4 or 2 depending on previous dt
                    if previous_data_type_was_bool:
                        index = index + index % 2
                    else:
                        index = index + index % 4
                    # print(f'{field.name} at index: {index}')
                    new_value, index = self.bytes_to_dict(data, getattr(new_settings, field.name), index)
                    index = index + index % 4
                    setattr(new_settings, field.name, new_value)
                else:
                    print(f"key: {field.name}, of unsupported type {field.type} detected")
            return new_settings, index
        except struct.error as e:
            print(e)
            return current_settings, index

    def set_cam_connection_state(self, state):
        self.state.camera_connected = state
        self.plc_state_update_request_flag = True

    def set_PLC_connection_state(self, state):
        self.state.PLC_connected = state
        self.plc_state_update_request_flag = True

    def set_log_state(self, logging_active=False, replay_active=False, progress=0.0):
        self.state.logging_active = logging_active
        self.state.replay_active = replay_active
        self.state.log_progress = progress

    def adjust_exposure(self, value):
        self.settings.cam_settings.ExposureTime += value * 100
        self.cam_exposure_update_flag = True
        self.state.frontend_update_required = True

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def clamp_max_min(n: MaxMin, smallest, largest, min_distance=1):
    n.min = clamp(n.min, smallest, largest - min_distance)
    n.max = clamp(n.max, n.min + min_distance, largest)
    return n


class MessageType(Enum):
    LINE_VALUE = 0
    SETTINGS_SET = 1
    SETTINGS_GET = 3
    IDLE = 4
    STATE_SET = 5


def check_dataclass_structure(obj, dataclass_type):
    if not (isinstance(obj, dataclass_type) and is_dataclass(obj)):
        return False

    expected_fields = {f.name for f in fields(dataclass_type)}
    actual_fields = set(obj.__dict__.keys())

    return expected_fields == actual_fields


if __name__ == '__main__':
    settings = Interface()
    settings.set_settings(bytearray(b'\x00\x16\x00\x00\x00\xf7\x00B\x00\xff\x008\x00\x05\x00\x05\x08\xfc\x03 '))
    print(settings.get_settings(as_byte_stream=True))
    print(settings.get_settings(as_byte_stream=False))
