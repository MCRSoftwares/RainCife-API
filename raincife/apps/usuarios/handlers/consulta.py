# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from usuarios.db.tables import Usuario
from tornado import gen


class UsuarioListHandler(ReDBHandler):
    table = Usuario

    @gen.coroutine
    def get(self):
        self.write({'data': (yield self.url_query)})

    @gen.coroutine
    def get_url_query(self, arguments):
        if 'fields' in arguments:
            fields = self.get_param('fields')
            result = self.documents.fields(*fields).filter(arguments)
            raise gen.Return((yield result.run()))
        raise gen.Return((yield self.documents.filter(arguments).run()))
