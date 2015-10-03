# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls import patterns


urlpatterns = patterns(
    'apac.views',
    url(r'^markers/$', 'apacmarkers_list_view', name='markers-list'),
    url(r'^markers/(?P<pk>[0-9]+)/$',
        'apacmarker_retrieve_view', name='marker-detail'),
)
