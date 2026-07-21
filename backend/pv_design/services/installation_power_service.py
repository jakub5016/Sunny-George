import math

from config.const import (
    LIKERT_SHADING_FACTORS,
    OPTIMAL_TILT_DEG,
    TILT_FACTOR_SIGMA,
    Y_REF_KWH_PER_KWP,
)
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto


class InstallationPowerService:
    def nominal_power_kw(self, installation: InstallationDto) -> float:
        return (installation.module_type.power_watt * installation.module_count) / 1000

    def tilt_factor(self, beta_deg: float) -> float:
        return math.exp(-((beta_deg - OPTIMAL_TILT_DEG) ** 2) / (2 * TILT_FACTOR_SIGMA ** 2))

    def shading_factor(self, likert: int) -> float:
        if likert not in LIKERT_SHADING_FACTORS:
            raise ValueError("Likert shading must be 1–5")
        return LIKERT_SHADING_FACTORS[likert]

    def _resolve_tilt_deg(self, installation_site: InstallationSiteDto) -> float:
        if installation_site.roof_angle is not None:
            return installation_site.roof_angle
        return OPTIMAL_TILT_DEG

    def effective_power_kw(
        self,
        installation: InstallationDto,
        installation_site: InstallationSiteDto,
    ) -> float:
        nominal_power_kw = self.nominal_power_kw(installation)
        tilt_deg = self._resolve_tilt_deg(installation_site)

        return (
            nominal_power_kw
            * self.tilt_factor(tilt_deg)
            * self.shading_factor(installation_site.shading_likert)
        )

    def estimate_annual_energy_kwh(
        self,
        installation: InstallationDto,
        installation_site: InstallationSiteDto,
    ) -> float:
        return self.effective_power_kw(installation, installation_site) * Y_REF_KWH_PER_KWP
