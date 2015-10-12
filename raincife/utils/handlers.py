# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from raincife.logs import errors
from tornado import gen
from raincife.apps.auth import querysets


class JSONHandler(RequestHandler):
    schemas = None

    @gen.coroutine
    def validate(self, data):
        for schema in self.schemas:
            if not schema.validate(data):
                def_name = yield self._search_def(data, 'invalid')
                raise gen.Return(def_name)

        def_name = yield self._search_def(data, 'valid')
        raise gen.Return(def_name)

    @gen.coroutine
    def authenticate(self, data):
        if data['type'] != 'token':
            raise gen.Return(errors.AUTH['invalid_token'])
        json_data = {
            'id': data['id'],
            'user': data['user']
        }
        db_response = yield gen.Task(querysets.token.filter, json_data)

        if not db_response['data']:
            db_response = errors.AUTH['invalid_token']

        raise gen.Return(db_response)

    def _search_def(self, data, validation):
        def_name = 'json_{0}'.format(validation)
        if hasattr(self, def_name):
            return getattr(self, def_name)(data)
        else:
            raise NotImplementedError(errors.JSON['not_implemented'])

    class Meta:
        abstract = True
