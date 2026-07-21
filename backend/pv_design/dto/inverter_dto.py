from dataclasses import dataclass

@dataclass
class InverterDto:
    id: int
    name: str
    price_pln: float
    max_dc_voltage: float
    mppt_min: float
    mppt_max: float
    max_dc_power: float
    phases: str
    max_mppt_current: float