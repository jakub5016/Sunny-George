from rest_framework import serializers

from pv_elements.models import Inverter


class InverterSerializer(serializers.ModelSerializer):
    phases_display = serializers.CharField(source="get_phases_display", read_only=True)

    class Meta:
        model = Inverter
        fields = [
            "id",
            "name",
            "price_pln",
            "max_dc_voltage",
            "mppt_min",
            "mppt_max",
            "max_dc_power",
            "phases",
            "phases_display",
            "max_mppt_current",
        ]
