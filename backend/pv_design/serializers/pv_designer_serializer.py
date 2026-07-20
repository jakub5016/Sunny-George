from rest_framework import serializers

from pv_design.serializers.client_requirements_serializer import ClientRequirementsSerializer
from pv_design.serializers.installation_site_serializer import InstallationSiteSerializer


class PvDesignerSerializer(serializers.Serializer):
    client_requirements = ClientRequirementsSerializer()
    installation_site = InstallationSiteSerializer()
    generations = serializers.IntegerField(required=False, allow_null=True, min_value=1)
    population_size = serializers.IntegerField(required=False, allow_null=True, min_value=1)
