from dataclasses import dataclass

from pv_design.dto.inverter_dto import InverterDto
from pv_design.dto.pv_module_dto import PvModuleDto

@dataclass
class GAData:
    modules: list[PvModuleDto]
    inverters: list[InverterDto]

