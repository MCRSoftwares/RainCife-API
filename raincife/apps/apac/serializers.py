# -*- coding: utf-8 -*-


from rest_framework import serializers
from .models import APACMarker


class APACMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = APACMarker
        fields = ('id', 'apac_id', 'name', 'local',
                  'latitude', 'longitude', )
