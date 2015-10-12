# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado import gen
from .. import querysets


class SensorRetrieveHandler(RequestHandler):

    @gen.coroutine
    def get(self, sensor_id):
        response = yield gen.Task(querysets.sensor.get_by_id, sensor_id)
        self.write(response)
