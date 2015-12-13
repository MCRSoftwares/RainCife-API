# -*- coding: utf-8 -*-

from jsonado.db import tables
from jsonado.core.utils import get_module
import rethinkdb as r


class MarcadorReQL(tables.ReQL):
    """
    Classe responsável por executar as consultas realizadas no Manager que
    a referencia.
    """
    def new_marcador(self, usuario_id, **kwargs):
        """
        Método que adiciona um novo marcador para
        o usuário fornecido através do ID.
        """
        Usuario = get_module('usuarios.db.tables', 'Usuario')
        return Usuario.docs.get(usuario_id).raw().do(
            self.docs.insert({
                'usuario_id': r.row['id'],
            }.update(**kwargs)).raw()
        )


class MarcadorManager(tables.Manager):
    """
    Classe responsável por definir os métodos de consultas
    realizadas para tabela que o referenciar.
    """
    def get_reql(self):
        return MarcadorReQL(db=self)

    @tables.reql
    def new_marcador(self, usuario_id, **kwargs):
        """
        Método que executa um método com mesmo nome, definido na ReQL.
        """
        return self.get_reql().new_marcador(usuario_id, **kwargs)
