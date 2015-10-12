# -*- coding: utf-8 -*-

from decouple import config
from tornado import gen
import rethinkdb as r


class ReQL(object):
    cursor = None

    def __init__(self, *args, **kwargs):
        self.connection = r.connect(
            host=config('HOST'), port=config('DB_PORT'), db=config('DB_NAME'))

    @gen.coroutine
    def _read(self):
        items = []
        while (yield self.cursor.fetch_next()):
            item = yield self.cursor.next()
            items.append(item)

        raise gen.Return(items)

    @gen.coroutine
    def run(self, query):
        c = yield self.connection
        self.cursor = yield query.run(c)
        if self.cursor:
            items = yield self._read()
            raise gen.Return({'data': items})
        raise gen.Return({'error': {'Query result returned empty.'}})

    @gen.coroutine
    def single(self, query):
        c = yield self.connection
        item = yield query.run(c)
        raise gen.Return(item)


def initdb():
    r.set_loop_type("tornado")
    globals()['q'] = ReQL()
