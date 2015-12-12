# -*- coding: utf-8 -*-

from jsonado.db import tables
from usuarios.db.tables import Usuario
import rethinkdb as r


class MarcadorReQL(tables.ReQL):

    def new_marcador(self, usuario_id, **kwargs):
        return Usuario.documents().get(usuario_id).raw().do(
            self.documents.insert({
                'usuario_id': r.row['id'],
            }.update(**kwargs)).raw()
        )


class MarcadorManager(tables.Manager):

    def get_reql(self):
        return MarcadorReQL(db=self)

    @tables.reql
    def new_marcador(self, usuario_id, **kwargs):
        return self.get_reql().new_marcador(usuario_id, **kwargs)