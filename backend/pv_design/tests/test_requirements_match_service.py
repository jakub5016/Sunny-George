from django.test import SimpleTestCase

from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_metrics import InstallationMetrics
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.inverter_dto import InverterDto
from pv_design.dto.pv_module_dto import PvModuleDto
from pv_design.services.requirements_match_service import RequirementsMatchService


class RequirementsMatchServiceTests(SimpleTestCase):
    def setUp(self) -> None:
        self.service = RequirementsMatchService()
        self.requirements = ClientRequirementsDto(
            installation_area_m2=20.0,
            installation_power_kw=2.0,
            max_pln_budget=10_000.0,
        )
        self.installation_site = InstallationSiteDto(
            roof_angle=30.0,
            on_roof_installation=True,
            installation_area_m2=20.0,
            distance_from_inverter_to_modules_m=10.0,
            shading_likert=1,
        )
        self.installation = InstallationDto(
            inverter=InverterDto(
                id=1,
                name="Test inverter",
                price_pln=3_000,
                max_dc_voltage=600,
                mppt_min=200,
                mppt_max=500,
                max_dc_power=5_000,
                phases="1",
                max_mppt_current=12,
            ),
            module_type=PvModuleDto(
                id=1,
                name="Test module",
                power_watt=400,
                efficiency_percent=20,
                price_pln=800,
                height_cm=170,
                width_cm=100,
                voc=40,
                vmp=33,
                Imp=12,
                temperature_coefficient_percent_per_c=-0.3,
            ),
            module_count=5,
        )

    def test_near_perfect_match_scores_high(self) -> None:
        self.service.metrics_service.calculate = lambda *_args: InstallationMetrics(
            installation_area_m2=19.4,
            installation_power_kw=2.0,
            total_cost_pln=9_945.0,
        )

        match_percent = self.service.calculate_percent(
            self.installation,
            self.requirements,
            self.installation_site,
        )

        self.assertGreaterEqual(match_percent, 95)

    def test_underpowered_installation_lowers_score(self) -> None:
        self.service.metrics_service.calculate = lambda *_args: InstallationMetrics(
            installation_area_m2=19.0,
            installation_power_kw=1.0,
            total_cost_pln=8_000.0,
        )

        match_percent = self.service.calculate_percent(
            self.installation,
            self.requirements,
            self.installation_site,
        )

        self.assertLess(match_percent, 90)
