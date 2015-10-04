# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from decouple import config


urlpatterns = [
    url(r'^{0}/'.format(config('ADMIN_URL', default='admin')),
        include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^apac/', include('apac.urls', namespace='apac')),
    url(r'^', include('core.urls', namespace='core')),
]
