# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='api')),
    url(r'^apac/', include('apac.urls', namespace='apac')),
]
