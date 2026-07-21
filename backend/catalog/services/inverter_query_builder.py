from django.db.models import QuerySet

from pv_elements.models import Inverter

from catalog.dto import InverterFiltersDTO


class InverterQueryBuilder:
    def __init__(self, filters: InverterFiltersDTO) -> None:
        self._filters = filters
        self._query_set: QuerySet = Inverter.objects.all().order_by("name")

    def build(self) -> QuerySet:
        filters = self._filters
        if filters.search:
            self._query_set = self._query_set.filter(name__icontains=filters.search)
        if filters.phases:
            self._query_set = self._query_set.filter(phases=filters.phases)
        if filters.power_min is not None:
            self._query_set = self._query_set.filter(max_dc_power__gte=filters.power_min)
        if filters.power_max is not None:
            self._query_set = self._query_set.filter(max_dc_power__lte=filters.power_max)
        if filters.price_min is not None:
            self._query_set = self._query_set.filter(price_pln__gte=filters.price_min)
        if filters.price_max is not None:
            self._query_set = self._query_set.filter(price_pln__lte=filters.price_max)
        return self._query_set
