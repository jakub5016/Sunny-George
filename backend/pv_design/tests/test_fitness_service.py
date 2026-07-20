from django.test import SimpleTestCase

from pv_design.dto.ga_data import GAData
from pv_design.services.genetic_algorithm.fitness_service import FitnessService
from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache

from .fixtures import make_inverter, make_installation, make_installation_site, make_module, make_requirements


class FitnessServiceTests(SimpleTestCase):
    def setUp(self) -> None:
        self.service = FitnessService()
        self.installation = make_installation()
        self.requirements = make_requirements()
        self.site = make_installation_site()

    def test_calculate_returns_positive_for_valid_installation(self) -> None:
        fitness = self.service.calculate(self.installation, self.requirements, self.site)
        self.assertGreater(fitness, 0)

    def test_calculate_returns_zero_for_invalid_installation(self) -> None:
        installation = make_installation(module_type=make_module(Imp=99))
        self.assertEqual(
            self.service.calculate(installation, self.requirements, self.site),
            0.0,
        )

    def test_calculate_returns_zero_when_underpowered(self) -> None:
        requirements = make_requirements(installation_power_kw=100.0)
        self.assertEqual(
            self.service.calculate(self.installation, requirements, self.site),
            0.0,
        )

    def test_calculate_returns_zero_when_area_exceeded(self) -> None:
        requirements = make_requirements(installation_area_m2=1.0)
        self.assertEqual(
            self.service.calculate(self.installation, requirements, self.site),
            0.0,
        )

    def test_budget_penalty_under_budget(self) -> None:
        self.assertEqual(self.service.calculate_budget_cost_penalty(8000, 10_000), 0.0)

    def test_budget_penalty_between_budget_and_max(self) -> None:
        penalty = self.service.calculate_budget_cost_penalty(10_200, 10_000, 0.05)
        self.assertGreater(penalty, 0)

    def test_budget_penalty_beyond_max_returns_none(self) -> None:
        self.assertIsNone(self.service.calculate_budget_cost_penalty(20_000, 10_000))

    def test_cost_savings_bonus_below_budget(self) -> None:
        bonus = self.service.calculate_cost_savings_bonus(8000, 10_000)
        self.assertAlmostEqual(bonus, 0.2)

    def test_cost_savings_bonus_at_or_above_budget(self) -> None:
        self.assertEqual(self.service.calculate_cost_savings_bonus(10_000, 10_000), 0.0)
        self.assertEqual(self.service.calculate_cost_savings_bonus(0, 0), 0.0)


class GADataCacheTests(SimpleTestCase):
    def setUp(self) -> None:
        self.cache = GADataCache()
        self.cache.clear_cache()

    def test_write_and_get_cache(self) -> None:
        data = GAData(
            modules=[make_module()],
            inverters=[make_inverter()],
        )
        self.cache.write_to_cache(data)
        self.assertEqual(self.cache.get_cache(), data)

    def test_clear_cache(self) -> None:
        self.cache.write_to_cache(GAData(modules=[], inverters=[]))
        self.cache.clear_cache()
        self.assertIsNone(self.cache.get_cache())

    def test_write_invalid_type_raises(self) -> None:
        with self.assertRaises(TypeError):
            self.cache.write_to_cache("invalid")  # type: ignore[arg-type]
