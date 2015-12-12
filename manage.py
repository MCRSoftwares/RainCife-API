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
        for obj in tables:
            r.db_list().contains(obj.db).do(
                lambda db_exists: r.branch(
                    db_exists,
                    {'created': 0},
                    r.db_create(obj.db))
            ).run(c)
            redb = r.db(obj.db)
            redb.table_list().contains(obj.table).do(
                lambda table_exists: r.branch(
                    table_exists,
                    {'created': 0},
                    redb.table_create(obj.table))
            ).run(c)


RaincifeCommands()
