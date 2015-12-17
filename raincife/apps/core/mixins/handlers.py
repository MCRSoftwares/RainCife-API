# -*- coding: utf-8 -*-

from tornado import gen
from jsonado.handlers import ReDBHandler
from decouple import config
from tornado_cors import CorsMixin


class CORSHandler(CorsMixin, ReDBHandler):
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN = '*'
    CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages'
    CORS_CREDENTIALS = True

    def __init__(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        super(CORSHandler, self).__init__(*args, **kwargs)


class CurrentUserMixin(CORSHandler):

    def get_current_user(self):
        return self.get_secure_cookie(
            config('USER_AUTH_COOKIE', default='user', cast=str))


class URLQueryMixin(CurrentUserMixin):

    @gen.coroutine
    def get_url_query(self, arguments):
        """
        Método assíncrono responsável por tratar as
        query strings recebidas pela URL.
        """
        fields = self.pop_arguments('fields', None)
        result = self.docs.without('senha').filter(arguments)
        if fields:
            result = result.fields(*fields)
        raise gen.Return((yield result.run()))
