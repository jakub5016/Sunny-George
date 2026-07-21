from rest_framework import serializers


class InstallationSiteSerializer(serializers.Serializer):
    roof_angle = serializers.FloatField(required=False, allow_null=True)
    on_roof_installation = serializers.BooleanField()
    installation_area_m2 = serializers.FloatField(min_value=0)
    distance_from_inverter_to_modules_m = serializers.FloatField(min_value=0)
    shading_likert = serializers.IntegerField(min_value=1, max_value=5)
