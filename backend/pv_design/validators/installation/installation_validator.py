from abc import ABC, abstractmethod

from pv_design.dto.installation_dto import InstallationDto


class InstallationValidator(ABC):
    @abstractmethod
    def validate(self, installation: InstallationDto) -> bool:
        pass
