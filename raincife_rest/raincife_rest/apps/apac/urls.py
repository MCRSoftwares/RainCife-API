# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns(
    'apac.views',
    url(r'^markers/$', 'apacmarkers_list', name='markers-list'),
    url(r'^markers/(?P<pk>[0-9]+)/$',
        'apacmarker_retrieve', name='marker-detail'),
)
