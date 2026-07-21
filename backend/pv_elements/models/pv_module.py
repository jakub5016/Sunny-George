from django.db.models import CharField, FloatField, Model


class PvModule(Model):
    name = CharField(max_length=255)
    power_watt = FloatField(default=0) # W
    efficiency_percent = FloatField(default=0) # %
    price_pln = FloatField(default=0) # PLN
    height_cm = FloatField(default=0) # cm
    width_cm = FloatField(default=0) # cm
    voc = FloatField(default=0) # V
    vmp = FloatField(default=0) # V
    Imp = FloatField(default=0) # A
    temperature_coefficient_percent_per_c = FloatField(default=0) # %/°C
    