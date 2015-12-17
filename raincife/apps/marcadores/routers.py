# -*- coding: utf-8 -*-

"""
Routers definem os caminhos (URLs) da aplicação.
Este módulo define os routers relacionados à aplicação de marcadores.
"""

from marcadores.handlers import MarcadorListHandler
from marcadores.handlers import MarcadorCreateHandler


base_router = '/api/v1/marcadores{}'

routers = [
    (base_router.format('/'), MarcadorListHandler),
    (base_router.format('/criar/'), MarcadorCreateHandler),
]
