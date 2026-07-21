import random
from dataclasses import replace

from config.const import (
    CROSSOVER_RATE,
    ELITISM_RATE,
    GENERATIONS,
    MAX_DEFAULT_NUMBER_OF_MODULES,
    MUTATION_RATE,
    POPULATION_SIZE,
    TOP_RESULTS_COUNT,
    TOURNAMENT_SIZE
)
from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.ga_data import GAData
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.inverter_dto import InverterDto
from pv_design.dto.pv_module_dto import PvModuleDto
from pv_design.services.genetic_algorithm.chromosome_provider import ChromosomeProvider
from pv_design.services.genetic_algorithm.fitness_service import FitnessService
from pv_design.services.genetic_algorithm.ga_data_provider import GADataProvider
from pv_design.services.installation_checker import InstallationChecker


class GeneticAlgorithmService:
    _MODULE_COUNT_SIGMA = MAX_DEFAULT_NUMBER_OF_MODULES / 4

    def __init__(
        self,
        client_requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
        population_size: int = POPULATION_SIZE,
        mutation_rate: float = MUTATION_RATE,
        crossover_rate: float = CROSSOVER_RATE,
        elitism_rate: float = ELITISM_RATE,
        generations: int = GENERATIONS,
        tournament_size: int = TOURNAMENT_SIZE,
    ):
        self.client_requirements = client_requirements
        self.installation_site = installation_site
        self.generations = generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.chromosome_provider = ChromosomeProvider()
        self.ga_data_provider = GADataProvider()
        self.checker = InstallationChecker()
        self.fitness_service = FitnessService()
        self._ga_data: GAData = self.ga_data_provider.load_data()
        self.population: list[InstallationDto] = self._initialize_population(population_size)
        self.tournament_size = tournament_size

    def _initialize_population(self, population_size: int) -> list[InstallationDto]:
        return [self.chromosome_provider.get_random() for _ in range(population_size)]

    def run(self) -> list[InstallationDto]:
        top: list[tuple[InstallationDto, float]] = []

        for _ in range(self.generations):
            scored = [
                (individual, self.fitness_service.calculate(
                    individual, self.client_requirements, self.installation_site
                ))
                for individual in self.population
            ]

            for individual, fitness in scored:
                self._update_top_results(top, individual, fitness)

            elite_count = max(1, int(self.population_size * self.elitism_rate))
            elites = self._select_elite(scored, elite_count)
            new_population = list[InstallationDto](elites)

            while len(new_population) < self.population_size:
                parent1 = self._select_parent(scored)
                parent2 = self._select_parent(scored)

                if random.random() < self.crossover_rate:
                    offspring = self._crossover(parent1, parent2)
                else:
                    offspring = replace(parent1)

                offspring = self._mutate(offspring)
                new_population.append(offspring)

            self.population = new_population[: self.population_size]

        return [individual for individual, _ in top]

    def _update_top_results(
        self,
        top: list[tuple[InstallationDto, float]],
        individual: InstallationDto,
        fitness: float,
    ) -> None:
        if fitness <= 0 or not self.checker.check(individual):
            return

        for index, (existing, existing_fitness) in enumerate(top):
            if self._is_same_installation(existing, individual):
                if fitness > existing_fitness:
                    top[index] = (individual, fitness)
                return

        top.append((individual, fitness))
        top.sort(key=lambda item: item[1], reverse=True)
        del top[TOP_RESULTS_COUNT:]

    def _is_same_installation(
        self,
        first: InstallationDto,
        second: InstallationDto,
    ) -> bool:
        return (
            first.inverter == second.inverter
            and first.module_type == second.module_type
            and first.module_count == second.module_count
        )

    def _select_elite(
        self,
        scored: list[tuple[InstallationDto, float]],
        count: int,
    ) -> list[InstallationDto]:
        valid = [
            (individual, fitness)
            for individual, fitness in scored
            if self.checker.check(individual) and fitness > 0
        ]
        valid.sort(key=lambda item: item[1], reverse=True)
        return [individual for individual, _ in valid[:count]]

    def _select_parent(
        self,
        scored: list[tuple[InstallationDto, float]],
    ) -> InstallationDto:
        tournament = random.sample(scored, min(self.tournament_size, len(scored)))
        return max(tournament, key=lambda item: item[1])[0]

    def _crossover(
        self,
        parent1: InstallationDto,
        parent2: InstallationDto,
    ) -> InstallationDto:
        crossover_inverter = random.choice([True, False])
        crossover_module_type = random.choice([True, False])
        crossover_module_count = random.choice([True, False])

        if crossover_inverter:
            inverter = random.choice([parent1.inverter, parent2.inverter])
        else:
            inverter = parent1.inverter

        if crossover_module_type:
            module_type = random.choice([parent1.module_type, parent2.module_type])
        else:
            module_type = parent1.module_type

        if crossover_module_count:
            average_count = (parent1.module_count + parent2.module_count) / 2
            module_count = self._perturb_module_count(average_count)
        else:
            module_count = parent1.module_count

        return InstallationDto(
            inverter=inverter,
            module_type=module_type,
            module_count=module_count,
        )

    def _mutate(self, individual: InstallationDto) -> InstallationDto:
        inverter = individual.inverter
        module_type = individual.module_type
        module_count = individual.module_count

        if random.random() < self.mutation_rate:
            inverter = self._pick_different_inverter(inverter)

        if random.random() < self.mutation_rate:
            module_type = self._pick_different_module(module_type)

        if random.random() < self.mutation_rate:
            module_count = self._perturb_module_count(individual.module_count)

        return InstallationDto(
            inverter=inverter,
            module_type=module_type,
            module_count=module_count,
        )

    def _perturb_module_count(self, base: float) -> int:
        value = random.gauss(base, self._MODULE_COUNT_SIGMA)
        return max(1, min(MAX_DEFAULT_NUMBER_OF_MODULES, round(value)))

    def _pick_different_inverter(self, current: InverterDto) -> InverterDto:
        alternatives = [
            inverter for inverter in self._ga_data.inverters if inverter != current
        ]
        if not alternatives:
            return current
        return random.choice(alternatives)

    def _pick_different_module(self, current: PvModuleDto) -> PvModuleDto:
        alternatives = [
            module for module in self._ga_data.modules if module != current
        ]
        if not alternatives:
            return current
        return random.choice(alternatives)
