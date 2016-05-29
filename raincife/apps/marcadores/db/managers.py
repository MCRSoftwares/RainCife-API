# -*- coding: utf-8 -*-

from jsonado.db import tables
from datetime import datetime
from decouple import config
import rethinkdb as r


class MarcadorReQL(tables.ReQL):
    """
    Classe responsável por executar as consultas realizadas no Manager que
    a referencia.
    """
    def new_marcador(self, **kwargs):
        """
        Método que adiciona um novo marcador para
        o usuário fornecido através do ID.
        """
        data = {
            'usuario_id': kwargs.pop('usuario_id', None),
            'criado_em': r.expr(datetime.now(r.make_timezone(
                config('TIMEZONE', default='-03:00'))))
        }
        data.update(kwargs)
        return self.insert(data)


class MarcadorManager(tables.Manager):
    """
    Classe responsável por definir os métodos de consultas
    realizadas para tabela que o referenciar.
    """
    def get_reql(self):
        return MarcadorReQL(db=self)

    @tables.reql
    def new_marcador(self, **kwargs):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().new_marcador(**kwargs)
