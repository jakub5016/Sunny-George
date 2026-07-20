from django.test import SimpleTestCase

from config.const import OPTIMAL_TILT_DEG, Y_REF_KWH_PER_KWP
from pv_design.services.installation_metrics_service import InstallationMetricsService
from pv_design.services.installation_power_service import InstallationPowerService
from pv_design.services.requirements_match_service import RequirementsMatchService

from .fixtures import make_installation, make_installation_site, make_requirements


class InstallationPowerServiceTests(SimpleTestCase):
    def setUp(self) -> None:
        self.service = InstallationPowerService()
        self.installation = make_installation()
        self.site = make_installation_site()

    def test_nominal_power_kw(self) -> None:
        self.assertEqual(self.service.nominal_power_kw(self.installation), 2.0)

    def test_tilt_factor_at_optimal(self) -> None:
        self.assertAlmostEqual(self.service.tilt_factor(OPTIMAL_TILT_DEG), 1.0)

    def test_tilt_factor_decreases_off_optimal(self) -> None:
        self.assertLess(self.service.tilt_factor(0), 1.0)

    def test_shading_factor_for_valid_likert(self) -> None:
        self.assertEqual(self.service.shading_factor(1), 1.0)
        self.assertEqual(self.service.shading_factor(5), 0.5)

    def test_shading_factor_invalid_likert_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.service.shading_factor(9)

    def test_effective_power_uses_default_tilt_when_roof_angle_none(self) -> None:
        site = make_installation_site(roof_angle=None)
        power = self.service.effective_power_kw(self.installation, site)
        self.assertGreater(power, 0)

    def test_estimate_annual_energy_kwh(self) -> None:
        energy = self.service.estimate_annual_energy_kwh(self.installation, self.site)
        expected = self.service.effective_power_kw(self.installation, self.site) * Y_REF_KWH_PER_KWP
        self.assertAlmostEqual(energy, expected)


class InstallationMetricsServiceTests(SimpleTestCase):
    def setUp(self) -> None:
        self.service = InstallationMetricsService()
        self.installation = make_installation()
        self.site = make_installation_site()

    def test_calculate_roof_installation(self) -> None:
        metrics = self.service.calculate(self.installation, self.site)

        self.assertAlmostEqual(metrics.installation_area_m2, 8.5)
        self.assertGreater(metrics.installation_power_kw, 0)
        self.assertGreater(metrics.total_cost_pln, 0)

    def test_calculate_ground_installation_uses_higher_costs(self) -> None:
        roof_site = make_installation_site(on_roof_installation=True)
        ground_site = make_installation_site(on_roof_installation=False)

        roof_cost = self.service.calculate(self.installation, roof_site).total_cost_pln
        ground_cost = self.service.calculate(self.installation, ground_site).total_cost_pln

        self.assertGreater(ground_cost, roof_cost)


class RequirementsMatchServiceExtendedTests(SimpleTestCase):
    def setUp(self) -> None:
        self.service = RequirementsMatchService()

    def test_area_score_exact_match(self) -> None:
        self.assertEqual(self.service._area_score(20.0, 20.0), 1.0)

    def test_area_score_over_required(self) -> None:
        self.assertLess(self.service._area_score(25.0, 20.0), 1.0)

    def test_area_score_zero_required(self) -> None:
        self.assertEqual(self.service._area_score(0.0, 0.0), 1.0)
        self.assertEqual(self.service._area_score(5.0, 0.0), 0.0)

    def test_power_score_meets_requirement(self) -> None:
        self.assertEqual(self.service._power_score(3.0, 2.0), 1.0)

    def test_power_score_underpowered(self) -> None:
        self.assertEqual(self.service._power_score(1.0, 2.0), 0.5)

    def test_power_score_zero_required(self) -> None:
        self.assertEqual(self.service._power_score(0.0, 0.0), 1.0)

    def test_cost_score_under_budget(self) -> None:
        self.assertEqual(self.service._cost_score(8000.0, 10_000.0), 1.0)

    def test_cost_score_slightly_over_budget(self) -> None:
        self.assertLess(self.service._cost_score(10_200.0, 10_000.0), 1.0)

    def test_cost_score_beyond_max_overshoot(self) -> None:
        self.assertEqual(self.service._cost_score(20_000.0, 10_000.0), 0.0)

    def test_cost_score_zero_budget(self) -> None:
        self.assertEqual(self.service._cost_score(0.0, 0.0), 1.0)
        self.assertEqual(self.service._cost_score(100.0, 0.0), 0.0)
