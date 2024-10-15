from dataclasses import dataclass, field


@dataclass
class MaxMin:
    max: int = 0
    min: int = 0


@dataclass
class CamSettings:
    ReverseX: bool = False
    ReverseY: bool = False
    ExposureTime: float = 0.0
    ColorTransformationEnable: bool = False
    frame_cutout: MaxMin = field(default_factory=MaxMin)


@dataclass
class ColourFilter:
    hue: MaxMin = field(default_factory=MaxMin)
    saturation: MaxMin = field(default_factory=MaxMin)
    value: MaxMin = field(default_factory=MaxMin)


@dataclass
class State:
    camera_connected: bool = False
    PLC_connected: bool = False
    frontend_update_required: bool = False
    logging_active: bool = False
    replay_active: bool = False
    log_progress: float = 0.0


@dataclass
class SettingsStructure:
    colourFilter: ColourFilter = field(default_factory=ColourFilter)
    filter_1: int = 0
    filter_2: int = 0
    fisheye: float = 0.1
    lines: int = 6
    cam_settings: CamSettings = field(default_factory=CamSettings)
