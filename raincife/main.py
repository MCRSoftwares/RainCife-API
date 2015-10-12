# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from decouple import config
from tornado.httpserver import HTTPServer
from db.redb import initdb
from raincife.utils import str_bool
from raincife.logs.log import MAIN as l


def start():
    return Application([])
app = start()


def load_handlers():
    from urls import patterns
    app.add_handlers(config('DNS', default=config('HOST')), patterns)


def start_log():
    host = '{0}:{1}'.format(config('HOST'), config('PORT'))
    dns = config('DNS', default=host)
    print l['listen'].format(dns)
    print l['quit']


def listen():
    print l['load_settings']
    if str_bool(config('DEBUG', default='True')):
        print l['start_dev_server']
        start_log()
        app.listen(config('PORT'))
    else:
        print l['start_prod_server']
        start_log()
        server = HTTPServer(app)
        server.bind(config('PORT'))
        server.start(0)
    initdb()
    load_handlers()
    IOLoop.current().start()
