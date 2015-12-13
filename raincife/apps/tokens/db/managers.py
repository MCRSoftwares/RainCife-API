# -*- coding: utf-8 -*-

from jsonado.db import tables


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
