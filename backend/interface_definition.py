from dataclasses import dataclass, field


@dataclass
class CamSettings:
    ReverseX: bool = False
    ReverseY: bool = False
    ExposureTime: float = 0.0
    ColorTransformationEnable: bool = False


@dataclass
class MaxMin:
    max: int = 0
    min: int = 0


@dataclass
class ColourFilter:
    hue: MaxMin = field(default_factory=MaxMin)
    saturation: MaxMin = field(default_factory=MaxMin)
    value: MaxMin = field(default_factory=MaxMin)


@dataclass
class State:
    camera_connected: bool = False
    PLC_connected: bool = False


@dataclass
class SettingsStructure:
    colourFilter: ColourFilter = field(default_factory=ColourFilter)
    filter_1: int = 0
    filter_2: int = 0
    fisheye: float = 0.1
    frame_cutout: MaxMin = field(default_factory=MaxMin)
    lines: int = 6
    cam_settings: CamSettings = field(default_factory=CamSettings)
