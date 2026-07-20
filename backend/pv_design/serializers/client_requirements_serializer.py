from rest_framework import serializers


class ClientRequirementsSerializer(serializers.Serializer):
    installation_area_m2 = serializers.FloatField(min_value=0)
    installation_power_kw = serializers.FloatField(min_value=0)
    max_pln_budget = serializers.FloatField(min_value=0)
