# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns(
    'core.views',
    url(r'^$', 'api_root', name='api-root'),
)
