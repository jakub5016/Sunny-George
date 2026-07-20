from dataclasses import dataclass

@dataclass
class ClientRequirementsDto:
    installation_area_m2: float
    installation_power_kw: float
    max_pln_budget: float