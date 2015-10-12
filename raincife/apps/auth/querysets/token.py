# -*- coding: utf-8 -*-

import rethinkdb as r
from raincife.db.redb import q
from tornado import gen


@gen.coroutine
def filter(data):
    results = yield q.run(r.table('token').filter(data))
    raise gen.Return(results)
