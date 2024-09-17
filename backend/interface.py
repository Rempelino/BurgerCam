from dataclasses import dataclass, asdict
from typing import Union
from enum import Enum
import json

@dataclass
class MaxMin:
    max: float
    min: float


@dataclass
class ColourFilter:
    hue: MaxMin
    saturation: MaxMin
    value: MaxMin


@dataclass
class SettingsStructure:
    colourFilter: ColourFilter
    filter_1: float
    filter_2: float


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
            values = list(settings)
            self.settings.colourFilter.hue.max = values[0]
            self.settings.colourFilter.hue.min = values[1]
            self.settings.colourFilter.saturation.max = values[2]
            self.settings.colourFilter.saturation.min = values[3]
            self.settings.colourFilter.value.max = values[4]
            self.settings.colourFilter.value.min = values[5]
            self.settings.filter_1 = values[6]
            self.settings.filter_2 = values[7]
        print(f"Settings set to: {self.settings}")

    def get_settings(self, as_byte_stream=False):
        if not as_byte_stream:
            return self.settings
        data = json.dumps(asdict(self.settings)).encode('utf-8')
        data = self.extract_values_from_json_bytes(data)
        data = bytes(data)
        print(f"byte data: {data}")
        return data

    @staticmethod
    def get_defaults() -> SettingsStructure:
        return SettingsStructure(
            colourFilter=ColourFilter(
                hue=MaxMin(max=22, min=0),
                saturation=MaxMin(max=247, min=66),
                value=MaxMin(max=255, min=56)
            ),
            filter_1=5,
            filter_2=5
        )

    @staticmethod
    def extract_values_from_json_bytes(byte_data):
        # Decode bytes to string
        json_str = byte_data.decode('utf-8')

        # Parse JSON
        data = json.loads(json_str)

        # Extract values
        values = []

        # Handle nested dictionary
        for key, value in data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict):
                        values.extend(sub_value.values())
                    else:
                        values.append(sub_value)
            else:
                values.append(value)

        return values


class MessageType(Enum):
    LINE_VALUE = 0
    SETTINGS = 1
    ALIVE = 2
    REQUEST_SETTINGS = 3
    IDLE = 4
    PLC_CONFIRM = 5

