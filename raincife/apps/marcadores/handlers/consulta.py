# -*- coding: utf-8 -*-

from core.mixins import URLQueryMixin
from marcadores.db.tables import Marcador
from tornado import gen
from tornado.web import authenticated


class MarcadorListHandler(URLQueryMixin):
    """
    Handler responsável pela listagem de marcadores existentes no banco.
    """
    table = Marcador

    @authenticated
    @gen.coroutine
    def get(self):
        """
        Método assíncrono responsável por retornar
        os dados recuperados do banco via GET.
        """
        self.write({'data': (yield self.url_query)})
