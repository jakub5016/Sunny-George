from dataclasses import dataclass

@dataclass
class InstallationMetrics:
    installation_area_m2: float
    installation_power_kw: float
    total_cost_pln: float
