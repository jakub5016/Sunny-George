from config.const import MAX_BUDGET_OVERSHOOT_RATIO
from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.services.installation_metrics_service import InstallationMetricsService


class RequirementsMatchService:
    """
    Calculates how closely an installation matches client requirements (0–100%).
    Separate from GA fitness — intended for user-facing display.
    """

    def __init__(self) -> None:
        self.metrics_service = InstallationMetricsService()

    def calculate_percent(
        self,
        installation: InstallationDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> int:
        metrics = self.metrics_service.calculate(installation, installation_site)

        area_score = self._area_score(
            metrics.installation_area_m2,
            requirements.installation_area_m2,
        )
        power_score = self._power_score(
            metrics.installation_power_kw,
            requirements.installation_power_kw,
        )
        cost_score = self._cost_score(
            metrics.total_cost_pln,
            requirements.max_pln_budget,
        )

        average = (area_score + power_score + cost_score) / 3
        return round(min(100, max(0, average * 100)))

    def _area_score(self, actual: float, required: float) -> float:
        if required <= 0:
            return 1.0 if actual <= 0 else 0.0

        if actual > required:
            return max(0.0, 1.0 - (actual - required) / required)

        return max(0.0, 1.0 - abs(actual - required) / required)

    def _power_score(self, actual: float, required: float) -> float:
        if required <= 0:
            return 1.0

        if actual >= required:
            return 1.0

        return max(0.0, actual / required)

    def _cost_score(
        self,
        actual: float,
        max_budget: float,
        max_overshoot_ratio: float = MAX_BUDGET_OVERSHOOT_RATIO,
    ) -> float:
        if max_budget <= 0:
            return 1.0 if actual <= 0 else 0.0

        max_acceptable = max_budget * (1 + max_overshoot_ratio)

        if actual <= max_budget:
            return 1.0

        if actual > max_acceptable:
            return 0.0

        overshoot_range = max_acceptable - max_budget
        if overshoot_range <= 0:
            return 0.0

        return max(0.0, 1.0 - (actual - max_budget) / overshoot_range)
