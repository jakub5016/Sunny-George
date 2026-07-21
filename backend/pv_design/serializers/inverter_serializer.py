from rest_framework import serializers


class InverterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price_pln = serializers.FloatField()
    max_dc_voltage = serializers.FloatField()
    mppt_min = serializers.FloatField()
    mppt_max = serializers.FloatField()
    max_dc_power = serializers.FloatField()
    phases = serializers.CharField()
    max_mppt_current = serializers.FloatField()
