from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.services.installation_metrics_service import InstallationMetricsService
from pv_design.validators.client_expectations.client_expectations_validator import (
    ClientExpectationsValidator,
)


class MinPowerValidator(ClientExpectationsValidator):
    def __init__(self) -> None:
        self.metrics_service = InstallationMetricsService()

    def validate(
        self,
        installation: InstallationDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> bool:
        metrics = self.metrics_service.calculate(installation, installation_site)

        return metrics.installation_power_kw >= requirements.installation_power_kw
