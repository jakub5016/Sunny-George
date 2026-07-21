from rest_framework.generics import ListAPIView

from catalog.dto import InverterFiltersDTO
from catalog.serializers import InverterSerializer
from catalog.services import InverterQueryBuilder


class InverterListView(ListAPIView):
    serializer_class = InverterSerializer

    def get_queryset(self):
        filters = InverterFiltersDTO.from_request(self.request)
        return InverterQueryBuilder(filters).build()
