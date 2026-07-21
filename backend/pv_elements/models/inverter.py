from django.db.models import Model, CharField, FloatField

from pv_elements.models.types.phase_type import PhaseType


class Inverter(Model):
    name = CharField(max_length=255)
    price_pln = FloatField(default=0)
    max_dc_voltage = FloatField(default=0)  # V
    mppt_min = FloatField(default=0)  # V
    mppt_max = FloatField(default=0)  # V
    max_dc_power = FloatField(default=0)  # W
    phases = CharField(max_length=255, choices=PhaseType.choices)
    max_mppt_current = FloatField(default=0)  # A
    