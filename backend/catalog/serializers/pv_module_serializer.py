from rest_framework import serializers

from pv_elements.models import PvModule


class PvModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PvModule
        fields = [
            "id",
            "name",
            "power_watt",
            "efficiency_percent",
            "price_pln",
            "height_cm",
            "width_cm",
            "voc",
            "vmp",
            "Imp",
            "temperature_coefficient_percent_per_c",
        ]
