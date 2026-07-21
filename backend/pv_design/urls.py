from django.urls import path

from pv_design.views.pv_designer import PvDesignerView

urlpatterns = [
    path("design/", PvDesignerView.as_view(), name="pv-design"),
]
