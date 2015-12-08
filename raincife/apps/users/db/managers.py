# -*- coding: utf-8 -*-

from jsonado.db import tables


class UserReQL(tables.ReQL):

    def fields(self, *args):
        return self.r.pluck(*args)


class UserManager(tables.Manager):

    def get_reql(self):
        return UserReQL(redb=self.r)

    def fields(self, *args):
        return self.get_reql().fields(*args)
