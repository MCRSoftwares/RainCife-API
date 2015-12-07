# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from raincife.routers import routers
from decouple import config


def start():
    return Application(routers)


def listen(app):
    app.listen(config('PORT', default=8888, cast=int))
    IOLoop.current().start()

listen(start())
