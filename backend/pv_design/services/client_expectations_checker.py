from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.validators.client_expectations.client_expectations_validator import (
    ClientExpectationsValidator,
)
from pv_design.validators.client_expectations.max_area_validator import MaxAreaValidator
from pv_design.validators.client_expectations.max_price_validator import MaxPriceValidator
from pv_design.validators.client_expectations.min_power_validator import MinPowerValidator


class ClientExpectationsChecker:
    def __init__(self) -> None:
        self.validators: list[ClientExpectationsValidator] = [
            MaxPriceValidator(),
            MinPowerValidator(),
            MaxAreaValidator(),
        ]

    def check(
        self,
        installation: InstallationDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> bool:
        for validator in self.validators:
            if not validator.validate(installation, requirements, installation_site):
                return False
        return True
