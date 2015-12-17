# -*- coding: utf-8 -*-

from core.mixins import CORSMixin
from marcadores.db.tables import Marcador
from tornado import gen


class MarcadorListHandler(CORSMixin):
    """
    Handler responsável pela listagem de marcadores existentes no banco.
    """
    table = Marcador

    @gen.coroutine
    def get(self):
        """
        Método assíncrono responsável por retornar
        os dados recuperados do banco via GET.
        """
        self.write({'data': (yield self.get_url_query())})

    @gen.coroutine
    def get_url_query(self):
        raise gen.Return((yield self.docs.all().without('criado_em').run()))
