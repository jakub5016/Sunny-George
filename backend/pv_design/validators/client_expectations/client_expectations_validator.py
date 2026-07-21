from abc import ABC, abstractmethod

from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto


class ClientExpectationsValidator(ABC):
    @abstractmethod
    def validate(
        self,
        installation: InstallationDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> bool:
        pass
