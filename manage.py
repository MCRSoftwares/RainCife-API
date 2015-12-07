# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from raincife.routers import routers
from decouple import config
from jsonado.core.utils import TableFinder
from jsonado.core.utils import Commands
import rethinkdb as r


class RaincifeCommands(Commands):

    def cmd_serve(self, *args):
        app = Application(routers)
        if len(args) > 0:
            port = int(args[0])
        else:
            port = config('PORT', default=8888, cast=int)
        app.listen(port)
        r.set_loop_type('tornado')
        IOLoop.current().start()

    def cmd_sync(self, *args):
        tables = TableFinder().find('raincife/apps/')
        c = r.connect(
            port=config('DB_PORT', default=28015, cast=int),
            host=config('DB_HOST', default='localhost')
        )
        for obj in tables:
            r.db_list().contains(obj.db).do(
                lambda db_exists: r.branch(
                    db_exists,
                    {'created': 0},
                    r.db_create(obj.db))
            ).run(c)
            r.db(obj.db).table_list().contains(obj.table).do(
                lambda table_exists: r.branch(
                    table_exists,
                    {'created': 0},
                    r.db(obj.db).table_create(obj.table))
            ).run(c)


RaincifeCommands()
