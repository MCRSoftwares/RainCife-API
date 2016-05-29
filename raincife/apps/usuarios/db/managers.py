# -*- coding: utf-8 -*-

from jsonado.db import tables
from jsonado.core.utils import get_module
from datetime import datetime
from decouple import config
import rethinkdb as r


class UsuarioReQL(tables.ReQL):
    """
    Classe responsável por executar as consultas realizadas no Manager que
    a referencia.
    """
    def fields(self, *args):
        """
        Método que filtra os campos retornados pela query executada.
        """
        return self.pluck(*args)

    def marcadores(self, usuario_id):
        """
        Método que retorna todos os marcadores de um usuário,
        junto das demais informações do mesmo.
        """
        Marcador = get_module('marcadores.db.tables', 'Marcador')
        return self.get(usuario_id).merge(
            lambda row: {
                'marcadores': Marcador.docs.raw().get_all(
                    row['id'], index='usuario_id').coerce_to('array')
            })

    def new_usuario(self, data):
        """
        Método que cria um usuário com os dados informados.
        """
        data['criado_em'] = r.expr(datetime.now(
            r.make_timezone(config('TIMEZONE', default='-03:00'))))
        return self.insert(data)

    def novo_login(self):
        """
        Método que realiza o login e salva a data em que o usuário o realizou.
        """
        return self.update({'ultimo_login': r.expr(datetime.now(
            r.make_timezone(config('TIMEZONE', default='-03:00'))))})


class UsuarioManager(tables.Manager):
    """
    Classe responsável por definir os métodos de consultas
    realizadas para tabela que o referenciar.
    """
    def get_reql(self):
        return UsuarioReQL(db=self)

    @tables.reql
    def fields(self, *args):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().fields(*args)

    @tables.reql
    def marcadores(self, usuario_id):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().marcadores(usuario_id)

    @tables.reql
    def new_usuario(self, data):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().new_usuario(data)

    @tables.reql
    def novo_login(self):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().novo_login()
