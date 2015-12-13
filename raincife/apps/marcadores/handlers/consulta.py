# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from marcadores.db.tables import Marcador
from tornado import gen


class MarcadorListHandler(ReDBHandler):
    table = Marcador

    @gen.coroutine
    def get(self):
        self.write({'data': (yield self.url_query)})

    @gen.coroutine
    def get_url_query(self, arguments):
        if 'fields' in arguments:
            fields = self.get_param('fields')
            result = self.docs.filter(arguments).fields(*fields)
            raise gen.Return((yield result.run()))
        raise gen.Return((yield self.docs.filter(arguments).run()))
