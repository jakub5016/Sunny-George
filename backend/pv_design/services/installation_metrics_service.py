from config.const import (
    BASIC_SERVICE_COST_PLN,
    CABLE_COST_PLN_PER_M,
    GROUND_LABOR_COST_PLN_PER_PANEL,
    GROUND_MOUNTING_COST_PLN_PER_PANEL,
    ROOF_LABOR_COST_PLN_PER_PANEL,
    ROOF_MOUNTING_COST_PLN_PER_PANEL,
)
from pv_design.services.installation_power_service import InstallationPowerService
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_metrics import InstallationMetrics
from pv_design.dto.installation_site_dto import InstallationSiteDto


class InstallationMetricsService:
    def __init__(self) -> None:
        self.power_service = InstallationPowerService()

    def calculate(
        self,
        installation: InstallationDto,
        installation_site: InstallationSiteDto,
    ) -> InstallationMetrics:
        module = installation.module_type
        module_area_m2 = (module.height_cm * module.width_cm) / 10_000
        installation_area_m2 = module_area_m2 * installation.module_count
        installation_power_kw = self.power_service.effective_power_kw(
            installation, installation_site
        )
        modules_cost_pln = module.price_pln * installation.module_count
        cable_cost_pln = (
            CABLE_COST_PLN_PER_M * installation_site.distance_from_inverter_to_modules_m
        )

        if installation_site.on_roof_installation:
            labor_cost_pln = ROOF_LABOR_COST_PLN_PER_PANEL * installation.module_count
            mounting_cost_pln = ROOF_MOUNTING_COST_PLN_PER_PANEL * installation.module_count
        else:
            labor_cost_pln = GROUND_LABOR_COST_PLN_PER_PANEL * installation.module_count
            mounting_cost_pln = GROUND_MOUNTING_COST_PLN_PER_PANEL * installation.module_count

        total_cost_pln = (
            modules_cost_pln
            + installation.inverter.price_pln
            + BASIC_SERVICE_COST_PLN
            + cable_cost_pln
            + labor_cost_pln
            + mounting_cost_pln
        )

        return InstallationMetrics(
            installation_area_m2=installation_area_m2,
            installation_power_kw=installation_power_kw,
            total_cost_pln=total_cost_pln,
        )
