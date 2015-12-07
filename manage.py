# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from raincife.routers import routers
from decouple import config
from jsonado.core.utils import TableFinder
from jsonado.core.utils import Commands


class RaincifeCommands(Commands):

    def cmd_serve(self, *args):
        app = Application(routers)
        if len(args) > 0:
            port = int(args[0])
        else:
            port = config('PORT', default=8888, cast=int)
        app.listen(port)
        IOLoop.current().start()


RaincifeCommands()
