# -*- coding: utf-8 -*-

from raincife.utils.handlers import JSONHandler
from raincife.logs import errors
from tornado import gen
from ..schemas import Sensor
from raincife.apps.auth.schemas import Token
from .. import querysets
import json


class SensorCreateHandler(JSONHandler):
    schemas = (Token, Sensor)

    @gen.coroutine
    def json_valid(self, json_data):
        db_response = yield gen.Task(self.authenticate, json_data['auth'])

        if 'error' not in db_response:
            for data in json_data['data']:
                data['user'] = db_response['data'][0]['user']
            response = yield gen.Task(querysets.sensor.insert, json_data)
        else:
            raise gen.Return(db_response)

        raise gen.Return(response)

    @gen.coroutine
    def json_invalid(self, json_data):
        raise gen.Return(errors.JSON['invalid_format'])

    @gen.coroutine
    def post(self):
        self.set_header('ContentType', 'application/json')
        json_data = json.loads(self.request.body)
        response = (yield self.validate(json_data))
        self.write(response)

# curl -X POST -H "application/json" -d '{"auth": {"type": "token", "id": "054331b3aaa59aeec63a9285326072cbd9e87501c3fc96ce0be593256dfadd7c", "user": "b97ab76d-613e-46f4-89b9-d9bd49db8164"}, "data": [{"id_apac": 2000, "nome": "aloha", "local": "hey", "latitude": "1000", "longitude": "10231"}]}' http://127.0.0.1:8888/api/v1/sensores/criar/  # noqa
