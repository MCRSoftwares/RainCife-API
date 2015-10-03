# -*- coding: utf-8 -*-

from django.contrib import admin
from apac.models import APACMarker


@admin.register(APACMarker)
class APACMarkerAdmin(admin.ModelAdmin):
    pass
