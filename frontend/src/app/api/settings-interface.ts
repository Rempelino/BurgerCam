export interface SettingsStructure {
    colourFilter: ColourFilter;
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