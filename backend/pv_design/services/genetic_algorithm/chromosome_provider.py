from random import randint

from config.const import MAX_DEFAULT_NUMBER_OF_MODULES
from pv_design.dto.ga_data import GAData
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.inverter_dto import InverterDto
from pv_design.dto.pv_module_dto import PvModuleDto
from pv_design.services.genetic_algorithm.ga_data_provider import GADataProvider


class ChromosomeProvider:
    def __init__(self) -> None:
        self._ga_data_provider = GADataProvider()

    def get_random(self) -> InstallationDto:
        ga_data: GAData = self._ga_data_provider.load_data()

        inverters: list[InverterDto] = ga_data.inverters
        modules: list[PvModuleDto] = ga_data.modules

        selected_inverter: InverterDto = inverters[randint(0, len(inverters) - 1)]
        selected_module: PvModuleDto = modules[randint(0, len(modules) - 1)]
        selected_number_of_modules: int = randint(1, MAX_DEFAULT_NUMBER_OF_MODULES)

        return InstallationDto(
            inverter=selected_inverter,
            module_type=selected_module,
            module_count=selected_number_of_modules,
        )