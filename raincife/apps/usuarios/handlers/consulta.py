# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from usuarios.db.tables import Usuario
from tornado import gen


class UsuarioListHandler(ReDBHandler):
    """
    Handler responsável pela listagem de usuários existentes no banco.
    """
    table = Usuario

    @gen.coroutine
    def get(self):
        """
        Método assíncrono responsável por retornar
        os dados recuperados do banco via GET.
        """
        self.write({'data': (yield self.url_query)})

    @gen.coroutine
    def get_url_query(self, arguments):
        """
        Método assíncrono responsável por tratar as
        query strings recebidas pela URL.
        """
        if 'fields' in arguments:
            fields = self.get_param('fields')
            result = self.docs.filter(arguments).fields(*fields)
            raise gen.Return((yield result.run()))
        raise gen.Return((yield self.docs.filter(arguments).run()))
