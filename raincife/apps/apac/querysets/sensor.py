# -*- coding: utf-8 -*-

import rethinkdb as r
from raincife.db.redb import q
from tornado import gen


@gen.coroutine
def all():
    results = yield q.run(r.table('sensor'))
    raise gen.Return(results)


@gen.coroutine
def count():
    result = yield q.single(r.table('sensor').count())
    raise gen.Return(result)


@gen.coroutine
def insert(data):
    data['data'] = yield q.unique_only('sensor', data['data'], 'id_apac')
    results = yield q.single(r.table('sensor').insert(data['data']))
    raise gen.Return(results)


@gen.coroutine
def get_by_id(sensor_id):
    result = yield q.run(
        r.table('sensor').filter({'id_apac': int(sensor_id)}))
    raise gen.Return(result)
