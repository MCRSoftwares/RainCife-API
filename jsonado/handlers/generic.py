# -*- coding: utf-8 -*-

from jsonado.handlers.base import ReDBHandlerBase
from tornado.web import RequestHandler
from tornado_cors import CorsMixin


class ReDBHandler(ReDBHandlerBase, RequestHandler):

    def __init__(self, *args, **kwargs):
        super(ReDBHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'application/json')


class CORSHandler(CorsMixin, ReDBHandler):
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN = '*'
    CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages'
    CORS_CREDENTIALS = True
