# -*- coding: utf-8 -*-

from raincife.logs import errors


class Schema(object):
    base_field = None
    fields = None

    def __init__(self, *args, **kwargs):
        if not self.fields:
            raise ValueError(errors.SCHEMA['none_fields'])

    def validate(self, data):
        if self.base_field not in data:
            return False
        field_list = data[self.base_field]
        if isinstance(field_list, list):
            for instance in field_list:
                return self._validate_fields(instance)
        else:
            return self._validate_fields(field_list)
        return True

    def _validate_fields(self, instance):
        for field, value in self.fields.items():
            if field not in instance and value['required']:
                return False
        for field, value in instance.items():
            try:
                validate = 'validate_{0}'.format(field)
                if hasattr(self, validate):
                    return getattr(self, validate)(field, value)
                elif not isinstance(value, self.fields[field]['type']):
                    return False
            except KeyError:
                return False
        return True
