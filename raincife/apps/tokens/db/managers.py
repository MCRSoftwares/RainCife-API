# -*- coding: utf-8 -*-

from jsonado.db import tables
from jsonado.core.utils import get_module
from datetime import datetime
import rethinkdb as r
import bcrypt
import hashlib


class TokenReQL(tables.ReQL):
    """
    Classe responsável por executar as consultas realizadas no Manager que
    a referencia.
    """
    def usuario(self, usuario_id):
        """
        Método que filtra os usuários pelo id.
        """
        return self.filter({'usuario_id': usuario_id})

    def new_token(self, usuario):
        """
        Método que gera e salva um token para o usuário fornecido.
        """
        Usuario = get_module('usuarios.db.tables', 'Usuario')
        Usuario.docs.raw().get_all(usuario, index='usuario').do(
            self.insert({
                'usuario_id': r.row['id'],
                'token': bcrypt.hashpw(
                    hashlib.sha256().hexdigest(), bcrypt.gensalt()),
                'criado_em': r.expr(datetime.now(r.make_timezone('-07:00')))
            })
        )


class TokenManager(tables.Manager):
    """
    Classe responsável por definir os métodos de consultas
    realizadas para tabela que o referenciar.
    """
    def get_reql(self):
        return TokenReQL(db=self)

    @tables.reql
    def usuario(self, usuario_id):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().usuario(usuario_id)

    @tables.reql
    def new_token(self, usuario):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().new_token(usuario)
