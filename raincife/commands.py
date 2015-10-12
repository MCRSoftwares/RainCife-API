# -*- coding: utf-8 -*-

import rethinkdb as r
from decouple import config
from raincife.db.tables import manager
from raincife.logs.log import COMMANDS as l


def _create_redb_connection():
    print l['start_temp_conn']
    connection = r.connect(
        host=config('HOST'), port=config('DB_PORT'), db=config('DB_NAME'))
    return connection


def _close_redb_connection(connection):
    print l['close_conn']
    connection.close(noreply_wait=False)
    print l['done']


def create_tables():
    connection = _create_redb_connection()
    manager.add('user', 'token', 'sensor')
    manager.set_indexes({
        'user': ['username'],
        'token': ['user'],
        'sensor': ['id_apac']
    })
    for table in manager.all():
        try:
            print l['create_table'].format(table)
            r.table_create(table).run(connection)
            r.table(table).index_create(manager.get_index(table, 0))
            print l['value_done'].format(table)
        except r.RqlRuntimeError:
            print l['table_exists'].format(table)
    _close_redb_connection(connection)


def create_default_users():
    connection = _create_redb_connection()
    print l['create_users']

    r.table(manager.get(0)).insert([{
        'username': config('APAC_USER'),
        'password': config('APAC_PASS')
    }, {
        'username': config('SYSTEM_USER'),
        'password': config('SYSTEM_PASS')
    }]).run(connection)
    print l['users_done']

    apac_user = r.table(manager.get(0)).filter({
        'username': config('APAC_USER')
    }).get_field('id').run(connection).next()
    system_user = r.table(manager.get(0)).filter({
        'username': config('SYSTEM_USER')
    }).get_field('id').run(connection).next()

    print l['create_tokens']
    r.table(manager.get(1)).insert([{
        'user': apac_user,
        'id': config('APAC_TOKEN')
    }, {
        'user': system_user,
        'id': config('SYSTEM_TOKEN')
    }]).run(connection)

    print l['tokens_done']
    _close_redb_connection(connection)
