from dataclasses import dataclass


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
    gap_filler: float


class Settings:
    def __init__(self):
        self.settings = self.get_defaults()

    def set_settings(self, settings: SettingsStructure):
        self.settings = settings

    def get_settings(self):
        return self.settings

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
            gap_filler=50
        )
