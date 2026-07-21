from pv_design.validators.installation.installation_validator import InstallationValidator
from pv_design.dto.installation_dto import InstallationDto

class MpptMinValidator(InstallationValidator):
    def validate(self, installation: InstallationDto) -> bool:
        module = installation.module_type
        string_vmp = module.vmp * installation.module_count

        return string_vmp >= installation.inverter.mppt_min 