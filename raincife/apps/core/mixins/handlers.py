# -*- coding: utf-8 -*-

from tornado import gen
from jsonado.handlers import ReDBHandler


class URLQueryMixin(ReDBHandler):

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
