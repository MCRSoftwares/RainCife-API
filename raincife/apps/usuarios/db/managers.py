# -*- coding: utf-8 -*-

from jsonado.db import tables


class UsuarioReQL(tables.ReQL):

    def fields(self, *args):
        return self.pluck(*args)


class UsuarioManager(tables.Manager):

    def get_reql(self):
        return UsuarioReQL(db=self)

    @tables.reql
    def fields(self, *args):
        return self.get_reql().fields(*args)
