from rest_framework import serializers


class InstallationMetricsSerializer(serializers.Serializer):
    installation_area_m2 = serializers.FloatField()
    installation_power_kw = serializers.FloatField()
    total_cost_pln = serializers.FloatField()
