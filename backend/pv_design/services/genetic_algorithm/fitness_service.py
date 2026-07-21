from config.const import MAX_BUDGET_OVERSHOOT_RATIO
from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.services.installation_checker import InstallationChecker
from pv_design.services.installation_metrics_service import InstallationMetricsService


class FitnessService:
    """
    Calculates fitness for installation - GA algorithm
    """
    def __init__(self) -> None:
        self.checker = InstallationChecker()
        self.metrics_service = InstallationMetricsService()

    def calculate(
        self,
        installation: InstallationDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,

    ) -> float:
        if not self.checker.check(installation):
            return 0.0

        metrics = self.metrics_service.calculate(installation, installation_site)

        if metrics.installation_power_kw < requirements.installation_power_kw:
            return 0.0

        if metrics.installation_area_m2 > requirements.installation_area_m2:
            return 0.0

        budget_penalty = self.calculate_budget_cost_penalty(
            metrics.total_cost_pln,
            requirements.max_pln_budget,
        )
        if budget_penalty is None:
            return 0.0

        cost_savings_bonus = self.calculate_cost_savings_bonus(
            metrics.total_cost_pln,
            requirements.max_pln_budget,
        )

        diff = (
            abs(metrics.installation_area_m2 - requirements.installation_area_m2)
            + budget_penalty
            - cost_savings_bonus
        )

        return 1.0 / (1.0 + max(diff, 0.0))

    def calculate_budget_cost_penalty(
        self,
        total_cost_pln: float,
        max_pln_budget: float,
        max_overshoot_ratio: float = MAX_BUDGET_OVERSHOOT_RATIO,
    ) -> float | None:
        """
        Budget cost penalty for fitness calculation.

        Returns None when cost exceeds the acceptable budget (hard reject).
        Returns 0 when cost is at or below the target budget (lower is better).
        Returns a steep penalty when cost is between budget and max acceptable.
        """
        max_acceptable_budget = max_pln_budget * (1 + max_overshoot_ratio)

        if total_cost_pln > max_acceptable_budget:
            return None

        if total_cost_pln <= max_pln_budget:
            return 0.0

        max_overshoot = max_pln_budget * max_overshoot_ratio
        overshoot_normalized = (total_cost_pln - max_pln_budget) / max_overshoot

        return max_pln_budget * overshoot_normalized**4

    def calculate_cost_savings_bonus(
        self,
        total_cost_pln: float,
        max_pln_budget: float,
        max_bonus: float = 1.0,
    ) -> float:
        """
        Moderate bonus for solutions below budget.

        Uses the same scale as area deviation (m²) so cheaper options are preferred
        without outweighing client requirements.
        """
        if max_pln_budget <= 0 or total_cost_pln >= max_pln_budget:
            return 0.0

        savings_ratio = (max_pln_budget - total_cost_pln) / max_pln_budget
        return savings_ratio * max_bonus
