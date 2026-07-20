from django.test import TestCase

from catalog.dto.inverter_filters import InverterFiltersDTO
from catalog.dto.module_filters import ModuleFiltersDTO
from catalog.services.inverter_query_builder import InverterQueryBuilder
from catalog.services.pv_module_query_builder import PvModuleQueryBuilder
from pv_elements.models import Inverter, PvModule
from pv_elements.models.types.phase_type import PhaseType


class InverterQueryBuilderTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.inv_a = Inverter.objects.create(
            name="Alpha Inverter",
            price_pln=2000,
            max_dc_power=4000,
            phases=PhaseType.SINGLE,
        )
        cls.inv_b = Inverter.objects.create(
            name="Beta Inverter",
            price_pln=4000,
            max_dc_power=8000,
            phases=PhaseType.THREE,
        )

    def test_no_filters_returns_all_ordered(self) -> None:
        qs = InverterQueryBuilder(
            InverterFiltersDTO(None, None, None, None, None, None)
        ).build()
        self.assertEqual(list(qs), [self.inv_a, self.inv_b])

    def test_search_filter(self) -> None:
        filters = InverterFiltersDTO(
            search="Alpha", phases=None, power_min=None, power_max=None,
            price_min=None, price_max=None,
        )
        qs = InverterQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.inv_a])

    def test_phases_filter(self) -> None:
        filters = InverterFiltersDTO(None, PhaseType.THREE, None, None, None, None)
        qs = InverterQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.inv_b])

    def test_power_and_price_filters(self) -> None:
        filters = InverterFiltersDTO(None, None, 5000, 9000, 3000, 5000)
        qs = InverterQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.inv_b])


class PvModuleQueryBuilderTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.mod_a = PvModule.objects.create(
            name="Alpha Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
        )
        cls.mod_b = PvModule.objects.create(
            name="Beta Module",
            power_watt=500,
            efficiency_percent=22,
            price_pln=1000,
        )

    def test_no_filters_returns_all_ordered(self) -> None:
        filters = ModuleFiltersDTO(None, None, None, None, None, None, None)
        qs = PvModuleQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.mod_a, self.mod_b])

    def test_search_filter(self) -> None:
        filters = ModuleFiltersDTO("Beta", None, None, None, None, None, None)
        qs = PvModuleQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.mod_b])

    def test_power_efficiency_price_filters(self) -> None:
        filters = ModuleFiltersDTO(None, 450, 550, 21, 23, 900, 1100)
        qs = PvModuleQueryBuilder(filters).build()
        self.assertEqual(list(qs), [self.mod_b])
