# -*- coding: utf-8 -*-

from jsonado.handlers import CORSHandler


class CORSMixin(CORSHandler):
    CORS_EXPOSE_HEADERS = None
    CORS_CREDENTIALS = None
    CORS_HEADERS = None
