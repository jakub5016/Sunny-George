from django.urls import path

from catalog.views import InverterListView, PvModuleListView

urlpatterns = [
    path("modules/", PvModuleListView.as_view(), name="catalog-modules"),
    path("inverters/", InverterListView.as_view(), name="catalog-inverters"),
]
