from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pv_elements.models import Inverter, PvModule
from pv_elements.models.types.phase_type import PhaseType


class CatalogViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Inverter.objects.create(
            name="Test Inverter",
            price_pln=3000,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=12,
        )
        PvModule.objects.create(
            name="Test Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
        )

    def test_inverter_list_returns_200(self) -> None:
        response = self.client.get(reverse("catalog-inverters"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Inverter")
        self.assertIn("phases_display", response.data[0])

    def test_inverter_list_with_filters(self) -> None:
        response = self.client.get(reverse("catalog-inverters"), {"search": "Missing"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_module_list_returns_200(self) -> None:
        response = self.client.get(reverse("catalog-modules"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["power_watt"], 400)
