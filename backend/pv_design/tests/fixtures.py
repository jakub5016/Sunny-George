from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.inverter_dto import InverterDto
from pv_design.dto.pv_module_dto import PvModuleDto


def make_inverter(**overrides) -> InverterDto:
    defaults = {
        "id": 1,
        "name": "Test inverter",
        "price_pln": 3000,
        "max_dc_voltage": 600,
        "mppt_min": 100,
        "mppt_max": 500,
        "max_dc_power": 5000,
        "phases": "single",
        "max_mppt_current": 15,
    }
    defaults.update(overrides)
    return InverterDto(**defaults)


def make_module(**overrides) -> PvModuleDto:
    defaults = {
        "id": 1,
        "name": "Test module",
        "power_watt": 400,
        "efficiency_percent": 20,
        "price_pln": 800,
        "height_cm": 170,
        "width_cm": 100,
        "voc": 40,
        "vmp": 33,
        "Imp": 12,
        "temperature_coefficient_percent_per_c": -0.3,
    }
    defaults.update(overrides)
    return PvModuleDto(**defaults)


def make_installation(**overrides) -> InstallationDto:
    defaults = {
        "inverter": make_inverter(),
        "module_type": make_module(),
        "module_count": 5,
    }
    defaults.update(overrides)
    return InstallationDto(**defaults)


def make_requirements(**overrides) -> ClientRequirementsDto:
    defaults = {
        "installation_area_m2": 20.0,
        "installation_power_kw": 1.5,
        "max_pln_budget": 10_000.0,
    }
    defaults.update(overrides)
    return ClientRequirementsDto(**defaults)


def make_installation_site(**overrides) -> InstallationSiteDto:
    defaults = {
        "roof_angle": 30.0,
        "on_roof_installation": True,
        "installation_area_m2": 20.0,
        "distance_from_inverter_to_modules_m": 10.0,
        "shading_likert": 1,
    }
    defaults.update(overrides)
    return InstallationSiteDto(**defaults)
