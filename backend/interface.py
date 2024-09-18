from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Union
from enum import Enum
import json
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
class SettingsStructure:
    colourFilter: ColourFilter
    filter_1: int
    filter_2: int
    frame_cutout: MaxMin


class Settings:
    plc_update_request_flag = False

    def __init__(self):
        self.settings: SettingsStructure = self.get_defaults()

    def set_settings(self, settings: Union[SettingsStructure, bytearray]):

        # settings changed by frontend
        if isinstance(settings, SettingsStructure):
            self.settings = settings
            self.plc_update_request_flag = True

        # settings changed by plc
        else:

            self.settings, _ = self.bytes_to_dict(settings, SettingsStructure, self.settings)
            print(f'settings updated by PLC: {self.settings}')



    def get_settings(self, as_byte_stream=False):
        if not as_byte_stream:
            return self.settings
        return self.dict_to_bytes(asdict(self.settings))

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
            frame_cutout=MaxMin(max=2300, min=800)
        )

    def dict_to_bytes(self, dictionary):
        bytestream = b''
        for key, value in dictionary.items():
            if isinstance(value, int):
                new_bytes = struct.pack('>h', value)
                bytestream += new_bytes
            elif isinstance(value, dict):
                bytestream += self.dict_to_bytes(value)
            else:
                print(f"key: {key}, value: {value} is of unsupported type {type(value)} detected")
        return bytestream

    def bytes_to_dict(self, data, data_class, current_settings, index=0):

        new_settings = current_settings

        for field in fields(new_settings):
            if field.type == int:
                sub_data = data[index:index + 2]
                index += 2
                (new_value,) = struct.unpack('>h', sub_data)
                setattr(new_settings, field.name, new_value)
            elif is_dataclass(getattr(new_settings, field.name)):
                new_value, index = self.bytes_to_dict(data, field.type, getattr(new_settings, field.name), index)
                setattr(new_settings, field.name, new_value)
            else:
                print(f"key: {field.name}, of unsupported type {field.type} detected")
        return new_settings, index


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
