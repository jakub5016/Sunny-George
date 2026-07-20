from rest_framework import serializers

from pv_design.serializers.inverter_serializer import InverterSerializer
from pv_design.serializers.installation_metrics_serializer import InstallationMetricsSerializer
from pv_design.serializers.pv_module_serializer import PvModuleSerializer


class InstallationResultSerializer(serializers.Serializer):
    inverter = InverterSerializer()
    module_type = PvModuleSerializer()
    module_count = serializers.IntegerField()
    match_percent = serializers.IntegerField(min_value=0, max_value=100)
    metrics = InstallationMetricsSerializer()


class PvInstallationResponseSerializer(serializers.Serializer):
    matching_installations = InstallationResultSerializer(many=True)
    alternative_installations = InstallationResultSerializer(many=True)
