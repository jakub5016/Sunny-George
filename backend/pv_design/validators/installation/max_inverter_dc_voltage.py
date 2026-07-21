from pv_design.validators.installation.installation_validator import InstallationValidator
from django.db.models import Max
from pv_design.dto.pv_module_dto import PvModuleDto
from pv_design.dto.installation_dto import InstallationDto
from config.const import DEFAULT_MIN_TEMP_C


class MaxInverterDcVoltageValidator(InstallationValidator):

    def calculate_cold_voc(self, module: PvModuleDto, min_temp: float) -> float:
        delta = 25 - min_temp

        return module.voc * (
            1
            + abs(module.temperature_coefficient_percent_per_c)
            * delta
            / 100
        )

    def validate(self, installation: InstallationDto) -> bool:
        module = installation.module_type
        
        cold_voc = self.calculate_cold_voc(module, DEFAULT_MIN_TEMP_C)

        return cold_voc <= installation.inverter.max_dc_voltage