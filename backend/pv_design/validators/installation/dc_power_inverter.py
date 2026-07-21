from pv_design.validators.installation.installation_validator import InstallationValidator
from pv_design.dto.installation_dto import InstallationDto

class DcPowerInverterValidator(InstallationValidator):
    def validate(self, installation: InstallationDto) -> bool:
        ratio =  (
            installation.module_type.power_watt * installation.module_count
        ) / installation.inverter.max_dc_power
        return ratio <= 1.5