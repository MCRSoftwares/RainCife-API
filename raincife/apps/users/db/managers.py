# -*- coding: utf-8 -*-

from jsonado.db import tables


class UserReQL(tables.ReQL):
    pass


class UserManager(tables.Manager):

    def get_reql(self):
        return UserReQL(redb=self.r)
