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

    def validate_id_apac(self, field, value):
        if int(value) < 1000:
            return False
        return True


Sensor = SensorSchema()
