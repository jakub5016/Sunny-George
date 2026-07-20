from rest_framework import serializers


class PvModuleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    power_watt = serializers.FloatField()
    efficiency_percent = serializers.FloatField()
    price_pln = serializers.FloatField()
    height_cm = serializers.FloatField()
    width_cm = serializers.FloatField()
    voc = serializers.FloatField()
    vmp = serializers.FloatField()
    Imp = serializers.FloatField()
    temperature_coefficient_percent_per_c = serializers.FloatField()
