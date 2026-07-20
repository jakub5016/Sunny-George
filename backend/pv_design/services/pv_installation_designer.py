from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.pv_design_result_dto import PvDesignResultDto
from pv_design.services.client_expectations_checker import ClientExpectationsChecker
from pv_design.services.genetic_algorithm.genetic_algorithm_service import GeneticAlgorithmService
from pv_design.services.installation_checker import InstallationChecker


class PvInstallationDesigner:
    def __init__(self) -> None:
        self.installation_checker = InstallationChecker()
        self.client_expectations_checker = ClientExpectationsChecker()

    def _create_installations(
        self,
        client_requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
        *,
        generations: int | None = None,
        population_size: int | None = None,
    ) -> list[InstallationDto]:
        ga_kwargs = {}
        if generations is not None:
            ga_kwargs["generations"] = generations
        if population_size is not None:
            ga_kwargs["population_size"] = population_size

        genetic_algorithm = GeneticAlgorithmService(
            client_requirements, installation_site, **ga_kwargs
        )
        return genetic_algorithm.run()

    def _filter_candidates(
        self,
        candidates: list[InstallationDto],
        client_requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> PvDesignResultDto:
        matching: list[InstallationDto] = []
        alternative: list[InstallationDto] = []

        for installation in candidates:
            if not self.installation_checker.check(installation):
                continue
            if self.client_expectations_checker.check(
                installation, client_requirements, installation_site
            ):
                matching.append(installation)
            else:
                alternative.append(installation)

        return PvDesignResultDto(
            matching_installations=matching,
            alternative_installations=alternative,
        )

    def design(
        self,
        client_requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
        *,
        generations: int | None = None,
        population_size: int | None = None,
    ) -> PvDesignResultDto:
        candidates = self._create_installations(
            client_requirements,
            installation_site,
            generations=generations,
            population_size=population_size,
        )
        return self._filter_candidates(candidates, client_requirements, installation_site)
