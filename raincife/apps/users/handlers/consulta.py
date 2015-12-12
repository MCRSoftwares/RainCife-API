# -*- coding: utf-8 -*-

from jsonado.handlers.generic import ReDBHandler
from users.db.tables import User
from tornado import gen


class UserListHandler(ReDBHandler):
    table = User

    @gen.coroutine
    def get(self):
        self.write({'data': (yield self.url_query)})

    @gen.coroutine
    def get_url_query(self, arguments):
        if 'fields' in arguments:
            fields = self.get_param('fields').split(',')
            result = self.documents.fields(*fields).filter(arguments)
            raise gen.Return((yield result.run()))
        raise gen.Return((yield self.documents.filter(arguments).run()))
