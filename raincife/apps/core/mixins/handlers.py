# -*- coding: utf-8 -*-

from jsonado.handlers import CORSHandler


class CORSMixin(CORSHandler):
    """
    Class Mixin responsável por redefinir
    variáveis relacionadas ao CORS.
    """
    CORS_EXPOSE_HEADERS = None
    CORS_CREDENTIALS = None
    CORS_HEADERS = None
