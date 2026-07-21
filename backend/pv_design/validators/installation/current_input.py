from pv_design.validators.installation.installation_validator import InstallationValidator
from pv_design.dto.installation_dto import InstallationDto

class CurrentInputValidator(InstallationValidator):
    def validate(self, installation: InstallationDto) -> bool:
        return installation.module_type.Imp <= installation.inverter.max_mppt_current