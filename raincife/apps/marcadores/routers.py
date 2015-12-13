# -*- coding: utf-8 -*-

from marcadores.handlers import MarcadorListHandler


base_router = '/api/v1/marcadores{}'

routers = [
    (base_router.format('/'), MarcadorListHandler),
]
