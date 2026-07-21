from dataclasses import dataclass

@dataclass
class PvModuleDto:
    id: int
    name: str
    power_watt: float
    efficiency_percent: float
    price_pln: float
    height_cm: float
    width_cm: float
    voc: float
    vmp: float
    Imp: float
    temperature_coefficient_percent_per_c: float