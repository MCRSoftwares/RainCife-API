# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import netutil
from tornado import process
from raincife.routers import routers
from decouple import config
from jsonado.core.utils import ClassFinder
from jsonado.core.utils import Commands
from raincife.db.connections import MainConnection
from raincife.logs import ServerLog
import rethinkdb as r


class RaincifeCommands(Commands):
    port = config('PORT', default=8888, cast=int)
    host = config('HOST', default='localhost')
    fork_processes = config('FORK_PROCESSES', default=0, cast=int)

    def cmd_debug(self, *args):
        port = int(args[0]) if args else self.port
        ServerLog.info(code='dev_server_starting', args=[port])
        app = Application(routers, debug=True, autoreload=False)
        app.listen(port)
        r.set_loop_type('tornado')
        ioloop = IOLoop.current()
        ioloop.add_callback(
            callback=ServerLog.info,
            code='server_started',
            args=[self.host, port]
        )
        ioloop.start()

    def cmd_serve(self, *args):
        port = int(args[0]) if args else self.port
        ServerLog.info(code='dev_server_starting', args=[port])
        app = Application(routers)
        sockets = netutil.bind_sockets(port)
        process.fork_processes(self.fork_processes)
        server = HTTPServer(app)
        server.add_sockets(sockets)
        r.set_loop_type('tornado')
        ioloop = IOLoop.current()
        ioloop.add_callback(
            callback=ServerLog.info,
            code='server_started',
            args=[self.host, port]
        )
        ioloop.start()

    def cmd_sync(self, *args):
        tables = ClassFinder(
            'jsonado.db.tables', 'Table').find('raincife/apps/')
        c = MainConnection().get()
        db_list = []
        table_list = []
        index_list = []
        for obj in tables:
            r.db_list().contains(obj.db).do(
                lambda db_exists: r.branch(
                    db_exists,
                    {'created': 0},
                    r.db_create(obj.db)
                )
            ).run(c)
            redb = r.db(obj.db)
            redb.table_list().contains(obj.table).do(
                lambda table_exists: r.branch(
                    table_exists,
                    {'created': 0},
                    redb.table_create(obj.table)
                )
            ).run(c)
            retb = redb.table(obj.table)
            if hasattr(obj, 'indexes'):
                for i, value in obj.indexes.iteritems():
                    retb.index_list().contains(i).do(
                        lambda index_exists: r.branch(
                            index_exists,
                            {'created': 0},
                            retb.index_create(i, value)
                            if value else retb.index_create(i)
                        )
                    ).run(c)
                    index_list.append(i)
            db_list.append(obj.db)
            table_list.append(obj.table)

        redb_list = r.db_list().run(c)
        redb_list.remove('rethinkdb')
        self._check_if_exists(db_list, redb_list, c, r.db_drop)
        for db in db_list:
            self._check_if_exists(
                table_list, r.db(db).table_list().run(c),
                c, r.db(db).table_drop)
            for table in table_list:
                self._check_if_exists(
                    index_list, r.db(db).table(table).index_list().run(c),
                    c, r.db(db).table(table).index_drop)

    def _check_if_exists(self, value_list, origin_list, c, command):
        for val in origin_list:
            if val not in value_list:
                command(val).run(c)
                return False
        return True

RaincifeCommands()
