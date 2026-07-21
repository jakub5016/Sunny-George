from django.db.models import QuerySet

from pv_elements.models import PvModule

from catalog.dto import ModuleFiltersDTO


class PvModuleQueryBuilder:
    def __init__(self, filters: ModuleFiltersDTO) -> None:
        self._filters = filters
        self._query_set: QuerySet = PvModule.objects.all().order_by("name")

    def build(self) -> QuerySet:
        filters = self._filters
        if filters.search:
            self._query_set = self._query_set.filter(name__icontains=filters.search)
        if filters.power_min is not None:
            self._query_set = self._query_set.filter(power_watt__gte=filters.power_min)
        if filters.power_max is not None:
            self._query_set = self._query_set.filter(power_watt__lte=filters.power_max)
        if filters.efficiency_min is not None:
            self._query_set = self._query_set.filter(efficiency_percent__gte=filters.efficiency_min)
        if filters.efficiency_max is not None:
            self._query_set = self._query_set.filter(efficiency_percent__lte=filters.efficiency_max)
        if filters.price_min is not None:
            self._query_set = self._query_set.filter(price_pln__gte=filters.price_min)
        if filters.price_max is not None:
            self._query_set = self._query_set.filter(price_pln__lte=filters.price_max)
        return self._query_set
