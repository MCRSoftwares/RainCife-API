# -*- coding: utf-8 -*-

from jsonado.db import tables


class UserReQL(tables.ReQL):

    def fields(self, *args):
        return self.pluck(*args)


class UserManager(tables.Manager):

    def get_reql(self):
        return UserReQL(db=self)

    @tables.reql
    def fields(self, *args):
        return self.get_reql().fields(*args)
