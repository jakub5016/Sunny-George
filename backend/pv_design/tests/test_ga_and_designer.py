from unittest.mock import patch

from django.test import TestCase

from pv_design.dto.ga_data import GAData
from pv_design.services.genetic_algorithm.chromosome_provider import ChromosomeProvider
from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache
from pv_design.services.genetic_algorithm.ga_data_provider import GADataProvider
from pv_design.services.genetic_algorithm.genetic_algorithm_service import GeneticAlgorithmService
from pv_design.services.pv_installation_designer import PvInstallationDesigner
from pv_design.tasks.clear_ga_data_cache import ClearGADataCache
from pv_elements.models import Inverter, PvModule
from pv_elements.models.types.phase_type import PhaseType

from .fixtures import (
    make_inverter,
    make_installation,
    make_installation_site,
    make_module,
    make_requirements,
)


class GADataProviderTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.module = PvModule.objects.create(
            name="GA Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
            height_cm=170,
            width_cm=100,
            voc=40,
            vmp=33,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        cls.inverter = Inverter.objects.create(
            name="GA Inverter",
            price_pln=3000,
            max_dc_voltage=600,
            mppt_min=100,
            mppt_max=500,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=15,
        )

    def setUp(self) -> None:
        GADataCache().clear_cache()

    def test_load_data_reads_from_database(self) -> None:
        data = GADataProvider().load_data()

        self.assertEqual(len(data.modules), 1)
        self.assertEqual(len(data.inverters), 1)
        self.assertEqual(data.modules[0].name, "GA Module")

    def test_load_data_uses_cache_on_second_call(self) -> None:
        provider = GADataProvider()
        first = provider.load_data()

        with patch.object(provider, "get_modules") as mock_get_modules:
            second = provider.load_data()
            mock_get_modules.assert_not_called()

        self.assertIs(first, second)


class ChromosomeProviderTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        PvModule.objects.create(
            name="Chromosome Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
            height_cm=170,
            width_cm=100,
            voc=40,
            vmp=33,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        Inverter.objects.create(
            name="Chromosome Inverter",
            price_pln=3000,
            max_dc_voltage=600,
            mppt_min=100,
            mppt_max=500,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=15,
        )

    def setUp(self) -> None:
        GADataCache().clear_cache()

    def test_get_random_returns_installation_dto(self) -> None:
        installation = ChromosomeProvider().get_random()

        self.assertGreaterEqual(installation.module_count, 1)
        self.assertIsNotNone(installation.inverter.name)
        self.assertIsNotNone(installation.module_type.name)


class GeneticAlgorithmServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        PvModule.objects.create(
            name="GA Module A",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
            height_cm=170,
            width_cm=100,
            voc=40,
            vmp=33,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        PvModule.objects.create(
            name="GA Module B",
            power_watt=450,
            efficiency_percent=21,
            price_pln=900,
            height_cm=170,
            width_cm=100,
            voc=41,
            vmp=34,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        Inverter.objects.create(
            name="GA Inverter A",
            price_pln=3000,
            max_dc_voltage=600,
            mppt_min=100,
            mppt_max=500,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=15,
        )
        Inverter.objects.create(
            name="GA Inverter B",
            price_pln=3500,
            max_dc_voltage=650,
            mppt_min=110,
            mppt_max=520,
            max_dc_power=5500,
            phases=PhaseType.THREE,
            max_mppt_current=16,
        )

    def setUp(self) -> None:
        GADataCache().clear_cache()
        self.requirements = make_requirements()
        self.site = make_installation_site()

    def test_run_returns_list_of_installations(self) -> None:
        service = GeneticAlgorithmService(
            self.requirements,
            self.site,
            population_size=4,
            generations=2,
        )
        results = service.run()

        self.assertIsInstance(results, list)
        for installation in results:
            self.assertGreater(installation.module_count, 0)

    def test_crossover_and_mutate_produce_valid_dto(self) -> None:
        service = GeneticAlgorithmService(
            self.requirements,
            self.site,
            population_size=2,
            generations=1,
        )
        parent1 = make_installation(module_count=4)
        parent2 = make_installation(
            inverter=make_inverter(id=2, name="Other"),
            module_type=make_module(id=2, name="Other module"),
            module_count=8,
        )

        offspring = service._crossover(parent1, parent2)
        self.assertGreaterEqual(offspring.module_count, 1)

        mutated = service._mutate(offspring)
        self.assertGreaterEqual(mutated.module_count, 1)

    def test_update_top_results_keeps_best_fitness(self) -> None:
        service = GeneticAlgorithmService(
            self.requirements,
            self.site,
            population_size=2,
            generations=1,
        )
        top: list = []
        installation = make_installation()

        service._update_top_results(top, installation, 0.0)
        self.assertEqual(top, [])

        service._update_top_results(top, installation, 0.5)
        self.assertEqual(len(top), 1)
        self.assertEqual(top[0][1], 0.5)

        service._update_top_results(top, installation, 0.8)
        self.assertEqual(top[0][1], 0.8)


class PvInstallationDesignerTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        PvModule.objects.create(
            name="Designer Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
            height_cm=170,
            width_cm=100,
            voc=40,
            vmp=33,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        Inverter.objects.create(
            name="Designer Inverter",
            price_pln=3000,
            max_dc_voltage=600,
            mppt_min=100,
            mppt_max=500,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=15,
        )

    def setUp(self) -> None:
        GADataCache().clear_cache()

    def test_design_returns_matching_and_alternative_lists(self) -> None:
        result = PvInstallationDesigner().design(
            make_requirements(),
            make_installation_site(),
            generations=2,
            population_size=4,
        )

        self.assertIsNotNone(result.matching_installations)
        self.assertIsNotNone(result.alternative_installations)


class ClearGADataCacheTaskTests(TestCase):
    def test_task_clears_cache(self) -> None:
        cache = GADataCache()
        cache.write_to_cache(GAData(modules=[], inverters=[]))

        ClearGADataCache().run()

        self.assertIsNone(cache.get_cache())
