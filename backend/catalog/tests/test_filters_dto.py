from django.test import SimpleTestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from catalog.dto.inverter_filters import InverterFiltersDTO
from catalog.dto.module_filters import ModuleFiltersDTO


class InverterFiltersDTOTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_from_request_empty_params(self) -> None:
        request = Request(self.factory.get("/api/catalog/inverters/"))
        dto = InverterFiltersDTO.from_request(request)

        self.assertIsNone(dto.search)
        self.assertIsNone(dto.phases)
        self.assertIsNone(dto.power_min)

    def test_from_request_with_all_params(self) -> None:
        request = Request(
            self.factory.get(
                "/api/catalog/inverters/",
                {
                    "search": "test",
                    "phases": "single",
                    "power_min": "1000",
                    "power_max": "5000",
                    "price_min": "100",
                    "price_max": "5000",
                },
            )
        )
        dto = InverterFiltersDTO.from_request(request)

        self.assertEqual(dto.search, "test")
        self.assertEqual(dto.phases, "single")
        self.assertEqual(dto.power_min, 1000.0)
        self.assertEqual(dto.power_max, 5000.0)
        self.assertEqual(dto.price_min, 100.0)
        self.assertEqual(dto.price_max, 5000.0)


class ModuleFiltersDTOTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_from_request_empty_params(self) -> None:
        request = Request(self.factory.get("/api/catalog/modules/"))
        dto = ModuleFiltersDTO.from_request(request)

        self.assertIsNone(dto.search)
        self.assertIsNone(dto.efficiency_min)

    def test_from_request_with_all_params(self) -> None:
        request = Request(
            self.factory.get(
                "/api/catalog/modules/",
                {
                    "search": "panel",
                    "power_min": "300",
                    "power_max": "500",
                    "efficiency_min": "18",
                    "efficiency_max": "22",
                    "price_min": "500",
                    "price_max": "1200",
                },
            )
        )
        dto = ModuleFiltersDTO.from_request(request)

        self.assertEqual(dto.search, "panel")
        self.assertEqual(dto.power_min, 300.0)
        self.assertEqual(dto.efficiency_max, 22.0)
