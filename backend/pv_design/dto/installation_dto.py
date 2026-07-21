from dataclasses import dataclass
from pv_design.dto.pv_module_dto import PvModuleDto
from pv_design.dto.inverter_dto import InverterDto

@dataclass
class InstallationDto:
    inverter: InverterDto
    module_type: PvModuleDto
    module_count: int