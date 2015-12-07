# -*- coding: utf-8 -*-

from jsonado.db import tables


class TokenReQL(tables.ReQL):
    pass


class TokenManager(tables.Manager):

    def get_reql(self):
        return TokenReQL(redb=self.r)
