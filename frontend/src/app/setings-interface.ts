export interface SettingsStructure {
    colourFilter: ColourFilter;
    filter_1: number;
    filter_2: number;
    frame_cutout: MaxMin;
    lines: number;
    cam_settings: CamSettings;
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

export interface CamSettings{
    ReverseX: boolean;
    ReverseY: boolean;
    ExposureTime: number;
    ColorTransformationEnable: boolean;
}
