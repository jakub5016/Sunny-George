from pv_design.validators.installation.installation_validator import InstallationValidator
from pv_design.validators.installation.max_inverter_dc_voltage import MaxInverterDcVoltageValidator
from pv_design.validators.installation.mppt_max import MpptMaxValidator
from pv_design.validators.installation.mppt_min import MpptMinValidator
from pv_design.validators.installation.current_input import CurrentInputValidator
from pv_design.validators.installation.dc_power_inverter import DcPowerInverterValidator
from pv_design.dto.installation_dto import InstallationDto

class InstallationChecker:
    def __init__(self):
        self.validators: list[InstallationValidator] = [
            CurrentInputValidator(),
            DcPowerInverterValidator(),
            MaxInverterDcVoltageValidator(),
            MpptMaxValidator(),
            MpptMinValidator(),
        ]

    def check(self, installation: InstallationDto) -> bool:
        for validator in self.validators:
            if not validator.validate(installation):
                return False
        return True