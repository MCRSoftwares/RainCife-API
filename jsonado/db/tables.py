# -*- coding: utf-8 -*-

from jsonado.core.decorators import classproperty
from jsonado.db.exceptions import ReDBError
from tornado import gen
import rethinkdb as r


def reql(query):
    def query_wrapper(instance, *args, **kwargs):
        return instance.__class__(
            table=instance.table, __prev__=instance,
            __reql__=query(instance, *args, **kwargs))
    return query_wrapper


class Connection(object):
    db_port = '28015'
    db_host = 'localhost'

    def __init__(self, *args, **kwargs):

        for name, attr in {
                'db_host': self.get_db_host,
                'db_port': self.get_db_port
        }.iteritems():
            if not isinstance(attr(), basestring):
                raise ReDBError(
                    code='attr_is_not_string',
                    args=[name, type(attr()).__name__]
                )

        self.connection = r.connect(
            host=self.get_db_host(),
            port=self.get_db_port()
        )
        super(Connection, self).__init__(*args, **kwargs)

    def get_db_port(self):
        return self.db_port

    def get_db_host(self):
        return self.db_host

    def get(self):
        return self.connection


class ReQL(object):

    def __init__(self, db, *args, **kwargs):
        self.manager = db
        self.r = db.r
        super(ReQL, self).__init__(*args, **kwargs)

    def __getattr__(self, *args):
        return self.r.__getattribute__(*args)

    def get_manager(self):
        return self.manager

    def all(self):
        return self.r


class Manager(object):

    def __init__(self, table, *args, **kwargs):
        self.table = table
        self.r = r.db(self.table.get_db()).table(self.table.get_table())
        self.__reql__ = kwargs.pop('__reql__', None)
        self.__prev__ = kwargs.pop('__prev__', None)
        super(Manager, self).__init__(*args, **kwargs)

    def __getattr__(self, *args):
        attr = self.r.__getattribute__(*args)

        def query_wrapper(*args, **kwargs):
            query = attr(*args, **kwargs)
            return self.__class__(
                table=self.table, __prev__=self, __reql__=query)
        return query_wrapper

    def raw(self):
        if self.__prev__ and self.__reql__:
            method = self.__reql__.__class__.__dict__['st']
            args = self.__reql__.__dict__['args']
            kwargs = self.__reql__.__dict__['optargs']
            if method in ['db', 'table']:
                return self.__prev__.raw()
            args.pop(0)
            return self.__prev__.raw().__getattribute__(
                method)(*args, **kwargs)
        return self.r

    def get_connection(self):
        return self.table.get_connection()

    def get_table(self):
        return self.table

    def get_reql(self):
        return ReQL(db=self)

    @reql
    def all(self):
        return self.get_reql().all()

    @gen.coroutine
    def run(self, cursor=False):
        result = (yield self.raw().run((yield self.get_connection())))
        if not cursor and result:
            if issubclass(result.__class__, r.net_tornado.TornadoCursor):
                raise gen.Return((yield self.read_cursor(result)))
        raise gen.Return(result)

    @gen.coroutine
    def read_cursor(self, cursor):
        items = []
        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            items.append(item)
        raise gen.Return(items)


class Table(object):
    db = None
    table = None
    connection = Connection
    documents = Manager
    indexes = {}

    def __init__(self, *args, **kwargs):
        for name, attr in {
                'db': self.get_db,
                'table': self.get_table
        }.iteritems():
            if not isinstance(attr(), basestring):
                raise ReDBError(
                    code='attr_is_not_string',
                    args=[name, type(attr()).__name__]
                )

        if not self.connection or not issubclass(self.connection, Connection):
            raise ReDBError(
                code='attr_is_not_connection',
                args=[type(self.connection).__name__]
            )
        super(Table, self).__init__(*args, **kwargs)

    def __getattr__(self, *args):
        return self.docs.r.__getattribute__(*args)

    def get_table(self):
        return self.table

    def get_db(self):
        return self.db

    def get_connection(self, raw=True):
        return self.conn.get() if raw else self.conn

    def get_indexes(self):
        return self.indexes

    @classproperty
    def docs(cls):
        return cls.documents(cls())

    @classproperty
    def conn(cls):
        return cls.connection()
