# -*- coding: utf-8 -*-


from usuarios.handlers import UsuarioListHandler
from usuarios.handlers import UsuarioCreateHandler
from usuarios.handlers import UsuarioUpdateHandler


default_url = '/api/v1/usuarios{}'

routers = [
    (default_url.format('/'), UsuarioListHandler),
    (default_url.format('/alterar/'), UsuarioUpdateHandler),
    (default_url.format('/criar/'), UsuarioCreateHandler),
]
