from dataclasses import asdict

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from pv_design.dto.client_requirements import ClientRequirementsDto
from pv_design.dto.installation_dto import InstallationDto
from pv_design.dto.installation_site_dto import InstallationSiteDto
from pv_design.dto.pv_design_result_dto import PvDesignResultDto
from pv_design.serializers.pv_designer_serializer import PvDesignerSerializer
from pv_design.serializers.pv_installation_serializer import PvInstallationResponseSerializer
from pv_design.services.installation_metrics_service import InstallationMetricsService
from pv_design.services.pv_installation_designer import PvInstallationDesigner
from pv_design.services.requirements_match_service import RequirementsMatchService


class PvDesignerView(APIView):
    def post(self, request):
        serializer = PvDesignerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        client_requirements = ClientRequirementsDto(**data["client_requirements"])
        installation_site = InstallationSiteDto(**data["installation_site"])

        result = PvInstallationDesigner().design(
            client_requirements,
            installation_site,
        )

        return Response(
            self._serialize_design_result(
                result,
                client_requirements,
                installation_site,
            ),
        )

    def _serialize_design_result(
        self,
        result: PvDesignResultDto,
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> dict:
        payload = {
            "matching_installations": self._serialize_installation_list(
                result.matching_installations,
                requirements,
                installation_site,
            ),
            "alternative_installations": self._serialize_installation_list(
                result.alternative_installations,
                requirements,
                installation_site,
            ),
        }

        serializer = PvInstallationResponseSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def _serialize_installation_list(
        self,
        installations: list[InstallationDto],
        requirements: ClientRequirementsDto,
        installation_site: InstallationSiteDto,
    ) -> list[dict]:
        match_service = RequirementsMatchService()
        metrics_service = InstallationMetricsService()
        results = []

        for installation in installations:
            metrics = metrics_service.calculate(installation, installation_site)
            match_percent = match_service.calculate_percent(
                installation,
                requirements,
                installation_site,
            )
            results.append(
                {
                    "inverter": asdict(installation.inverter),
                    "module_type": asdict(installation.module_type),
                    "module_count": installation.module_count,
                    "match_percent": match_percent,
                    "metrics": asdict(metrics),
                }
            )

        return results
