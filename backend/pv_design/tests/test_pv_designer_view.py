from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pv_elements.models import Inverter, PvModule
from pv_elements.models.types.phase_type import PhaseType
from pv_design.services.genetic_algorithm.ga_data_cache import GADataCache


class PvDesignerViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        PvModule.objects.create(
            name="API Module",
            power_watt=400,
            efficiency_percent=20,
            price_pln=800,
            height_cm=170,
            width_cm=100,
            voc=40,
            vmp=33,
            Imp=12,
            temperature_coefficient_percent_per_c=-0.3,
        )
        Inverter.objects.create(
            name="API Inverter",
            price_pln=3000,
            max_dc_voltage=600,
            mppt_min=100,
            mppt_max=500,
            max_dc_power=5000,
            phases=PhaseType.SINGLE,
            max_mppt_current=15,
        )

    def setUp(self) -> None:
        GADataCache().clear_cache()

    def test_design_endpoint_returns_200(self) -> None:
        payload = {
            "client_requirements": {
                "installation_area_m2": 20,
                "installation_power_kw": 2,
                "max_pln_budget": 10000,
            },
            "installation_site": {
                "roof_angle": 30,
                "on_roof_installation": True,
                "installation_area_m2": 20,
                "distance_from_inverter_to_modules_m": 10,
                "shading_likert": 1,
            },
            "generations": 2,
            "population_size": 4,
        }

        response = self.client.post(reverse("pv-design"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("matching_installations", response.data)
        self.assertIn("alternative_installations", response.data)

    def test_design_endpoint_invalid_payload_returns_400(self) -> None:
        response = self.client.post(reverse("pv-design"), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
