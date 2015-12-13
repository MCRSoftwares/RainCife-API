# -*- coding: utf-8 -*-

from jsonado.db import tables
from jsonado.core.utils import get_module


class UsuarioReQL(tables.ReQL):

    def fields(self, *args):
        return self.pluck(*args)

    def marcadores(self, usuario_id):
        Marcador = get_module('marcadores.db.tables', 'Marcador')
        return self.get(usuario_id).merge(
            lambda row: {
                'marcadores': Marcador.docs.raw().get_all(
                    row['id'], index='usuario_id').coerce_to('array')
            })


class UsuarioManager(tables.Manager):

    def get_reql(self):
        return UsuarioReQL(db=self)

    @tables.reql
    def fields(self, *args):
        return self.get_reql().fields(*args)

    @tables.reql
    def marcadores(self, usuario_id):
        return self.get_reql().marcadores(usuario_id)
