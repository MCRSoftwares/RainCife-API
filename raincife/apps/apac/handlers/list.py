# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado import gen
from .. import querysets


class SensorListHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        response = yield gen.Task(querysets.sensor.all)
        count = yield gen.Task(querysets.sensor.count)
        response.update({'count': count})
        self.write(response)
