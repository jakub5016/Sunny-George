from rest_framework.generics import ListAPIView

from catalog.dto import ModuleFiltersDTO
from catalog.serializers import PvModuleSerializer
from catalog.services import PvModuleQueryBuilder


class PvModuleListView(ListAPIView):
    serializer_class = PvModuleSerializer

    def get_queryset(self):
        filters = ModuleFiltersDTO.from_request(self.request)
        return PvModuleQueryBuilder(filters).build()
