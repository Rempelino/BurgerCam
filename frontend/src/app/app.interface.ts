import exp from "constants";

export interface CamSettings{
    ReverseX: boolean;
    ReverseY: boolean;
    ExposureTime: number;
    ColorTransformationEnable: boolean;
}

export interface ColourFilter {
    hue: MaxMin;
    saturation: MaxMin;
    value: MaxMin;
}

export interface MaxMin {
    max: number;
    min: number;
}

export interface ColourFilter {
    hue: MaxMin;
    saturation: MaxMin;
    value: MaxMin;
}

export interface Status {
    camera_connected: boolean;
    PLC_connected: boolean;
}

export interface SettingsStructure {
    colourFilter: ColourFilter;
    filter_1: number;
    filter_2: number;
    frame_cutout: MaxMin;
    lines: number;
    cam_settings: CamSettings;
    status: Status;
}