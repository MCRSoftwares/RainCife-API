# -*- coding: utf-8 -*-

from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from view_manager.decorators import include_view
from apac.models import APACMarker
from apac.serializers import APACMarkerSerializer


@include_view('apacmarkers_list')
class APACMarkersListView(ListAPIView):
    queryset = APACMarker.objects.all()
    serializer_class = APACMarkerSerializer


@include_view('apacmarker_retrieve')
class APACMarkerRetrieveView(RetrieveAPIView):
    queryset = APACMarker.objects.all()
    serializer_class = APACMarkerSerializer