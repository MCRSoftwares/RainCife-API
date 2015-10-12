# -*- coding: utf-8 -*-

from raincife.utils.schemas import Schema


class SensorSchema(Schema):
    base_field = 'data'
    fields = {
        'id_apac': {'type': int, 'required': True},
        'nome': {'type': basestring, 'required': True},
        'local': {'type': basestring, 'required': True},
        'latitude': {'type': basestring, 'required': True},
        'longitude': {'type': basestring, 'required': True},
    }


Sensor = SensorSchema()
