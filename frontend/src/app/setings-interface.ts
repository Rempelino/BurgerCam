export interface SettingsStructure {
    colourFilter: ColourFilter;
    filter_1: number;
    filter_2: number;
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