# -*- coding: utf-8 -*-

from jsonado.db import tables


class TokenReQL(tables.ReQL):

    def usuario(self, usuario_id):
        return self.filter({'usuario_id': usuario_id})


class TokenManager(tables.Manager):

    def get_reql(self):
        return TokenReQL(db=self)

    @tables.reql
    def usuario(self, usuario_id):
        return self.get_reql().usuario(usuario_id)
