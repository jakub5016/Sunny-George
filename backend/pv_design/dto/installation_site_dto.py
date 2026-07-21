from dataclasses import dataclass


@dataclass
class InstallationSiteDto:
    roof_angle: float | None
    on_roof_installation: bool
    installation_area_m2: float
    distance_from_inverter_to_modules_m: float
    shading_likert: int