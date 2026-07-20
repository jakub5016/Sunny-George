from django.test import TestCase

from pv_elements.models import Inverter, PvModule
from pv_elements.models.types.phase_type import PhaseType


class PvElementsModelTests(TestCase):
    def test_create_inverter_and_module(self) -> None:
        inverter = Inverter.objects.create(
            name="Model Inverter",
            price_pln=3000,
            phases=PhaseType.SINGLE,
        )
        module = PvModule.objects.create(
            name="Model Module",
            power_watt=400,
            price_pln=800,
        )

        self.assertEqual(str(inverter.name), "Model Inverter")
        self.assertEqual(module.power_watt, 400)
