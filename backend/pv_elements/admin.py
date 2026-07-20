from django.contrib import admin

from pv_elements.models import Inverter, PvModule

admin.site.register(PvModule)
admin.site.register(Inverter)
