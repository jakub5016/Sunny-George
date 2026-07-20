from dataclasses import dataclass

from pv_design.dto.installation_dto import InstallationDto


@dataclass
class PvDesignResultDto:
    matching_installations: list[InstallationDto]
    alternative_installations: list[InstallationDto]
