from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Union
from enum import Enum
from camera_settings import CamSettings, get_default_cam_settings
import struct


@dataclass
class MaxMin:
    max: int
    min: int


@dataclass
class ColourFilter:
    hue: MaxMin
    saturation: MaxMin
    value: MaxMin


@dataclass
class CameraSettings:
    ColorTransformationEnable: bool


@dataclass
class SettingsStructure:
    colourFilter: ColourFilter
    filter_1: int
    filter_2: int
    frame_cutout: MaxMin
    lines: int
    cam_settings: CamSettings


class Settings:
    plc_update_request_flag = False
    cam_update_request_flag = False

    def __init__(self):
        self.settings: SettingsStructure = self.get_defaults()

    def set_settings(self, settings: Union[SettingsStructure, bytearray]):

        # settings changed by frontend
        if isinstance(settings, SettingsStructure):
            self.validate_settings(settings)
            self.plc_update_request_flag = True

        # settings changed by plc
        else:
            new_settings, _ = self.bytes_to_dict(settings, self.settings)
            self.validate_settings(new_settings)
        self.cam_update_request_flag = True

    def get_settings(self, as_byte_stream=False):
        if not as_byte_stream:
            return self.settings
        return self.dict_to_bytes(asdict(self.settings))

    def validate_settings(self, new_settings: SettingsStructure):
        self.settings.colourFilter.hue = clamp_max_min(new_settings.colourFilter.hue, 0, 255)
        self.settings.colourFilter.saturation = clamp_max_min(new_settings.colourFilter.saturation, 0, 255)
        self.settings.colourFilter.value = clamp_max_min(new_settings.colourFilter.value, 0, 255)

        self.settings.filter_1 = clamp(new_settings.filter_1, 0, 30)
        self.settings.filter_2 = clamp(new_settings.filter_2, 0, 30)

        self.settings.frame_cutout = clamp_max_min(new_settings.frame_cutout, 0, 3000)

    def get_cam_settings(self):
        return self.settings.cam_settings

    @staticmethod
    def get_defaults() -> SettingsStructure:
        return SettingsStructure(
            colourFilter=ColourFilter(
                hue=MaxMin(max=22, min=0),
                saturation=MaxMin(max=247, min=66),
                value=MaxMin(max=255, min=56)
            ),
            filter_1=5,
            filter_2=5,
            frame_cutout=MaxMin(max=2300, min=800),
            lines=6,
            cam_settings=get_default_cam_settings()
        )

    def dict_to_bytes(self, dictionary):
        bytestream = b''
        for key, value in dictionary.items():
            if isinstance(value, int):
                new_bytes = struct.pack('<h', value)
                bytestream += new_bytes
            if isinstance(value, bool):
                new_bytes = struct.pack('<?', value)
                bytestream += new_bytes + b'0'
            if isinstance(value, float):
                new_bytes = struct.pack('<f', value)
                bytestream += new_bytes
            elif isinstance(value, dict):
                bytestream += self.dict_to_bytes(value)
            else:
                print(f"key: {key}, value: {value} is of unsupported type {type(value)} detected")
        return bytestream

    def bytes_to_dict(self, data, current_settings, index=0):
        new_settings = current_settings
        try:
            for field in fields(new_settings):
                if field.type == int:
                    sub_data = data[index:index + 2]
                    index += 2
                    (new_value,) = struct.unpack('<h', sub_data)
                    setattr(new_settings, field.name, new_value)
                elif field.type == bool:
                    sub_data = data[index:index + 1]
                    index += 2
                    (new_value,) = struct.unpack('<?', sub_data)
                    setattr(new_settings, field.name, new_value)
                elif field.type == float:
                    sub_data = data[index:index + 4]
                    index += 4
                    (new_value,) = struct.unpack('<f', sub_data)
                    setattr(new_settings, field.name, new_value)
                elif is_dataclass(getattr(new_settings, field.name)):
                    # make sure that index is dividable by 4
                    # because data structs in the plc always start every 4th byte
                    index = index + index % 4
                    new_value, index = self.bytes_to_dict(data, getattr(new_settings, field.name), index)
                    setattr(new_settings, field.name, new_value)
                else:
                    print(f"key: {field.name}, of unsupported type {field.type} detected")
            return new_settings, index
        except struct.error as e:
            print(e)
            return current_settings, index


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def clamp_max_min(n: MaxMin, smallest, largest, min_distance=1):
    n.min = clamp(n.min, smallest, largest - min_distance)
    n.max = clamp(n.max, n.min + min_distance, largest)
    return n


class MessageType(Enum):
    LINE_VALUE = 0
    SETTINGS = 1
    ALIVE = 2
    REQUEST_SETTINGS = 3
    IDLE = 4
    PLC_CONFIRM = 5


if __name__ == '__main__':
    settings = Settings()
    settings.set_settings(bytearray(b'\x00\x16\x00\x00\x00\xf7\x00B\x00\xff\x008\x00\x05\x00\x05\x08\xfc\x03 '))
    print(settings.get_settings(as_byte_stream=True))
    print(settings.get_settings(as_byte_stream=False))
