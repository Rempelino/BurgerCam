import exp from "constants";

export interface MaxMin {
    max: number;
    min: number;
}

export interface CamSettings{
    ReverseX: boolean;
    ReverseY: boolean;
    ExposureTime: number;
    ColorTransformationEnable: boolean;
    frame_cutout: MaxMin;
}

export interface ColourFilter {
    hue: MaxMin;
    saturation: MaxMin;
    value: MaxMin;
}


export interface ColourFilter {
    hue: MaxMin;
    saturation: MaxMin;
    value: MaxMin;
}

export interface State {
    camera_connected: boolean;
    PLC_connected: boolean;
}

export interface SettingsStructure {
    colourFilter: ColourFilter;
    filter_1: number;
    filter_2: number;
    fisheye: number;
    lines: number;
    cam_settings: CamSettings;
}