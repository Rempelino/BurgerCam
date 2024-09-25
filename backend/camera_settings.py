from dataclasses import dataclass


@dataclass
class CamSettings:
    ReverseX: bool
    ReverseY: bool
    ExposureTime: float
    ColorTransformationEnable: bool


def get_default_cam_settings() -> CamSettings:
    return CamSettings(
        ReverseX=False,
        ReverseY=False,
        ExposureTime=40000.0,
        ColorTransformationEnable=False
    )
