from pv_design.dto.pv_module_dto import PvModuleDto
from pv_elements.models.pv_module import PvModule
from pv_design.dto.inverter_dto import InverterDto
from pv_elements.models.inverter import Inverter
from pv_design.dto.ga_data import GAData
from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache


class GADataProvider:
    
    def __init__(self) -> None:
        self._cache = GADataCache()

    def get_modules(self) -> list[PvModuleDto]:
        return [PvModuleDto(
            id=module.id,
            name=module.name,
            power_watt=module.power_watt,
            efficiency_percent=module.efficiency_percent,
            price_pln=module.price_pln,
            height_cm=module.height_cm,
            width_cm=module.width_cm,
            voc=module.voc,
            vmp=module.vmp,
            Imp=module.Imp,
            temperature_coefficient_percent_per_c=module.temperature_coefficient_percent_per_c,
        ) for module in PvModule.objects.all()]

    def get_inverters(self) -> list[InverterDto]:
        return [InverterDto(
            id=inverter.id,
            name=inverter.name,
            price_pln=inverter.price_pln,
            max_dc_voltage=inverter.max_dc_voltage,
            mppt_min=inverter.mppt_min,
            mppt_max=inverter.mppt_max,
            max_dc_power=inverter.max_dc_power,
            phases=inverter.phases,
            max_mppt_current=inverter.max_mppt_current,
        ) for inverter in Inverter.objects.all()]

    def load_data(self):
        cached_values = self._cache.get_cache()

        if cached_values:
            return cached_values

        self.modules = self.get_modules()
        self.inverters = self.get_inverters()

        new_data = GAData(
            modules=self.modules,
            inverters=self.inverters,
        )

        self._cache.write_to_cache(new_data)

        return new_data